import re
import requests
from abc import ABC, abstractmethod

import telegram
from crontab import CronTab
from bs4 import BeautifulSoup


class CronJob:

    def __init__(self, command, comment, schedule, enable_on_init):
        self.command = command
        self.comment = comment
        self.schedule = schedule

        self.cron_tab = CronTab(user='root')
        self.job = self.cron_tab.new(command=self.command, comment=self.comment)
        self.job.setall(self.schedule)

        if enable_on_init:
            self.set_enable(True)

    def set_enable(self, enable):
        self.job.enable(enable)


class ParcelTracker:

    def __init__(self, parcel_code, parcel_company):
        self.parcel_code = parcel_code
        self.parcel_company = parcel_company
        self.statuses_len = 0

    def __get_correios_statuses(self):
        url = f'http://rastreamentocorreios.info/consulta/{self.parcel_code}'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        self.statuses = []
        for raw_html in soup.find_all('li'):
            contents = raw_html.contents
            status = '\n'.join(
                [re.sub('<.*?>', '', str(content).replace('<br/>', '\n')) for content in contents if content != ' ']
            )
            status = status.replace('De', '*De*').replace('Para', '*Para*')
            self.statuses.append(status)

    def get_statuses(self):
        if self.parcel_company.lower() == 'correios':
            self.__get_correios_statuses()
        else:
            pass

    def has_change_in_status(self):
        if len(self.statuses) > self.statuses_len:
            self.statuses_len = len(self.statuses)
            return True
        else:
            return False


class Tesla(ABC):

    def __init__(self, auth_token):
        self.token = auth_token
        self.parcel_trackers = []

    @abstractmethod
    def send_message(self, message):
        pass

    @staticmethod
    def create_cronjob(command, comment, schedule, enable_on_init=True):
        job = CronJob(command, comment, schedule, enable_on_init)
        return job

    def create_parcel_tracking(self, parcel_code, parcel_company='Correios'):
        parcel_tracker = ParcelTracker(parcel_code, parcel_company)
        self.parcel_trackers.append(parcel_tracker)

    def consult_parcels_status(self):
        for tracker in self.parcel_trackers:
            tracker.get_statuses()
            if tracker.has_change_in_status():
                messages = [f'*Status Atualizado - {tracker.parcel_code}*']
                messages += tracker.statuses
                message = '\n\n'.join(messages)
                self.send_message(message)
            return


class TeslaTelegram(Tesla, ABC):

    def __init__(self, auth_token):
        super().__init__(auth_token)
        self.bot = telegram.Bot(token=self.token)

    def send_message(self, message, parse_mode='Markdown'):
        chat_id = self.bot.get_updates()[-1].message.chat_id
        self.bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
