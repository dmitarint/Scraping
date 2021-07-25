# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
from pprint import pprint
url_token = 'https://test.api.amadeus.com/v1/security/oauth2/token' #для решения задания нашел сайт amadeus.com. Предоставляет услуги для путешественников (вылеты, отели и прочее).

# зададим заголовки запроса.
get_token_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0', # User-Agent - браузер, с которого отправляется запрос.
              'Content-Type': 'application/x-www-form-urlencoded'} # специализированный заголовок для аутентификации

# параметры для получения токена выданы на сайте
get_token_params = {'grant_type': 'client_credentials',
             'client_id': 'nf8XLa1Z3MK1MDwutFmvWo3MaxgHCL2K',
             'client_secret': '9rcf1fVdYGE9tL12'}

# отправляем запрос с именем и паролем и получаем токен
r = requests.post(url_token, data = get_token_params, headers=get_token_headers).json()

token = r["access_token"] #наш токен

print('Токен: ' + token+'\n')

#вторая часть. Отправим запрос с токеном и методом "получить картинку", чтобы получить сгенерированную картинку заката

get_pic_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                   'Authorization': 'Bearer '+str(token)} #в заголовке указываем метод авторизации и наш токен

get_pic_URL = 'https://test.api.amadeus.com/v2/media/files/generated-photos' #URL уже содержит метод /media/files/generated-photos
get_pic_params = {'category': 'BEACH'} #генерить будем пляж 'BEACH'. еще можно горы 'MOUNTAIN'

get_pic = requests.get(get_pic_URL, headers = get_pic_headers, params = get_pic_params).json() #данне сразу переводим в json
pic_URL = get_pic['data']['attachmentUri'] #из словаря вытаскиваем ссылку на картинку

print('Ссылка на красивый пляж: '+ pic_URL)

