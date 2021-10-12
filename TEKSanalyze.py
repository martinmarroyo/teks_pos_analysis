import spacy
import string
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter

nlp = spacy.load("en_core_web_sm")
punctuation = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS


"""
    Extracts verbs from each TEKS statement in a given list
    and returns those verbs as a list of strings. To pass in
    a whole page instead of a list, use the optional
    whole_page argument and set it to True
"""
def get_verbs(teks_statement,**kwargs):
    verbs = []
    if 'whole_page' in kwargs.keys() and kwargs['whole_page']== True:
        doc = nlp(teks_statement)
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"
                 and str(token) not in punctuation and token not in stop_words] #Getting the lemma of the verb
    else: 
        for statement in teks_statement:
            doc = nlp(statement)
            verb_list = "; ".join([token.lemma_ for token in doc if token.pos_ == "VERB"
                                   and str(token) not in punctuation and token not in stop_words])
            verbs.append(verb_list)
    return verbs


"""
    Returns a list of verbs and the frequency of each verb from the given list of verbs
"""
def get_verbs_and_counts(teks_statements):
    verbs_list = Counter(teks_statements)
    verbs = []
    counts = []
    for verb in verbs_list:
        verbs.append(verb)
        counts.append(verbs_list[verb])
    return (verbs, counts)
