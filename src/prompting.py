import os
import ambiguity
from ltlf2dfa.parser.ltlf import LTLfParser
import ast


def parse_formulas(choices):
    parser = LTLfParser()
    parsed_result_formulas = []
    for c in choices:
        try:
            formula_str = c.split("FINAL:")[1].strip(".")
        except:
            # formula_str = c
            formula_str = ""

        try:
            parsed_formula = parser(formula_str)
            parsed_result_formulas.append(parsed_formula)
        except:
            parsed_result_formulas.append(formula_str)
    return parsed_result_formulas


def parse_explanation_dictionary(choices, nl):
    parsed_explanation_results = []
    for c in choices:
        try:
            dict_string = (
                "{" + c.split("dictionary")[1].split("{")[1].split("}")[0] + "}"
            )
            parsed_dict = ast.literal_eval(dict_string)
            parsed_dict = dict(filter(lambda x: x[0] != nl, parsed_dict.items()))
            if parsed_dict:
                parsed_explanation_results.append(parsed_dict)
        except:
            pass
    return parsed_explanation_results


def generate_intermediate_output(intermediate_translation):
    nl = []
    ltl = []
    cert = []
    locked = []
    for t in intermediate_translation:
        nl.append(t[0])
        ltl.append(t[1])
        cert.append(t[2])
        locked.append(t[3])
    return [nl, ltl, cert, locked]


def prompt(args):
    inpt = args.nl
    prompt_dir = os.path.join("..", "prompts")
    if args.prompt == "minimal":
        fixed_prompt_file = open(os.path.join(prompt_dir, "minimal.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "smart":
        fixed_prompt_file = open(os.path.join(prompt_dir, "smart.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "stl":
        fixed_prompt_file = open(os.path.join(prompt_dir, "stl.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "indistribution":
        fixed_prompt_file = open(os.path.join(prompt_dir, "indistribution.txt"))
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "amba_master":
        fixed_prompt_file = open(
            os.path.join(prompt_dir, "amba_master_assumptions.txt")
        )
        fixed_prompt = fixed_prompt_file.read()
    elif args.prompt == "amba_slave":
        fixed_prompt_file = open(os.path.join(prompt_dir, "amba_slave_guarantees.txt"))
        fixed_prompt = fixed_prompt_file.read()
    else:
        fixed_prompt = args.prompt
    final_prompt = (
        fixed_prompt
        + "\nNatural Language: "
        + inpt
        + "\nGiven translation:"
        + args.given_translations
        + "\nExplanation:"
    )
    print("FINAL PROMPT:")
    print(final_prompt)
    return final_prompt


def extract_subinfo(choices, args, n):
    parsed_result_formulas = parse_formulas(choices)
    print("Results of multiple runs:")
    print(parsed_result_formulas)
    final_translation = ambiguity.ambiguity_final_translation(parsed_result_formulas, n)
    parse_explain = parse_explanation_dictionary(choices, args.nl)
    intermediate_translation = ambiguity.ambiguity_detection_translations(
        parse_explain,
        n,
        ast.literal_eval(args.locked_translations)
        if "locked_translations" in args
        else {},
    )
    intermediate_output = generate_intermediate_output(intermediate_translation)
    return final_translation, intermediate_output
