# Hungarian sentences, spoon-fed
This code takes a corpus of Hungarian sentences and sorts them by their least frequent word. This way, the sentences can be used to learn the most frequent words of Hungarian one by one, and in context.

Some details:
- The words are "deconjugated" so that different forms of the same word (e.g. van/vannak, ház/házak) are treated as the same word.
- At most 3 sentences are kept for each word that is being taught; when there are more than 3 available, the algorithm tries to pick sentences with different forms of that word, and generally sentences that are pretty different from each other.
- The frequency is based on both the frequency within the corpus of sentences, and a frequency list obtained [on Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Hungarian_webcorpus_frequency_list) (stored in [freq.txt](freq.txt)).
- The code tries to detect proper nouns and exclude them from the words to be learned, since most of them are very similar to English and don't require separate study.

The resulting Anki deck is available for download [on AnkiWeb](https://ankiweb.net/shared/info/593843988). You can see the first few sentences in order [here](sample.md).

Since the words get less and less common as you go, the usefulness gradually decreases, and you should stop studying studying new cards whenever you feel that it's no longer useful enough per time spent.

## Sentences used
The sentences I used come from two sources:
- Tatoeba: in particular [this Anki deck](https://ankiweb.net/shared/info/1691262801), which collects [all Hungarian sentences with audio](https://tatoeba.org/eng/audio/index/hun). Most sentences and audio on Tatoeba are under various [Creative Commons](https://creativecommons.org/) licenses. The major contributed as of this writing is user [jegaevi](https://tatoeba.org/eng/user/profile/jegaevi).
- FSI: in particular [these](https://ankiweb.net/shared/info/124854924) [two](https://ankiweb.net/shared/info/1875520915) Anki decks. The sentences and audio are in the public domain because they were created by the US government.

I exported those 3 decks into text form in the [decks/raw/](decks/raw/) folder.

## Dependencies
Uses [emMorphPy](https://github.com/dlt-rilmta/emmorphpy).

## Setup
If you want to make your own version of this deck, follow these steps.
- Download and import the 3 decks into your Anki collection so that your media folder contains the audio files.
- Run the 3 Python scripts in [decks/](decks/) to pre-process the decks. Make sure to enable HTML in fields so that the bolding works correctly.
- Run [sort.py](sort.py). This will produce [out.txt](out.txt).
- Import [out.txt](out.txt) into Anki. There are 4 fields, in this order: Hungarian (raw), Hungarian (with word to learn bolded), audio, and English.
