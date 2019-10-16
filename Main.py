import sys

from pip._vendor.distlib.compat import raw_input

from Database import Database
from InvertedIndex import InvertedIndex


def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term}\033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)


def main():
    db = Database()
    index = InvertedIndex(db)

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
                index.index_document(document)

    for texts in range(0, len(index.db)):
        print(texts)

    search_term = raw_input("Enter term(s) to search: ")
    result = index.lookup_query(search_term)

    print(result)

    for term in result.keys():
        for appearance in result[term]:
            document = db.get(appearance.docIndex)
            print(highlight_term(appearance.docIndex, term, document['text']))
            print("-----------------------")


main()
