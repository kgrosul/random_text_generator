import sys
import argparse
import os
import pickle
import re
import collections


def normalize(model_dict):
    """Функция нормирует вероятности в словаре model_dict"""
    for prev_words in model_dict.keys():
        """
        word_occurrences_sum = количество вхождений в текст
        пары <набор слов - prev_words><следующее слово - next_word>
        """
        word_occurrences_sum = sum(model_dict[prev_words].values())
        for next_word in model_dict[prev_words].keys():
            model_dict[prev_words][next_word] /= word_occurrences_sum


def file_train(model_dict, input_file, words_num, lowercase):
    """
    Функция построчно считывает текст из заданного файла.
    Каждая строка разбивается при необходимосто приводится
    к lowercase, затем разбивается на слова, состоящие только
    из алфавитных символов. Для каждо подстроки вида
    <слово1><слово2>...<cловоN> для каждого слова, следующего
    за подстрокой считается число раз, которое оно встречается
    и добавляется в модель.

    file_train(model_dict, input_file, words_num, lowercase)

    model_dict: словарь, содержащий модель
    input_file: файл с текстом
    words_num: количество слов,
                    на основании которых выбирается следующее
    lowercase: надо ли приводить к lowercase

    """

    text_file = sys.stdin
    if input_file is not None:
        text_file = open(input_file, 'r')

    words_list = []
    for line in text_file:
        if lowercase:
            line = line.lower()

        words = re.findall(r'\w+', line)
        for i in range(len(words) - 1):
            words_list.append(words[i])
            next_word = words[i+1]
            if len(words_list) < words_num:
                continue
            words_tuple = tuple(words_list)
            model_dict[words_tuple][next_word] += 1
            words_list.pop(0)

    text_file.close()


def train(input_dir, model_file, words_num, lowercase=False):
    """
    Для каждого файла в заданной директории вызывается функция
    file_train, которая дополняет модель.
    Модель представляется в виде словаря словарей, где первый
    ключ - набор слов длины word_num, второй - одно слово,
    значение - количество вхождений в данный текст.
    В конце модель записывается в заданный файл с помощью
    модулюя pickle

    train(input_dir, model_file, words_num, lowercase=False)

    input_dir: директория, где лежат тексты
    model_file: файл, где хранится модель
    words_num: количество слов,
                    на основании которых выбирается следующее
    lowercase: приводить ли к lowercase, default = False

    """

    model_dict = collections.defaultdict(lambda: collections.defaultdict(int))

    if input_dir is None:
        file_train(model_dict, input_dir, words_num, lowercase)
    else:
        for file in os.listdir(input_dir):
            if file.endswith(".txt"):
                input_file = input_dir + "/" + str(file)
                file_train(model_dict, input_file, words_num, lowercase)

    normalize(model_dict)

    with open(model_file, 'wb') as output:
        pickle.dump(dict(model_dict), output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Build model for generate.py using your texts. "
                    "You can set input directory, file name for the model,"
                    "n in n-gramm and should the text be lowercase or not")

    required = parser.add_argument_group('required arguments')

    parser.add_argument("--input-dir",
                        type=str,
                        default=None,
                        help="path to the input directory"
                        )

    required.add_argument("--model",
                          type=str,
                          help="path to to the model file",
                          required=True
                          )

    parser.add_argument("--lc",
                        action='store_true',
                        default=False,
                        help="converting text to the lower case"
                        )

    parser.add_argument("--words-num",
                        type=int,
                        default=1,
                        help="length of a Markov chain"
                        )

    args = parser.parse_args()
    train(args.input_dir, args.model, args.words_num, args.lc)
