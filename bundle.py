from bs4 import BeautifulSoup
import requests
import re

f= open("result.csv","w+") #РЕЗУЛЬТИРУЮЩИЙ CSV
file1 = open('test_bundle.csv', 'r') #ИСХОДНЫЙ ФАЙЛ
Lines = file1.readlines() 

for line in Lines: 
  bundle = line.strip()
  if (re.search(r'^[0-9]{3}', bundle)): # ios
    url = 'https://apps.apple.com/app/id' + bundle 
    app_name_class = "product-header__title app-header__title"
    publisher_class = "link"
  else:
    url = 'https://play.google.com/store/apps/details?id=' + bundle
    app_name_class = "AHFaub"
    publisher_class = "hrTbp R8zArc"

  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')  
  app_name = soup.find_all(class_=app_name_class)
  for tag in app_name:
    app_name = tag.text.strip()
    if publisher_class == "link":
      app_name = app_name[:-14]
    break
  
  publisher = soup.find_all(class_=publisher_class)
  for tag in publisher:
    publisher = tag.text.strip()
    break
  f.write(str(bundle) + ',' + str(app_name) + ',' + str(publisher) + '\n')
  print (app_name, publisher, sep=',')
f.close()
file1.close()