import json
import operator
import os
import tools

from sklearn.metrics.pairwise import cosine_similarity
from tokenizer import Tokenizer
from tf_idf_calculator import TF_IDF_Calculator


def dist_cosine(vecA, vecB):
    cosine = cosine_similarity([vecA], [vecB])
    return cosine[0][0]


class VectorModelSearch:

    def __init__(self):
        self.__tokenizer = Tokenizer()
        self.__all_docs_count = len(os.listdir(tools.LEMMATIZED_TEXTS_PATH))

        with open(tools.INDEX_PATH) as json_file:
            self.__indices = json.load(json_file).keys()

        with open(tools.TF_IDF_PATH) as json_file:
            self.tf_idf_calculations = json.load(json_file)

    def search(self, query):
        tokens = self.__tokenizer.clean_text(query)
        query_vector = []

        for token in tokens:
            doc_with_terms_count = len(self.tf_idf_calculations[token])
            _, _, tf_idf = TF_IDF_Calculator.calculate(token,
                                                       tokens,
                                                       self.__all_docs_count,
                                                       doc_with_terms_count)
            query_vector.append(tf_idf)

        distances = {}

        for index in self.__indices:
            document_vector = []

            for token in tokens:
                try:
                    tf_idf = self.tf_idf_calculations[token][index]["TF-IDF"]
                    document_vector.append(tf_idf)
                except KeyError:
                    document_vector.append(0.0)

            distances[index] = dist_cosine(query_vector, document_vector)

        searched_index = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
        print(searched_index)