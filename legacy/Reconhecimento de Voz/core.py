import speech_recognition as sr
import serial

r = sr.Recognizer()
arduino = serial.Serial('COM4', 9600)
keyWords = ["acender", "ligar", "acionar", 
            "apagar", "desligar", 
            "led", "luz", "lampada",
            "temperatura", "hoje", "amanha", "semana"]

estados = [["acender", "ligar", "acionar", "ativar"],["apagar", "desligar", "desativar"]]
dict = {"led": "l"}

#---------------------------------------------------------------------#
def ouveAudio():
    with sr.Microphone() as source:
        print("\nDiga algo!")
        audio = r.listen(source)
    
    try:
        return r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return "desconhecido"
    except sr.RequestError as e: 
        return "desconectado"
    
#---------------------------------------------------------------------#   
def normalizacaoComando(str):
    text = str.split()
    i=0    
    for word in text:
        text[i] = word.replace(',','')
        text[i] = word.replace('\'','')
        text[i] = word[1:]
        text[i] = word.lower()
        i = i + 1
    text = [word for word in text if word in keyWords]
    return text

#---------------------------------------------------------------------#
def controlaArduino(parametros):
    
    if len(parametros) >= 2:
        estado = parametros[0]
        dispositivo = parametros[1]
        
        if estado in estados[0]:
            mensagem = "1"
        elif estado in estados[1]:
            mensagem = "0"
        
        mensagem += dict[dispositivo]
        
        arduino.write(mensagem)
        return
    else: return
    
#---------------------------------------------------------------------#
ativo = True
while ativo:
    leitura = ouveAudio()
    
    if leitura == "desconhecido":
        print("Nao entendi o que voce disse. Pode repetir?")
        
    elif leitura == "desconectado":
        print("Nao consegui me conectar ao servidor. Cheque a conexao e tente novamente!")
    
    elif leitura == "boa noite":
        print("Até mais! :)")
        ativo = False
        arduino.close()
    
    else:
        leitura = normalizacaoComando(leitura)
        controlaArduino(leitura)

#---------------------------------------------------------------------#
