import models


def call(args):
    model = args.model
    if model == "codex":
        res = models.codex(args)
        return res
    if model == "bloom":
        res = models.bloom(args)
        return res
    raise Exception("Not a valid model.")
