from bs4 import BeautifulSoup
from bs4.element import Comment

import os
import shutil
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_html(url):
    """
    Возвращает HTML документ по переданному URL
    :param url: URL сайта
    :return: HTML документ
    """
    response = urllib.request.urlopen(url)
    return response.read()


def get_nested_links(soup):
    """
    Возвращает массив вложенных ссылок
    """
    links = [item['href'] for item in soup]
    return links


class Spider:

    def __init__(self,
                 base_url,
                 max_pages_count=100,
                 min_words_count=1000,
                 output_directory="output/",
                 output_filename="index.txt"):
        """
        Конструктор
        :param base_url: Базовый URL, с которого начинается работа краулера
        :param max_pages_count: Максимальное количество обработанных страниц
        :param min_words_count: Минимальное кол-во слов на странице
        :param output_directory: Директория для сохранения документов
        :param output_filename: Имя файла, в который записывается индекс страницы и ее URL
        """
        self.__base_url = base_url
        self.__max_pages_count = max_pages_count
        self.__min_words_count = min_words_count
        self.__current_page_index = 0
        self.__output_directory = output_directory
        self.__output_filename = output_filename

    def start_parsing(self):
        """ Производит парсинг с начальный страницы """
        self.__prepare_output_directory()
        base_html = get_html(self.__base_url)
        self.__parse(self.__base_url, base_html)

    def __prepare_output_directory(self):
        """ Очищает папку output от файлов предыдущего запуска """
        try:
            shutil.rmtree(self.__output_directory)
            os.mkdir(self.__output_directory)
        except OSError:
            print("Creation of the directory %s failed" % self.__output_directory)
        else:
            print("Successfully created the directory '%s' " % self.__output_directory)

    def __parse(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')

        if self.check_text_size(soup):
            self.__save_html(self.__current_page_index, url, html)
            self.__current_page_index = + 1

        if self.__current_page_index >= self.__max_pages_count:
            return

        nested_links = get_nested_links(soup)

        for nested_link in nested_links:
            nested_html = get_html(nested_link)
            self.__parse(nested_link, nested_html)

            if self.__current_page_index >= self.__max_pages_count:
                return

    def check_text_size(self, soup):
        """
        Проверяет количество слов на странице
        :return: True, если слов не меньше self.__min_words_count
        """
        size = len(soup.text.split())
        return size >= self.__min_words_count

    def __save_html(self, index, url, html):
        """
        Созхраняет переданный HTML документ и
        добавляет в таблицу URL с индексом
        :param index: Индекс страницы
        :param index: URL страницы
        :param html: HTML документ
        """

        html_filename_path = self.__output_directory + str(index) + ".txt"
        html_file = open(html_filename_path, "wb")
        html_file.write(html)
        html_file.close()

        output_filename_path = self.__output_directory + self.__output_filename

        with open(output_filename_path, 'a') as file:
            line = str(index) + " – " + url
            file.write(line)
