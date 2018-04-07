import sys
import random
import argparse
import pickle
import numpy


MAX_WORDS_NUM = 1000  # константа, отвечающая за макс. кол-во слов в памяти


def generate(model_file, seed, length, output_file):

    """
    функция получает модель, построенную train.py или wikitrain.py и
    на основе ее строит текст.

    model_file: путь к модели
    seed: первое слово
    length: длина текста
    output_file: путь к файлу, в который осуществляется запись текста

    """
    output = sys.stdout
    if output_file is not None:
        output = open(output_file, 'r')

    with open(model_file, 'rb') as model:
        model_dict = pickle.load(model)

    first_words = []
    if seed is not None:
        for element in model_dict.keys():
            if element[0] == seed:
                first_words += [element]
    if len(first_words) == 0:
        first_words = list(model_dict.keys())

    cur_words = random.choice(first_words)
    text = ' '.join(cur_words) + ' '
    for i in range(length-len(cur_words)):
        if cur_words not in model_dict.keys():
            """
            Если необходимого набора слов нет в ключах словаря из модели,
            то за новый набор возьмем его случайный ключ, а за новое слово -
            последнее слово данного набора.
            """
            cur_words = random.choice(list(model_dict.keys()))
        else:
            tmp_words = []
            tmp_p = []
            for key in model_dict[cur_words].keys():
                tmp_words += [key]
                tmp_p += [model_dict[cur_words][key]]

            cur_words = cur_words[1:] + (numpy.random.choice(tmp_words,
                                                             p=tmp_p
                                                             ),)
        text += cur_words[-1] + ' '
        if (i + 1) % MAX_WORDS_NUM == 0:
            """
            Если в переменной text уже достаточно много
            слов(а именно MAX_WORDS_NUM), выведем их в файл,
            а значение text обнулим
            """
            output.write(text)
            text = ''
    output.write(text)
    output.close()


if __name__ == '__main__':
    help(generate)
    parser = argparse.ArgumentParser(
        description="Generates texts using model made by train.py."
                    "You can set length of the text, file contains model, "
                    "output file and the the first word.")

    required = parser.add_argument_group('required arguments')

    required.add_argument("--model",
                          type=str,
                          help="path to the model",
                          required=True
                          )

    parser.add_argument("--seed",
                        type=str,
                        default=None,
                        help="the first word"
                        )

    required.add_argument("--length",
                          type=int,
                          help="length of the text",
                          required=True
                          )

    parser.add_argument("--output",
                        type=str,
                        default=None,
                        help="output file"
                        )

    args = parser.parse_args()
    generate(args.model, args.seed, args.length, args.output)
