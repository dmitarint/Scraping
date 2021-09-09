import scrapy
from scrapy.http import HtmlResponse
import re
import json
from copy import deepcopy
from urllib.parse import urlencode
from insta.items import InstaItem

"""
1) Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей и собирать данные об их подписчиках и подписках. 
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь имя, id, фото (остальные данные по желанию). Фото можно дополнительно скачать.
3) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
________________________________________
Для выполненя данной работы необходимо делать запросы в апи инстаграм с указанием заголовка User-Agent : 'Instagram 155.0.0.37.107'
"""


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    instagram_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    with open("pass") as file:
        _file = [row.strip() for row in file]
        instagram_login = _file[0]
        instagram_password = _file[1]
    user_parse = ['ai_machine_learning', 'nirvana.all.apologies']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    query_posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    users_followers_following = ['followers', 'following']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.instagram_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.instagram_login,
                                           'enc_password': self.instagram_password,
                                           # 'queryParams': '{}',
                                           # 'optIntoOneTap': 'false',
                                           # 'stopDeletionNonce': '',
                                           # 'trustedDeviceRecords': '{}'
                                           },
                                 headers={'x-csrftoken': csrf})


    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            # !!!! здесь добавить цикл, где проходимся по юзерам
            for user in self.user_parse:
                yield response.follow(f'/{user}',
                                      callback=self.user_follow,
                                      cb_kwargs={'username': user})



    def user_follow(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        for fol in self.users_followers_following:
            yield response.follow(f'https://i.instagram.com/api/v1/friendships/{user_id}/{fol}/?count=12',
                                  callback=self.user_data_parse,
                                  cb_kwargs={'username': deepcopy(username),
                                             'user_id': deepcopy(user_id),
                                             'user_type': fol})

    def user_data_parse(self, response:HtmlResponse, username, user_id, user_type):
        j_data = response.json()
        if j_data.get('next_max_id'):
            max_id = j_data.get('next_max_id')
            for fol in self.users_followers_following:
                yield response.follow(f'https://i.instagram.com/api/v1/friendships/{user_id}/{fol}/?count'
                                      f'=12&max_id={max_id}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': deepcopy(username),
                                                 'user_id': deepcopy(user_id),
                                                 'user_type': type})
        for uid in j_data.get('users'):
            print()
            item = InstaItem(user_id=user_id,
                                   user_fullname=username,
                                   subuser_type=user_type,
                                   subuser_id=uid.get('pk'),
                                   subuser_fullname=uid.get('full_name'),
                                   subuser_link_to_pic=uid.get('profile_pic_url'))
            yield item


    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')