# Задание
#
# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле,
# название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию
# о времени скачивания каждого изображения и общем времени выполнения программы.

from asyncio import ensure_future, gather, run
import sys
from time import time
from bs4 import *
import requests
import os

tasks = []
urls = ['https://yandex.ru/images',
        'https://vk.com/',
        'https://gb.ru/', ]


async def download_images(url):
    url_start_time = time()
    folder_name = 'async_' + 'images_' + url.replace('https://', '').replace('.', '_').replace(
        '/', '_')
    if os.path.isdir(folder_name):
        pass
    else:
        os.mkdir(folder_name)

    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    images = soup.findAll('img')
    if len(images) != 0:
        for i, image in enumerate(images):
            start_time_img = time()
            try:
                image_link = image["data-srcset"]
            except:
                try:
                    image_link = image["data-src"]
                except:
                    try:
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            image_link = image["src"]

                        except:
                            pass
            try:
                file_name = image_link.split('/')
                file_name = file_name[-1].replace('?', '').replace('=', '')
                if len(file_name) > 20:
                    file_name = file_name[:20]

                image_request = requests.get(image_link).content
                try:
                    image_request = str(image_request, 'utf-8')

                except UnicodeDecodeError:

                    with open(f"{folder_name}/{file_name}.jpg", "wb+") as f:
                        f.write(image_request)
                    print(f"Downloaded {file_name}.jpg in {time() - start_time_img:.2f} seconds")
            except:
                pass
        print(f"Downloaded {url} in {time() - url_start_time:.2f} seconds")


async def main(urls):
    for url in urls:
        task = ensure_future(download_images(url))
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    # Расскоментировать для ввода URL-адресов через аргументы командной строки
    # urls = sys.argv
    run(main(urls))
