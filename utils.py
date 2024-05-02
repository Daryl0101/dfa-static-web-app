def file_preprocess(file_name: str):
    """
    Preprocesses the file by:
    1. removing duplicates
    2. sorting the words
    3. removing non-alphabetic words
    """
    words = []
    alphabets = set("abcdefghijklmnopqrstuvwxyz")
    file = open(file_name, "r")
    words = file.read().splitlines()
    file.close()
    # print(
    #     sorted(
    #         list(
    #             set(
    #                 word
    #                 for word in words
    #                 if all(char.lower() in alphabets for char in word)
    #             )
    #         )
    #     )
    # )
    file = open(file_name, "w")
    file.write(
        "\n".join(
            sorted(
                list(
                    set(
                        word
                        for word in words
                        if all(char.lower() in alphabets for char in word)
                    )
                )
            )
        )
    )
    file.close()


def find_duplicates_in_files(file_names: list[str]):
    words = []
    for file_name in file_names:
        file = open(file_name, "r")
        words += file.read().splitlines()
        file.close()
    print(sorted(list(set([word for word in words if words.count(word) > 1]))))


file_preprocess("adjectives.txt")
# find_duplicates_in_files(["conjunctions.txt", "adverbs.txt", "adjectives.txt"])
