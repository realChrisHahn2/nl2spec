import models


def call(args):
    model = args.model
    if model == "codex":
        res = models.codex(args)
        return res
    if model == "bloom":
        res = models.bloom(args)
        return res
    if model == "gpt35":
        res = models.gpt35(args)
        return res
    raise Exception("Not a valid model.")
