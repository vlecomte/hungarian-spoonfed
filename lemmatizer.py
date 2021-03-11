from emmorphpy import EmMorphPy
import re

OBVIOUS = "[obvious]"
UNKNOWN = "[unknown]"

# Prefixes of some of the proper nouns in these decks (hopefully it doesn't catch too many other things)
OBVIOUS_PROPERS = ["tom", "mary", "boston", "harvard", "ausztráli", "budapest", "dunántúlt", "svéd", "moszkv", "amerik", "sándor", "john", "székesfehérvár", "taro", "sztálin", "franci", "york", "róma", "rómá", "ausztri", "smith", "jackson", "csehszlovákia", "london", "hollandi", "kanad", "szovjetuni", "péter", "brazíli", "bulgári", "mária", "éva", "románia", "európá", "paul", "albáni", "laurie", "jugoszlávi", "portugál", "norvég", "belg", "angli", "rigá", "mari", "edward", "odol", "lispe", "carousel", "kenji", "mojszejev"]
NONOBVIOUS_PROPERS = ["allamok", "bécs", "német", "finn", "lengyel", "magyar", "olasz", "orosz", "duná", "svajc", "török"]


_lemmatizer = EmMorphPy()


# Takes a conjugated form and returns its stem
def lemmatize(word):
    possibleStems = _lemmatizer.stem(word)
    if len(possibleStems) == 0:
        for known in NONOBVIOUS_PROPERS:
            if word.startswith(known):
                return word
        for known in OBVIOUS_PROPERS:
            if word.startswith(known):
                return OBVIOUS
        if "-" in word:
            return OBVIOUS
        return UNKNOWN + word
    else:
        return possibleStems[0][0]


WORD_PATTERN = re.compile(r"[\w-]+")
CAP_PUNCTUATION = ".?!"

# Extract words made of letters and dashes from a string
def getRawWords(s):
    return re.findall(WORD_PATTERN, s)

# Same but lowercase
def getWords(s):
    return [word.lower() for word in getRawWords(s)]

unrecognized = set()
propers = set()

# Extract stems of all the words in a sentence
def getLemmas(s):
    lemmas = []
    lastStart = -1
    for m in re.finditer(WORD_PATTERN, s):
        # Check whether there is punctuation since last word
        hasPunctuation = (lastStart == -1)
        for i in range(max(lastStart, 0), m.start()):
            if s[i] in CAP_PUNCTUATION:
                hasPunctuation = True
        lastStart = m.start()
        
        # If word is capitalized and not at beginning of sentence, it's probably a proper noun, so assume it's "obvious" and doesn't need to be taught
        if m.group()[0].isupper() and not hasPunctuation:
            lemmas.append(OBVIOUS)
            propers.add(m.group())
        else:
            lemma = lemmatize(m.group().lower())
            if lemma.startswith(UNKNOWN):
                unrecognized.add(m.group())
            lemmas.append(lemmatize(m.group().lower()))
    return lemmas
