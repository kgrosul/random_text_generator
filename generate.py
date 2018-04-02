import sys
import random
import argparse


def get_dict(file_name):
    main_dict = dict()
    with open(file_name, 'r') as file:
        for line in file:
            word1, word2, frequency = line.rstrip().split()
            if word1 not in main_dict.keys():
                main_dict[word1] = dict()
            if word2 not in main_dict[word1].keys():
                main_dict[word1][word2] = 1
            else:
                main_dict[word1][word2] += 1
    return main_dict


def generate(model_file, seed, length, output_file):
    output = sys.stdout
    if output_file is not None:
        output = open(output_file, 'r')
    model_dict = get_dict(model_file)
    prev_word = ""
    text = ""
    if seed is not None:
        prev_word = seed
        text = prev_word
        length -= 1
    for i in range(length):
        if prev_word not in model_dict.keys():
            prev_word = random.choice(list(model_dict.keys()))
        else:
            tmp_list = []
            for key in model_dict[prev_word].keys():
                tmp_list += [key]*model_dict[prev_word][key]

            prev_word = random.choice(tmp_list)
        text += prev_word + ' '
    output.write(text)
    output.close()


parser = argparse.ArgumentParser(description=
                                 "Generates texts using model made by train.py.\t"
                                 "You can set length of the text, file contains model, "
                                 "output file and the the first word.")
parser.add_argument("--model", type=str, help="path to the model")
parser.add_argument("--seed", type=str, default=None, help="the first word")
parser.add_argument("--length", type=int, help="length of the text")
parser.add_argument("--output", type=str, default=None, help="output file")
args = parser.parse_args()
generate(args.model, args.seed, args.length, args.output)
