import argparse
import time

import numpy as np
from ltlf2dfa.parser.ltlf import LTLfParser
from tabulate import tabulate

import backend

# import spot


def parse_args():
    parser = argparse.ArgumentParser(
        prog="nl2spec",
        description="Translates natural language to LTL formulas",
        epilog="Beta. If encountering problems, please contact hahn@cs.stanford.edu",
    )

    parser.add_argument(
        "--model",
        required=False,
        default="gpt-3.5-turbo",
        help="chose the deep learning model",
    )
    parser.add_argument(
        "--keyfile",
        required=False,
        default="",
        help="provide open ai key (for codex usage), or a huggingface api key (for bloom usage)",
    )
    parser.add_argument(
        "--keydir",
        required=False,
        default="../keys/",
        help="if not specify keyfile, specify directory",
    )
    parser.add_argument(
        "--prompt",
        required=False,
        default="minimal",
        help="secifies the name of the promptfile",
    )
    parser.add_argument(
        "--num_tries",
        required=False,
        default=3,
        type=int,
        help="Number of runs the underlying language model attempts a translation.",
    )
    parser.add_argument(
        "--temperature",
        required=False,
        default=0.2,
        type=float,
        help="Model temperature.",
    )
    parser.add_argument(
        "--teacher_model",
        required=False,
        default="",
        help="chose the deep learning model to render the subtranslations for the student model (see teacher student experiment in the nl2spec paper)",
    )
    parser.add_argument(
        "--datafile",
        required=False,
        default="",
        help="specify dataset file",
    )

    parser.add_argument(
        "--smoke",
        required=False,
        default=False,
        action="store_true",
        # type=bool,
        help="set to run smoke test",
    )
    parser.add_argument(
        "--wait",
        required=False,
        default=0,
        type=int,
        help="Wait a specified amount of time (s) after each sample to stay below rate limits",
    )

    args = parser.parse_args()
    return args


def get_dataset(datafile):
    if datafile == "":
        f = open("../datasets/expert_LTL_dataset.txt")
        f.readline()
        NL_list = []
        label_list = []
        for line in f:
            NL_data, label = line.split(";")
            NL_list.append(NL_data)
            parser = LTLfParser()
            label_list.append(str(parser(label)))
        return NL_list, label_list, None
    elif datafile == "codex-initial":
        f = open("../experiments/codex-initial_predictions.txt")
        f.readline()
        NL_list = []
        label_list = []
        subtranslation_list = []
        for line in f:
            NL_data, label, final_pred, subtranslations = line.split(";")
            NL_list.append(NL_data)
            parser = LTLfParser()
            label_list.append(str(parser(label)))
            subtranslation_list.append(subtranslations)
        return NL_list, label_list, subtranslation_list
    elif datafile == "gpt-3.5-turbo-interactive":
        f = open("../experiments/gpt-3.5-turbo-interactive_predictions.txt")
        f.readline()
        NL_list = []
        label_list = []
        subtranslation_list = []
        for line in f:
            NL_data, label, final_pred, subtranslations = line.split(";")
            NL_list.append(NL_data)
            parser = LTLfParser()
            label_list.append(str(parser(label)))
            subtranslation_list.append(subtranslations)
        return NL_list, label_list, subtranslation_list
    else:
        raise


def get_next_given_translations(backend_res):
    final_translation = backend_res[0]
    intermediate_output = backend_res[1]  # NL, F, confidence
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
    return str(backend_res[0][0]).strip("\n")


def call_backend(
    nl,
    model,
    prompt,
    num_tries,
    temperature,
    keyfile="",
    keydir="",
    given_translations="",
    **kwargs
):
    call_args = {
        "model": model,
        "nl": nl,
        "fewshots": "",
        "keyfile": keyfile,
        "keydir": keydir,
        "prompt": prompt,
        "maxtokens": 64,
        "given_translations": given_translations,
        "num_tries": num_tries,
        "temperature": temperature,
    }
    call_args = argparse.Namespace(**call_args)
    res = backend.call(call_args)
    return res


def display_results(NL_list, label_list, predictions, correct_list):
    tab_dict = {
        "input": NL_list,
        "label": label_list,
        "predictions": predictions,
        "correct": correct_list,
    }
    print(tabulate(tab_dict, headers="keys"))


def main():
    args = parse_args()
    NL_list, label_list, subtranslation_list = get_dataset(args.datafile)
    predictions = []
    if not args.smoke:
        num_examples = len(NL_list)
    else:
        num_examples = 2
    for i in range(num_examples):
        if args.wait != 0:
            time.sleep(args.wait)
        nl = NL_list[i]
        if subtranslation_list is not None:
            given_sub_translations = subtranslation_list[i]
        elif args.teacher_model != "":
            teacher_dict = vars(args).copy()
            teacher_dict["model"] = args.teacher_model
            res = call_backend(nl, **teacher_dict)
            given_sub_translations = str(get_next_given_translations(res))
            print("TEACHER SUB TRANSLATIONS")
            print(given_sub_translations)
        else:
            given_sub_translations = ""

        res = call_backend(nl, **vars(args), given_translations=given_sub_translations)
        predictions.append(get_final_translation(res))

    parser = LTLfParser()
    correct_list = []
    for i in range(len(predictions)):
        try:
            label = parser(label_list[i])
            pred = parser(predictions[i])
            # label = spot.formula(str(label_list[i]))
            # pred = spot.formula(str(predictions[i]))
            if label == pred:
                correct_list.append(1)
            else:
                correct_list.append(0)
        except Exception as e:
            correct_list.append(0)

    display_results(NL_list, label_list, predictions, correct_list)
    accuracy = np.mean(correct_list)
    print("ACCURACY:", accuracy)
    if args.smoke:
        print("backend smoke test success")
    if args.datafile != "":
        save_name = (
            "results-nl2spec_subtranslation-"
            + args.datafile
            + "_model-"
            + args.model
            + "_prompt-"
            + args.prompt
        )
    elif args.teacher_model != "":
        save_name = (
            "results-nl2spec_teacher-"
            + args.teacher_model
            + "_student-"
            + args.model
            + "_prompt-"
            + args.prompt
        )
    else:
        save_name = (
            "results-nl2spec_model-"
            + args.model
            + "_prompt-"
            + args.prompt
            + "_initial"
        )

    NL_list.insert(0, "input")
    label_list.insert(0, "label")
    predictions.insert(0, "prediction")
    correct_list.insert(0, "correct")
    np.savetxt(
        save_name + ".txt",
        [p for p in zip(NL_list, label_list, predictions, correct_list)],
        delimiter=";",
        fmt="%s",
    )
    np.savetxt(save_name + ".accuracy", [accuracy])


if __name__ == "__main__":
    main()
