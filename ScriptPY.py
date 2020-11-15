#!/usr/bin/python3


from selenium import webdriver
import pymysql

print('Погнали...  0%')                # Подключение к БД
con = pymysql.connect('localhost',     # Адрес          
                      'root',          # Логин
                      '******',          # Пароль
                      'First')         # Название БД

cur = con.cursor()
cur.execute("SELECT * FROM Tabl1")       # Выбор таблицы

driver = webdriver.Firefox(executable_path='/home/dimax/Документы/geckodriver')   # Драйвер для Mozila
driver.get("https://yandex.com/news/")                               # Сайт откуда берем информацию

allnews = driver.find_elements_by_xpath('//a[@class="news-card__link"]')
print('25%')
row = cur.fetchall()
news = []
href = []
for i in allnews:                       # Данный цикл отсеивает повторения и записывает нужные данные в списки
    k = 0
    for a in range(cur.rowcount):
        if str(row[a][1]) == str(i.text):
            k += 1
    if k == 0:
        news.append(i.text)
        href.append(i.get_attribute('href'))

driver.quit()
print('75%')
for h in range(len(news)):
    sql = """INSERT INTO `Tabl1` (`id`, `news`, `href`) VALUES (NULL, '{first}', # Данный цикл записывает данные из списков в таблицу в БД
     '{second}')""".format(first=news[h], second=href[h])
    cur.execute(sql)
    con.commit()
print('Готово  100%')
