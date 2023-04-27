import backend
import numpy as np
import argparse
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(
                        prog = 'nl2spec',
                        description = 'Translates natural language to LTL formulas',
                        epilog = 'Beta. If encountering problems, please contact hahn@cs.stanford.edu')

    parser.add_argument('--model', required=False, default="gpt-3.5-turbo", help='chose the deep learning model')
    parser.add_argument('--keyfile', required=False, default="", help='provide open ai key (for codex usage), or a huggingface api key (for bloom usage)')
    parser.add_argument('--prompt', required=False, default="minimal", help='secifies the name of the promptfile')
    parser.add_argument('--num_tries', required=False, default=3, help="Number of runs the underlying language model attempts a translation.")
    parser.add_argument('--temperature', required=False, default=0.2, type=float, help="Model temperature.")
    args = parser.parse_args()
    return args

def get_dataset():
    f = open("../examples.csv")
    f.readline()
    NL_list = []
    label_list = []
    for line in f:
        NL_data,label = line.split(";")
        NL_list.append(NL_data)
    return NL_list, label_list

def get_next_given_translation(backend_res):
    final_translation = backend_res[0]
    intermediate_output = backend_res[1] #NL, F, confidence
    NL_list = intermediate_output[0]
    T_list = intermediate_output[1]
    confidence_list = intermediate_output[2]
    next_given_translations = {}
    for i in range(len(NL_list)):
        NL_key = NL_list[i]
        formal_translation = T_list[i][np.argmax(confidence_list[i])]
        next_given_translations[NL_key] = formal_translation
    return next_given_translations

def get_final_translation(backend_res):
    return backend_res[0]

def call_backend(nl,model,keyfile,prompt):
    call_args = {
        "model":model,
        "nl":nl,
        "fewshots":"",
        "keyfile":keyfile,
        "prompt":prompt,
        "maxtokens":64,
        "given_translations":"",
        "num_tries":3,
        "temperature":0.2,
    }
    call_args = argparse.Namespace(**call_args)
    res = backend.call(call_args)
    return res

def display_results(NL_list,label_list,predictions):
    tab_dict = {"input":NL_list,"label":label_list,"predictions":predictions}
    print(tabulate(tab_dict,headers="keys"))

def main():
    NL_list, label_list = get_dataset()
    
    #print(NL_list)
    #args = parser.parse_args()
    args = parse_args()
    predictions = []
    for nl in NL_list:
        res = call_backend(nl,model=args.model,keyfile=args.keyfile,prompt=args.prompt)
        predictions.append(get_final_translation(res))
    
    display_results(NL_list,label_list,predictions)

if __name__ == "__main__":
    main()
