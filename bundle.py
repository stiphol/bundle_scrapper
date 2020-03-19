from bs4 import BeautifulSoup
import requests
import re

f= open("result.csv","w+") #РЕЗУЛЬТИРУЮЩИЙ CSV
file1 = open('test_bundle.csv', 'r') #ИСХОДНЫЙ ФАЙЛ
Lines = file1.readlines() 

for line in Lines: # ЧИТАЕМ ПОСТРОЧНО ФАЙЛ С БАНДЛАМИ
  bundle = line.strip()
  # r'^[0-9]{3}' - РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ, КОТОРОЕ ПРОВЕРЕЯТ ПЕРВЫЕ 3 СИМВОЛА БАНДЛА.
  if (re.search(r'^[0-9]{3}', bundle)): # ЕСЛИ ПЕРВЫЕ 3 - ЭТО ЦИФРЫ -- ЗНАЧИТ ЭТО IOS'НЫЙ БАНДЛ 
    url = 'https://apps.apple.com/app/id' + bundle # "ПРИКЛЕИТЬ" БАНДЛ К ССЫЛКЕ 
    app_name_class = "product-header__title app-header__title" # НАЗВАНИЕ HTML-КЛАССА, В КОТОРОМ ХРАНИТСЯ APP_NAME У IOS
    publisher_class = "link" # НАЗВАНИЕ HTML-КЛАССА, В КОТОРОМ ХРАНИТСЯ PUBLISHER_NAME У ANDROID
  else:
    url = 'https://play.google.com/store/apps/details?id=' + bundle
    app_name_class = "AHFaub" # НАЗВАНИЕ HTML-КЛАССА, В КОТОРОМ ХРАНИТСЯ APP_NAME У ANDROID
    publisher_class = "hrTbp R8zArc" # НАЗВАНИЕ HTML-КЛАССА, В КОТОРОМ ХРАНИТСЯ PUBLISHER_NAME У ANDROID

  response = requests.get(url) # ВЗЯТЬ URL СТРАНИЦЫ ИЗ СТОРА
  soup = BeautifulSoup(response.content, 'html.parser') #РАСПАРСИТЬ HTML С ПОМОЩЬЮ БИБЛИОТЕКИ BeautifulSoup 
  app_name = soup.find_all(class_=app_name_class) #ВЫТАЩИТЬ APP_NAME
  for tag in app_name: #ПО ДЕФОЛТУ НА ОДНОЙ СТРОКЕ  APP_NAME В APPSTORE ЕЩЕ УКАЗЫВАЮТ ВОЗРАСТНОЕ ОГРАНИЧЕНИЕ
    app_name = tag.text.strip() #ЭТИ КОМАНДЫ "СРЕЗАЮТ" НЕНУЖНЫЙ ХВОСТ 
    if publisher_class == "link":
      app_name = app_name[:-14] #КОНКРЕТНО ЗДЕСЬ ПРОИСХОДИТ СРЕЗ
    break
  
  publisher = soup.find_all(class_=publisher_class) #ВЫТАЩИТЬ PUBLISHER_NAME
  for tag in publisher: 
    publisher = tag.text.strip() #ВЫТАЩИТЬ ИМЕННО ТЕКСТОВУЮ ЧАСТЬ 
    break
  f.write(str(bundle) + ',' + str(app_name) + ',' + str(publisher) + '\n') #ЗАПИСЬ В ФАЙЛ С РАЗДЕЛЕНИЕМ ЧЕРЕЗ ,
  print (app_name, publisher, sep='/t') # ПРОСТО ВЫВОД В КОНСОЛЬ ДЛЯ СПРАВКИ 
f.close() #ЗАКРЫТЬ ФАЙЛ result.csv
file1.close() #ЗАКРЫТЬ ФАЙЛ test_bundle.csv