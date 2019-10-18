import sys
import nltk

from collections import Counter

from Database import Database
from InvertedIndex import InvertedIndex


def main():
    db = Database()
    index = InvertedIndex(db)

    stopwords = nltk.corpus.stopwords.words("portuguese")
    stopwords.sort()

    radicals = []
    num_files = 0
    # Read the base file. Output: db
    with open(sys.argv[1], 'r') as files:
        contents = files.read()
        for lines in contents.split("\n"):
            num_files += 1
            # Open and read the files
            with open(lines, 'r') as cont:
                document = {
                    'id': num_files,
                    'name': lines,
                    'text': cont.read()
                }
                index.index_document(document, stopwords, radicals)

    file_query = open(sys.argv[2], 'r')
    result = index.lookup_query(file_query.read())


    # Write on file indice
    file_index = open("output/indice.txt", "w+")
    [file_index.write(index.countWords(word, index.list) + "\n") for word in Counter(radicals).keys()]
    file_index.close()

    # Write on file resultado
    files_names = []
    for term in result.keys():
        for val in result[term]:
            files_names.append(val.name)

    file_result = open("output/resultado.txt", "w+")
    file_result.write(str(len(Counter(files_names).keys())) + "\n")
    for file_name in Counter(files_names).keys():
        file_result.write(file_name + "\n")

    file_result.close()

main()

