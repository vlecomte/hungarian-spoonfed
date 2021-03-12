from collections import Counter
import glob

from lemmatizer import *
from util import *

ngram = 6
freqList = []
freqId = {}
    
def getFreqId(word):
    if word == -1:
        return 0
    return freqId[word]

# Represents a sentence and its audio
class Note:
    def __init__(self, original, audio, translation, lemmas):
        self.original = original
        self.audio = audio
        self.translation = translation
        self.lemmas = lemmas
    def makeBold(self):
        self.bold = self.original
        for i, word in enumerate(getRawWords(self.original)):
            if getFreqId(self.lemmas[i]) == self.freq:
                self.bold = boldWord(self.bold, word)
    def __repr__(self):
        return self.original + "\t" + freqList[self.freq] + " (rank " + str(self.freq) + ")"
    def __str__(self):
        return self.original + "\t" + self.bold + "\t" + self.audio + "\t" + self.translation

# Tries to find the "most unique" sentence to teach a certain word (newLemma),
# given the sentences already chosen (exclude)
def mostUnique(notes, exclude, newLemma):
    formsSeen = set()
    cntLemmasExcluded = Counter()
    cntAll = Counter()
    for i in exclude:
        for word in getWords(notes[i].original):
            formsSeen.add(word)
        cntLemmasExcluded.update(notes[i].lemmas)
        
    for note in notes:
        cntAll.update(note.lemmas)
    
    # score prioritizes, in this order:
    # 1) has a new form of word being taught
    # 2) has a unique word compared to other sentences (and sentence is not too long)
    # 3) has a word that isn't contained in already-chosen sentences (and sentence is not too long)
    maxScore = (False, 0, 0)
    iMax = -1
    for i, note in enumerate(notes):
        uniqueForm = False
        for lemma, word in zip(getWords(note.original), note.lemmas):
            if lemma == newLemma and word not in formsSeen:
                uniqueForm = True
        nonExcluded = 0
        unique = 0
        for word in note.lemmas:
            if cntLemmasExcluded[word] == 0:
                nonExcluded += 1
                if cntAll[word] == 1:
                    unique = 1 # more unique is not necessarily good
        myScore = (uniqueForm, unique / len(note.original), nonExcluded / len(note.original))
        if myScore > maxScore:
            iMax = i
            maxScore = myScore
    return iMax

# Selects a subset of the notes that teach a "new word" to avoid redundancy
# - will select at least one note for every form of the new word that appears
# - if this results in less than 3 notes, add arbitrary notes to reach 3 (if possible)
def selection(freq, lemma, notes):
    used = set()
    choice = []
    
    exclude = []
    while len(choice) < min(3, len(notes)):
        i = mostUnique(notes, exclude, lemma)
        if i == -1:
            break
        choice.append(notes[i])
        exclude.append(i)
    
    return choice

# Import notes from all decks
allLines = []
for filename in glob.glob("decks/clean/*.txt"):
    with open(filename) as f:
        for line in f:
            allLines.append(line.strip().split("\t"))

# Read the original sentences
notes = []
cnt = Counter()
byNGram = {}
removed = 0
for (num, line) in enumerate(allLines):
    original, translation, audio = line
    
    # Get lemmas and update frequency count
    lemmas = list(getLemmas(original))
    cnt.update(lemmas)
    
    # Add note
    notes.append(Note(original, audio, translation, lemmas))

print("Top frequencies before applying list:")
for lemma, freq in cnt.most_common(20):
    print(lemma, freq)

# Adjust counts with frequency list
FACTOR = cnt.most_common(1)[0][1]
for lemma in cnt:
    cnt[lemma] /= FACTOR

with open("freq.txt") as freqFile:
    for i, line in enumerate(freqFile):
        cnt[lemmatize(line.strip())] += 1/(i+1)

print("Top frequencies after applying list:")
for lemma, freq in cnt.most_common(20):
    print(lemma, freq)

# Sort by frequency
freqList = [word for (word,occ) in cnt.most_common()]
freqId = {word: rank for (rank,word) in enumerate(freqList)}

# Isolate the least frequent word in each note (the "new word")
# and sort them by decreasing frequency of the "new word"
for note in notes:
    note.freq = 0
    for lemma in note.lemmas:
        note.freq = max(note.freq, getFreqId(lemma))
    note.makeBold()
notes.sort(key = lambda note: note.freq)

# Limit the number of sentences that teach the same "new word"
last = -1
finalChoice = []
curPart = []
for note in notes:
    # Run selection() every time we switch to another "new word"
    if note.freq != last:
        finalChoice.extend(selection(last, freqList[last], curPart))
        curPart = []
    last = note.freq
    
    # Add notes to buffer if it isn't teaching the obvious
    if note.freq != freqId[OBVIOUS]:
        curPart.append(note)
# Add last buffer in
finalChoice.extend(selection(last, freqList[last], curPart))

# Debug output with frequencies
with open("debug.txt", 'w') as ferr:
    for note in finalChoice:
        ferr.write("\n".join(("{} (occs {}, rank {})".format(freqList[note.freq], cnt[freqList[note.freq]], note.freq), note.original, note.translation, str(note.lemmas), "", "")))

# Sample for getting an idea
with open("sample.md", 'w') as fsample:
    nSample = 500
    fsample.write("# The first {} sentences\n".format(nSample))
    fsample.write("(The word being taught is given in square brackets.)\n\n")
    for note in finalChoice[:nSample]:
        fsample.write("- [{}]  {}  {}\n".format(freqList[note.freq], note.bold.replace("<b>", "**").replace("</b>", "**"), note.translation))

# Clean output for importing into Anki
with open("out.txt", "w") as fout:
    for note in finalChoice:
        fout.write(str(note) + "\n")

# Some debug output
print("unrecognized:", unrecognized)
print("propers:", propers)
