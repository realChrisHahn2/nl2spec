import models


def call(args):
    model = args.model
    if model == "code-davinci-002":
        res = models.code_davinci_002(args)
        return res
    if model == "text-bison@001":
        res = models.text_bison_001(args)
        return res
    if model == "code-bison@001":
        res = models.code_bison_001(args)
        return res
    if model == "text-davinci-003":
        res = models.text_davinci_003(args)
        return res
    if model == "code-davinci-edit-001":
        res = models.code_davinci_edit_001(args)
        return res
    if model == "bloom":
        res = models.bloom(args)
        return res
    if model == "gpt-3.5-turbo":
        res = models.gpt_35_turbo(args)
        return res
    if model == "gpt-4":
        res = models.gpt_4(args)
        return res
    if model == "bloomz":
        res = models.bloomz(args)
        return res
    raise Exception("Not a valid model.")
