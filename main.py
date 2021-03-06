from spider import Spider


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    base_url = "https://ria.ru/"
    nested_link_regexp = "^https://ria.ru/"

    spider = Spider(base_url, nested_link_regexp)
    spider.start_parsing()
