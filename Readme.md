# Overview

nl2spec is a framework for applying Large Language Models (LLMs) to derive formal specifications (in temporal logics) from unstructured natural language. It introduces a new methodology to detect and resolve the inherent ambiguity of system requirements in natural language by utilizing LLMs to map subformulas of the formalization back to the corresponding natural language fragments of the input. Users iteratively add, delete, and edit these sub-translations to amend erroneous formalizations, which is easier than manually redrafting the entire formalization.

The tool works best when providing in-distribution few-shot examples (see [Prompting](#prompting)). It can be easily adjusted to other models by extending the backend (see [Extendability](#extendability)).

# Install

Fulfill dependencies:
- [flask](https://flask.palletsprojects.com/en/2.2.x/)
- [ltlf2dfa](https://github.com/whitemech/LTLf2DFA)
- [huggingface](https://huggingface.co/)
- [openai-api](https://openai.com/blog/openai-api)
- [google-cloud-aiplatform](https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html)

All model inferences run in the cloud. Therefore, access to the respective APIs is necessary.
 - For bloom and bloomz, a [huggingface](huggingface.co) *User Access Token* is needed. You can create a token and use bloom/bloomz for free.
 - For Codex / GPT-based models, an [OpenAI](openai.com) *API key* is needed. See [OpenAI's Pricing](https://openai.com/pricing)
 - For using PaLM, access through *google cloud platform* is required. Set up a project in [google cloud platform](https://console.cloud.google.com/) with [Vertex AI enabled](https://console.cloud.google.com/vertex-ai) and [authenticate with the Google Cloud CLI](https://cloud.google.com/cli). See [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing).
 - See [Extendability](#extendability) on how to add more models.
 - Model inference through the APIs may be discontinued by the providers, which is beyond our control. This currently affects codex and bloomz. In the web interface, we marked these models as *obsolete*.


# Run frontend

From inside the ```src``` folder:
- create the following file and paste your open ai, hf key or google project id into: ```keys/oai_key.txt```, ```keys/hf_key.txt``` or ```keys/google_project_id.txt```
- ```python3 -m flask --app frontend.py run```
- add ```--debug``` for debug mode
- Then open web-based tool at http://127.0.0.1:5000

# Run from terminal

Can also be run from command line from the ```scr``` folder. See ```python3 nl2ltl.py --help``` for more details.

E.g., with gpt-3.5:

```python3 nl2ltl.py --model gpt-3.5-turbo --keyfile PATH/TO/YOUR/OPENAIKEY --nl "Globally a and b until c." --num_tries 3 --temperature 0.2 --prompt minimal```

or bloom

```python3 nl2ltl.py --model bloom --keyfile PATH/TO/YOUR/HFKEY --nl "Every request is eventually followed by a grant." --num_tries 3 --temperature 0.2 --prompt minimal```

or PaLM

```python3 nl2ltl.py --model text-bison@001 --keyfile PATH/TO/YOUR/GCLOUD/PROJECTID --nl "Every request is eventually followed by a grant." --num_tries 3 --temperature 0.2 --prompt minimal```

# Prompting

The prompting pattern consists of a short introduction to the specification language, followed by few-shot examples that exploit the LLM to construct subtranslations.
We provide four example prompts in ```/prompts```:
- minimal.txt - the generic prompt used for the user study experiments in the [paper]()
- indistribution.txt - the prompt with few-shot examples drawn from the user study
- smart.txt - a prompt obtained from examples in a recently conducted [smart home user study]()
- stl.txt - a proof of concept extension for [Signal Temporal Logic (STL)]()

See [the paper]() and ```/prompts``` for more details.
The prompts in nl2spec must follow a specific pattern to obtain the subtranslations as follows.

```<Specification Language Tutorial>```

Followed by few shot examples, where each few shot example consists of the following:

```<Natural Language input>```

```<Given translations, as a dictionary>```

```<Explanation of the translation>```

```<Explanation dictionary>```

```<Final Translation>```

# Extendability

The tool can be easily extended to other specification languages based on temporal logics (see ```/prompts/stl.txt```). The best performance is expected when drawing the few-shot examples from the distribution to translate. Adding a few well-crafted examples to the prompt and then using the tool to translate the rest of the workload is significantly easier than translating every requirement from scratch.

Additionally, the tool can be extended to more fine-tuned or other upcoming open-source language models. To this end, ```backend.py``` must be extended with a new ```new_model```, for which a method named ```new_model``` must be implemented in ```models.py```.

# How to cite

```
@inproceedings{nl2spec,
	title = {nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models},
	author = {Cosler, Matthias and Hahn, Christopher and Mendoza, Daniel and Schmitt, Frederik and Trippel, Caroline},
	booktitle = {Computer {Aided} {Verification}},
	series = {Lecture {Notes} in {Computer} {Science}},
	address = {Cham},
	isbn = {978-3-031-37703-7},
	shorttitle = {nl2spec},
	doi = {10.1007/978-3-031-37703-7_18},
	language = {en},
	publisher = {Springer Nature Switzerland},
	editor = {Enea, Constantin and Lal, Akash},
	year = {2023},
	pages = {383--396},
}
```
