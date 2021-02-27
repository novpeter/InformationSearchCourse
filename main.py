from spider import Spider


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    base_url = "https://www.povarenok.ru/recipes/"
    spider = Spider(base_url)
    spider.start_parsing()


