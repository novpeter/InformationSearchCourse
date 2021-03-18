import nltk
import re

from nltk.corpus import stopwords
from pymystem3 import Mystem


class Tokenizer:

    def clean_text(self, text):
        tokens = self.__tokenize(text)
        tokens = self.__lemmatize(tokens)
        tokens = self.__remove_stop_words(tokens)
        tokens = self.__convert_to_lowercase(tokens)
        tokens = self.__remove_numbers(tokens)
        tokens = self.__remove_empty_strings(tokens)

        return tokens

    def __tokenize(self, text):
        """ Делит текст на токены """
        tokens = nltk.word_tokenize(text)

        return tokens

    def __lemmatize(self, tokens):
        """ С помощью Mystem лематизирует токены """
        mystem = Mystem()

        tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]

        return tokens

    def __remove_stop_words(self, tokens):
        """ Удаляет лишние символы """
        tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]

        stop_words = stopwords.words('russian')
        only_cyrillic_letters = re.compile('[а-яА-Я]')

        tokens = [token for token in tokens if (token not in stop_words) and only_cyrillic_letters.match(token)]

        return tokens

    def __convert_to_lowercase(self, tokens):
        """ Приводит токены к нижнему регистру """
        tokens = [token.lower() for token in tokens]

        return tokens

    def __remove_numbers(self, tokens):
        """ Удаляет числа """
        tokens = [''.join([i for i in token if not i.isdigit()]) for token in tokens]

        return tokens

    def __remove_empty_strings(self, tokens):
        """ Удаляет пустые строки """
        tokens = [i for i in tokens if (i != '')]

        return tokens