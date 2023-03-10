# Overview

nl2spec is a framework for applying Large Language Models (LLMs) to derive formal specifications (in temporal logics) from unstructured natural language. It introduces a new methodology to detect and resolve the inherent ambiguity of system requirements in natural language by utilizing LLMs to map subformulas of the formalization back to the corresponding natural language fragments of the input. Users iteratively add, delete, and edit these sub-translations to amend erroneous formalizations, which is easier than manually redrafting the entire formalization.

The tool works best when providing in-distribution few-shot examples (see [Prompting](#prompting)). It can be easily adjusted to other models by extending the backend (see [Extendability](#extendability)).

# Install

Fulfil dependencies:
- [flask](https://flask.palletsprojects.com/en/2.2.x/)
- [ltlf2dfa](https://github.com/whitemech/LTLf2DFA)
- [huggingface](https://huggingface.co/)
- [openai-api](https://openai.com/blog/openai-api)

To use the tool, a [huggingface](huggingface.co) or an [OpenAI](openai.com) key, for access to Bloom or Codex is needed. See [Extendability](#extendability). The tool is using the huggingface and openai apis respectively.

# Run frontend

From inside the ```src``` folder:
- create the following file and paste your open ai or hf key into: ```keys/oai_key.txt``` or ```keys/hf_key.txt```
- ```python3 -m flask --app frontend.py run```
- add ```--debug``` for debug mode
- Then open web-based tool at http://127.0.0.1:5000

# Run from terminal

Can also be run from command line from the ```scr``` folder. See ```python3 nl2ltl.py --help``` for more details.

E.g., with codex:

```python3 nl2ltl.py --model codex --keyfile PATH/TO/YOUR/OPENAIKEY --nl "Globally a and b until c." --num_tries 3 --temperature 0.2 --prompt minimal```

or bloom

```python3 nl2ltl.py --model bloom --keyfile PATH/TO/YOUR/HFKEY --nl "Every request is eventually followed by a grant." --num_tries 3 --temperature 0.2 --prompt minimal```

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

TBD
