import wikipedia
from train import file_train
from train import normalize
from train import defaultdict_to_dict
import argparse
import pickle
import collections


def wiki_train(model_file, texts_num, words_num, lowercase=False):
    """

    :param model_file: файл для хранения модели
    :param texts_num: количество текстов
    :param words_num: количество слов, на основании которых выбирается следующее
    :param lowercase: приводить ли к lowercase

    Функция строит модель используя texts_num(количество) случайно
    найденных в Википедии текстом. Для доступа к Википедии используется
    модуль wikipedia.

    """

    file = open(model_file, 'w')
    for i in range(texts_num):
        file.write(wikipedia.page(wikipedia.search(wikipedia.random())[-1]).content)
    file.close()
    main_dict = collections.defaultdict(
        lambda: collections.defaultdict(lambda: 0))
    file_train(main_dict, model_file, words_num, lowercase)
    normalize(main_dict)
    main_dict = defaultdict_to_dict(main_dict)

    with open(model_file, 'wb') as output:
        pickle.dump(main_dict, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     "Build model for generate.py using random texts from Wikipedia. "
                                     "You can set model file name, number of texts,"
                                     "n in n-gramm and should the text be lowercase or not")

    required = parser.add_argument_group('required arguments')

    parser.add_argument("--texts-num", type=int, default=1,help="number of texts from Wikipedia")
    required.add_argument("--model", type=str, help="path to to the model file", required=True)
    parser.add_argument("--lc", action='store_true', default=False, help="converting text to the lower case")
    parser.add_argument("--words-num", type=int, default=1, help="length of a Markov chain")
    args = parser.parse_args()

    wiki_train(args.model, args.texts_num, args.words_num, args.lc)
