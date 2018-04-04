import sys
import argparse
import os
import pickle
import re


def file_train(main_dict, input_file, lowercase):
    text_file = sys.stdin
    if input_file is not None:
        text_file = open(input_file, 'r')

    for line in text_file:
        if lowercase:
            line = line.lower()

        words = re.findall(r'\w+', line)
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i+1]
            if word not in main_dict.keys():
                main_dict[word] = dict()

            if next_word not in main_dict[word]:
                main_dict[word][next_word] = 1
            else:
                main_dict[word][next_word] += 1

    text_file.close()


def train(input_dir, model_file, lowercase=False):
    main_dict = dict()
    if input_dir is None:
        file_train(main_dict, input_dir, lowercase)
    else:
        for file in os.listdir(input_dir):
            if file.endswith(".txt"):
                input_file = input_dir + "/" + str(file)
                file_train(main_dict, input_file, lowercase)

    with open(model_file, 'wb') as output:
        pickle.dump(main_dict, output)


parser = argparse.ArgumentParser(description=
                                 "Build model for generate.py using your text. "
                                 "You can set input file, file name for the model and "
                                 "should the text be lowercase or not")

required = parser.add_argument_group('required arguments')

parser.add_argument("--input-dir", type=str, default=None, help="path to the input directory")
required.add_argument("--model", type=str, help="path to to the model file",required=True)
parser.add_argument("--lc", action='store_true', default=False, help="converting text to the lower case")
args = parser.parse_args()

train(args.input_dir, args.model, args.lc)
