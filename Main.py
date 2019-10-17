import sys
import nltk

from collections import Counter

from Database import Database
from InvertedIndex import InvertedIndex


def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term}\033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)


def main():
    db = Database()
    index = InvertedIndex(db)

    stopwords = nltk.corpus.stopwords.words("portuguese")
    stopwords.sort()

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
                index.index_document(document, stopwords)

    file_query = open(sys.argv[2], 'r')
    result = index.lookup_query(file_query.read())

    # Write on file indice
    file_index = open("output/indice.txt", "w+")
    for term in result.keys():
        file_index.write(term + ": ")
        for appearance in result[term]:
            document = db.get(appearance.docIndex)
            file_index.write(str(appearance.docIndex) + "," + str(appearance.frequency) + " ")
        file_index.write("\n")
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
