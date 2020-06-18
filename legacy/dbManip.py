#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 22:14:33 2017

@author: gabsrf
"""

import psycopg2

def readDB():

    conn_string = "host='ec2-54-235-204-221.compute-1.amazonaws.com' dbname='d2kenm0t890l2k' user='uhkvkghmwwexhb' password='d9379e5137f832277000bd105080f5a890d4c65b27bab66e40e9481d47855def'"
    db = psycopg2.connect(conn_string)
    
    cur = db.cursor()
    cur.execute("""SELECT * FROM tabela;""")  
    
    records = cur.fetchall()
    
    db.commit()
    db.close()
    
    return records
     
def cleanDB():
	
    conn_string = "host='ec2-54-235-204-221.compute-1.amazonaws.com' dbname='d2kenm0t890l2k' user='uhkvkghmwwexhb' password='d9379e5137f832277000bd105080f5a890d4c65b27bab66e40e9481d47855def'"
    db = psycopg2.connect(conn_string)
     
    cur = db.cursor()     
    cur.execute("""TRUNCATE TABLE tabela""")
    
    db.commit()
    db.close()
    return