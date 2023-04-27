import openai
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel, pipeline
import requests
from statistics import mode
import requests
import prompting
import os


def gpt_35_turbo(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompting.prompt(args)}],
        n=n,
        temperature=args.temperature,
        stop="FINISH",
    )
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["message"]["content"]
        print("OUTPUT")
        print(output)
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def code_davinci_002(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    temperature = args.temperature
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompting.prompt(args),
        temperature=temperature,
        n=n,
        max_tokens=300,
        stop=["FINISH"],
        logprobs=5,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def text_davinci_003(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    temperature = args.temperature
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompting.prompt(args),
        temperature=temperature,
        n=n,
        max_tokens=300,
        stop=["FINISH"],
        logprobs=5,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def code_davinci_edit_001(args):
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"oai_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5

    temperature = args.temperature
    prompt = prompting.prompt(args) + " REPLACE"

    response = openai.Edit.create(
        model="code-davinci-edit-001",
        input=prompt,
        instruction="replace REPLACE with the explanation, an explanation dictionary and the final translation",
        temperature=temperature,
        top_p=1,
        n=n,
    )
    # print(response["choices"][0]["text"])
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["text"][len(prompt)-8:].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)


def bloom(args):
    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    headers = {"Authorization": "Bearer " + key}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    choices = []
    for i in range(0, n):
        raw_output = query(
            {
                "inputs": input_prompt,
                "options": {"use_cache": False, "wait_for_model": True},
                "parameters": {
                    "return_full_text": False,
                    "do_sample": False,
                    "max_new_tokens": 300,
                    "temperature": args.temperature,
                },
            }
        )
        # shots_count = input_prompt.count("FINISH")
        output = raw_output[0]["generated_text"].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)

def bloomz(args):
    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
    if args.keyfile != "":
        keyfile = args.keyfile
    else:
        keyfile = os.path.join(args.keydir,"hf_key.txt")
    key = open(keyfile).readline().strip("\n")
    if key == "":
        raise Exception("No key provided.")
    headers = {"Authorization": "Bearer " + key}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    choices = []
    for i in range(0, n):
        raw_output = query(
            {
                "inputs": input_prompt,
                "options": {"use_cache": False, "wait_for_model": True},
                "parameters": {
                    "return_full_text": False,
                    "do_sample": False,
                    "max_new_tokens": 300,
                    "temperature": args.temperature,
                },
            }
        )
        print("RAW OUTPUT")
        print(raw_output)
        # shots_count = input_prompt.count("FINISH")
        output = raw_output[0]["generated_text"].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)
