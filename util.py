import re

# Bold the first non-bolded occurrence of word sub in s
# (actually just checks if it's surrounded by non-word, non-angle brackets characters)
def boldWord(s, word):
    bolded = re.sub(r"(^|[^\w<>])" + word + r"($|[^\w<>])", r"\1<b>" + word + r"</b>\2", s, 1)
    assert(bolded != s)
    return bolded
