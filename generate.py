import sys
import random
import argparse
import pickle


def generate(model_file, seed, length, output_file):
    output = sys.stdout
    if output_file is not None:
        output = open(output_file, 'w')
    with open(model_file,'rb') as model:
        model_dict = pickle.load(model)
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

required = parser.add_argument_group('required arguments')

required.add_argument("--model", type=str, help="path to the model", required=True)
parser.add_argument("--seed", type=str, default=None, help="the first word")
required.add_argument("--length", type=int, help="length of the text", required=True)
parser.add_argument("--output", type=str, default=None, help="output file")
args = parser.parse_args()
generate(args.model, args.seed, args.length, args.output)
