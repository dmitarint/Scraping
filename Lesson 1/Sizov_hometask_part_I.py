# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import json
import requests
from pprint import pprint

name = 'dmitarint' #зададим имя
url = 'https://api.github.com/users/'+name+'/repos' #смотрим именно список репозиториев
response = requests.get(url) #запросим ответ от сервера с заданными параметрами
data = response.json() #на выходе получили список, в каждую ячейку которой зашит словарь
_ = []
for i in range(len(data)): #пройдемся по каждой ячейке и вытащим названия репозиториев для данного пользователя
   _.append(data[i]['name'])
repos = {name : _}

print (f'Для пользователя {name} список репозиториев следующий: \n {_}')

with open('data.json', 'w') as f: #сохраним данные в файл
    json.dump(repos, f)







