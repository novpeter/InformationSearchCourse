import json
import os
import tools
from tokenizer import Tokenizer
from spider import Spider
from inverted_index import InvertedIndexFactory
from boolean_search import BooleanSearch
from tf_idf_calculator import TF_IDF_Calculator
from vector_model_search import VectorModelSearch


def run_spider():
    spider = Spider(tools.BASE_URL, tools.NESTED_LINK_REGEXP)
    spider.start_parsing()


def run_tokenizer():
    input_directory_path = tools.TEXT_DOCUMENTS_PATH
    output_directory_path = tools.LEMMATIZED_TEXTS_PATH

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


def run_inverted_index():
    factory = InvertedIndexFactory(tools.LEMMATIZED_TEXTS_PATH, tools.INVERTED_INDEX_PATH)
    factory.make_inverted_index()
    print('Inverted index was created!')


def run_boolean_search():
    all_files_indexes = [filename[:-4] for filename in os.listdir(tools.LEMMATIZED_TEXTS_PATH)]

    bs = BooleanSearch(tools.INVERTED_INDEX_PATH, all_files_indexes)

    queries = {
        "байден & навальный | !путин",
        "байден & навальный | путин",
        "рецепт & вкусного & блина",
        "война & США | Россия",
        "политика & европа & санкции"
    }

    for query in queries:
        bs.search(query)


def run_tf_idf_calculator():
    all_filenames = os.listdir(tools.LEMMATIZED_TEXTS_PATH)

    with open(tools.INVERTED_INDEX_PATH) as json_file:
        inverted_index = json.load(json_file)

    result = {}

    for term in inverted_index.keys():
        docs_with_term = inverted_index[term]
        for doc_index in docs_with_term:
            lem_file_path = tools.LEMMATIZED_TEXTS_PATH + "/" + doc_index + ".txt"

            with open(lem_file_path, 'r') as file:
                tokens = file.read().split(' ')

            TF, IDF, TF_IDF = TF_IDF_Calculator.calculate(term,
                                                          tokens,
                                                          len(all_filenames),
                                                          len(docs_with_term))

            try:
                result[term][doc_index] = {"TF": TF, "IDF": IDF, "TF-IDF": TF_IDF}
            except KeyError:
                result[term] = {doc_index: {"TF": TF, "IDF": IDF, "TF-IDF": TF_IDF}}

    dump = json.dumps(result,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))

    tools.save_text_in_file(tools.TF_IDF_PATH, dump)


def search():
    vms = VectorModelSearch()
    vms.search("Россия не имела никакого отношения к каким-либо кампаниям против кандидатов на выборах")


if __name__ == '__main__':
    search()
