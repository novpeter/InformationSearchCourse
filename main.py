import os
import tools
from tokenizer import Tokenizer
from spider import Spider


def run_spider():
    base_url = "https://ria.ru/"
    nested_link_regexp = "^https://ria.ru/"

    spider = Spider(base_url, nested_link_regexp)
    spider.start_parsing()


def run_tokenizer():
    input_directory_path = "output/text_documents"
    output_directory_path = "output/lematized_texts"

    all_files = os.listdir(input_directory_path)
    tools.prepare_output_directory(output_directory_path)

    tokenizer = Tokenizer()

    for filename in all_files:
        input_file_path = input_directory_path + '/' + filename
        with open(input_file_path, 'r') as file:
            text = file.read().replace('\n', '')
            cleaned_text = tokenizer.clean_text(text)
            output_file_path = output_directory_path + '/' + filename
            tools.save_text_in_file(output_file_path, ' '.join(cleaned_text))
            print('Done %s' % filename)

    print('Done')


if __name__ == '__main__':
    # run_spider()
    run_tokenizer()
