import json
from pprint import pprint
from time import sleep

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

# Определение количества страниц для веб-скрапинга
headers_generator = Headers(os="win", browser="chrome")
url = f"https://spb.hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&order_by=publication_time&area=1&area=2&page=0"
response = requests.get(url, headers=headers_generator.generate())
html_data = response.text
soup = BeautifulSoup(html_data, 'lxml')
numbers = soup.findAll('span', class_='pager-item-not-in-short-range')
number = numbers[len(numbers) - 1].text

# Поиск вакансий по всем страницам, по фильтрам "django", "flask"
data = []
print("Количество страни:", number)
print("Поиск вакасий на странице")
for p in range(0, int(number)):
    print(p + 1, end=', ')
    url = f"https://spb.hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&order_by=publication_time&area=1&area=2&page={p}"
    sleep(1)
    headers_generator = Headers(os="win", browser="chrome")
    response = requests.get(url, headers=headers_generator.generate())
    html_data = response.text
    soup = BeautifulSoup(html_data, 'lxml')
    names = soup.findAll('div', class_='vacancy-serp-item__layout')
    for name in names:
        name_vacancy = name.find('span', class_='serp-item__title').text
        key_find = ["django", "flask"]
        for i in key_find:
            if i in name_vacancy.lower():
                link_vacancy = name.find('a', class_='bloko-link').get('href')
                company_vacancy = name.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                city_vacancy = name.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
                try:
                    compensation_vacancy = name.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    data.append([name_vacancy, link_vacancy, company_vacancy, city_vacancy, compensation_vacancy])
                except Exception:
                    data.append([name_vacancy, link_vacancy, company_vacancy, city_vacancy, 'нет суммы'])


# Запись в json файл
with open("vacancy.json", "w") as f:
    json.dump(data, f)

print("Поиск завершён, файл записан")