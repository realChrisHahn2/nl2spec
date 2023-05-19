import argparse

def parse_args():
    parser = argparse.ArgumentParser(
                        prog = 'nl2spec',
                        description = 'Translates natural language to LTL formulas',
                        epilog = 'Beta. If encountering problems, please contact hahn@cs.stanford.edu')

    parser.add_argument('--model', required=False, default="gpt-3.5-turbo", help='chose the deep learning model')
    parser.add_argument('--nl', required=True, default="", help='input sentence') 
    parser.add_argument('--fewshots', required=False, default="",  help='provide few shot examples')
    parser.add_argument('--keyfile', required=False, default="", help='provide open ai key (for codex usage), or a huggingface api key (for bloom usage)')
    parser.add_argument('--keydir', required=False, default="", help='if not specify keyfile, specify directory')
    parser.add_argument('--prompt', required=False, default="minimal", help='secifies the name of the promptfile')
    parser.add_argument('--maxtokens', required=False, default=64, help='Maximum number of tokens to compute')
    parser.add_argument('--given_translations', required=False, default="", help='Provides given translations')
    parser.add_argument('--num_tries', type=int, required=False, default=3, help="Number of runs the underlying language model attempts a translation.")
    parser.add_argument('--temperature', required=False, default=0.2, type=float, help="Model temperature.")
    args = parser.parse_args()
    return args
