import parser
import backend


def main():
    args = parser.parse_args()
    res = backend.call(args)
    print("Final formalization with confidence score:")
    print(res[0])
    print("Sub-translations with confidence scores:")
    print(res[1][:-1])  # Remove the information whether a subtranslation is locked
    return


if __name__ == "__main__":
    main()
