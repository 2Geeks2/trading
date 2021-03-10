# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import yfinance as yf
import smtplib




    
date = datetime.datetime.now().date()

print (str(date))

   

def run(**params):
    URL = "URL"
    response = requests.get(URL.format(**params))
    return response



response = run(query="registered%20direct%20offering")

closing = {}
opening = {}
string_opening =" OPENING: \n"
string_closing = " CLOSING: \n"

for link in BeautifulSoup(response.content, parse_only=SoupStrainer('a'),features="html.parser"):
    if link.has_attr('href'):
        if ("egistered" in (link["href"]) and (("quote/stock") in link["href"] or ("news/latest" in link["href"] ))):
            result = "DOMAIN" + link["href"]
            response = requests.get(result)
            soup = BeautifulSoup(response.content,features="html.parser")

            soup = soup.get_text()
            
            name_stock= re.findall(':[A-Z][A-Z][A-Z]+', str(soup))
            
            if not name_stock:
                
                name_stock= re.findall(': [A-Z][A-Z][A-Z]+', str(soup))

                if not name_stock:
                    
                    name_stock= re.findall(': [A-Z][A-Z][A-Z]+', str(soup))
                
                    if not name_stock:
                        
                        name_stock= re.findall('\([A-Z][A-Z][A-Z]+\)', str(soup))
                
    
            name_stock = name_stock[0]
            name_stock = name_stock.strip(" ").strip(":").strip(" ").strip("(").strip(")")
            data = yf.download(tickers=name_stock)
            current_price = data.tail(1)["Close"][0]

            if ("losing" in link["href"]  or "ompletion" in link["href"] or "loses" in link["href"] ):
                closing [name_stock] = result
                string_closing += " " + "  \n\n   stock="+ name_stock + " \n" + "link="+ result + " \n" + "current_price=" + str(current_price) + " \n\n"
            else:
                opening [name_stock] = result

    
                
                soup = re.sub('\$\d+(?:\.\d+)? million', ' ', str(soup))
                soup = re.sub('\$\d+(?:\.\d+)? Million', ' ', str(soup))
                prices = re.findall("\$\d+\.\d+", str(soup))
                initial = 1000
                for price in prices:
                    price= price.strip("$")
                    if float(price) < initial:
                        final_price = float(price)
                        initial = float(price)
                string_opening += " " + "  \n\n  stock="+ name_stock + " \n" + "link="+ result + " \n" + "current_price=" + str(current_price) + " \n"  + "offered_price=" + str(final_price) + " \n\n"


                

import smtplib, ssl, string

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login('EMAIL', 'PASSWORD')

    message = ("From: %s\r\n" % "Lorenzo Servadei"
            + "To: %s\r\n" % "Lorenzo Servadei"
            + "Subject: %s\r\n" % "TRADING"
            + "\r\n"
            + string_closing +  string_opening) 


    # Send text message through SMS gateway of destination number
    server.sendmail( 'FROM_MAIL', 'TO_MAIL', message)




            
            
            


