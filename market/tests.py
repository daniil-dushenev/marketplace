from django.test import TestCase
from .models import Item, Images

from bs4 import BeautifulSoup
import requests


class YourTestClass(TestCase):
    response = requests.get(input('Вставьте ссылку на страницу с товарами из сайта Lamoda:'))
    page = BeautifulSoup(response.text, 'html.parser')
    links = ''
    urls = []
    for link in page.find_all('a', class_=['products-list-item__link', 'link']):
        links += str(link.get('href')) + '\n'
    links = links[300:]
    urls = (links[links.find('None'):links.find('/track/')].replace('None\n', '')).split('\n')

    for url in urls:
        response = requests.get('https://www.lamoda.ru' + url)
        page = str(BeautifulSoup(response.text, 'html.parser'))
        html = page[page.find('d.product'):page.find('d.product') + 800]

        brand = html[html.find('name') + 7:]
        brand = brand[:brand.find(',') - 1]

        price = html[html.find('current') + 10:]
        price = price[:price.find(',') - 1]

        html = page[page.find('d.product') - 565:page.find('d.product')]
        category = html[html.find('title') + 8:]
        category = category[:category.find(',') - 1]

        html = page[page.find('d.product'):page.find('d.product') + 800]

        sec_category = html[html.find('category') + 11:]
        sec_category = sec_category[:sec_category.find(',') - 1]

        color = html[html.find('color') + 8:]
        color = color[:color.find(',') - 1]

        name = sec_category + ' ' + brand

        item = Item.objects.create(
            brand=brand,
            price=price,
            category=category,
            sec_category=sec_category,
            color=color,
            name=name,
            lamoda_id=url[24:36],
            img_count=0
        )
        images = html[html.find('images') + 10:]
        images = images[:images.find(']') - 1].split('","')
        Images.objects.create(image='https://a.lmcdn.ru/img600x866' + images[0], is_active=1, count=item.id)
        images.remove(images[0])
        for link in images:
            link = 'https://a.lmcdn.ru/img600x866' + link
            Images.objects.create(
                image=link,
                is_active=0,
                count=item.id
            )