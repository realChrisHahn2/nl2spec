import openai
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel, pipeline
import requests
from statistics import mode
import requests
import prompting

def gpt35(args):
    key = open(args.keyfile).readline()
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
    messages = [{"role":"user", "content": prompting.prompt(args)}],
    n = n,
    temperature = args.temperature,
    stop="FINISH"
    )
    choices = []
    for i in range(0, n):
        output = response["choices"][i]["message"]["content"]
        print("OUTPUT")
        print(output)
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)

def codex(args):
    key = open(args.keyfile).readline()
    if key == "":
        raise Exception("No key provided.")
    openai.api_key = key
    if args.num_tries == "":
        n = 3
    else:
        n = int(args.num_tries)
        if n > 5:
            n = 5
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompting.prompt(args),
        temperature=args.temperature,
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


def bloom(args):
    n = args.num_tries
    input_prompt = prompting.prompt(args)
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    key = open(args.keyfile).readline()
    if key == "":
        raise Exception("No key provided.")
    headers = {"Authorization": "Bearer "+key}

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
        #shots_count = input_prompt.count("FINISH")
        output = raw_output[0]["generated_text"].split("FINISH")[0]
        choices.append(output)
    return prompting.extract_subinfo(choices, args, n)
