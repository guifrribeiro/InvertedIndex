import re
import nltk

from Appearance import Appearance


class InvertedIndex:
    def __init__(self, db):
        nltk.download("punkt")
        nltk.download("rslp")
        self.index = dict()
        self.db = db
        self.terms = []
        self.radicals = []
        self.list = []

    def __repr__(self):
        return str(self.index)

    # Processing a document
    def index_document(self, document, stopwords, radicals):
        # Remove punctuation from the text
        clean_text = re.sub(r'[^\w\s]', '', document['text'])

        listAux = []

        self.terms = nltk.word_tokenize(clean_text)
        appearances_dict = dict()

        stemmer = nltk.stem.RSLPStemmer()
        var = [stemmer.stem(term) for term in self.terms if term not in stopwords]
        listAux += var
        self.list.append(var)
        listAux.sort()
        self.list.sort()

        radicals += [x for i, x in enumerate(listAux) if i == listAux.index(x)]
        # Counts the frequency of terms
        for term in self.terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], document['name'], term_frequency + 1)

        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)
        self.db.add(document)

        return document

    def lookup_query(self, query):
        return {term: self.index[term] for term in query.split(' ') if term in self.index}

    def countWords(self, word, list):
        frequency = ""
        i = 0
        for items in list:
            i += 1
            if items.count(word) > 0:
                frequency += (str(i) + ',' + str(items.count(word)) + ' ')

        return word + ": " + frequency
