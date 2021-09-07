"""
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
 и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!?
________________________________________
2) Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
 Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

"""
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#  Загружаем селениум и в него подгружаем сайт мэйл
firefox_options = Options()
firefox_options.add_argument('maximize_window')
driver = webdriver.Firefox(executable_path='./geckodriver.exe')
driver.maximize_window()
driver.get('https://mail.ru/')

#  Вводим логин
login = driver.find_element_by_name('login')
login.send_keys('study.ai_172')

#  Выбираем домен
domain = driver.find_element_by_name('domain')
select = Select(domain)
select.select_by_value('@mail.ru')

#  Жмем кнопку "ввести пароль"
password_button = driver.find_element_by_xpath("//button[contains(text(),'Ввести пароль')]")
password_button.click()

#  Вводим пароль
password = driver.find_element_by_xpath("//input[@type='password']")
password.send_keys('NextPassword172!?')

#  Заходим на почту
enter = driver.find_element_by_xpath("//button[@type='button'][contains(text(),'Войти')]")
enter.click()

time.sleep(3)
actions = ActionChains(driver)
letters_list = []
while True:
    letters = None
    letters = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    for letter in letters:
        letter_link = letter.get_attribute('href')
        if letter_link not in letters_list:
            letters_list.append(letter_link)
    actions.move_to_element(letters[0]).send_keys(Keys.PAGE_DOWN)
    actions.perform()
    time.sleep(0.5)

#Дошел до этого момента. Но 16.08. сменился пароль от ящика, продолжить не смог


    # driver.execute_script("window.scrollTo(0, 900)")

    # driver.execute_script("window.scrollTo(0, Y)")
    # last = driver.find_element_by_class_name('llc_last')
    # actions.move_to_element(last)
    # actions.perform()
    # for i in range(20):
    #     actions.send_keys(Keys.ARROW_DOWN)
    #     actions.perform()
    # print()

