import os, re

if not os.path.exists("raw"):
    os.makedirs("raw")

with open("raw/tatoeba.txt") as fin, open("clean/tatoeba.txt", 'w') as fout:
    for line in fin:
        fields = line.strip().split("\t")
        hu = fields[1]
        audio = fields[2]
        en = fields[4]
        if len(en) != 0:
            en = en[1:-1] # remove surrounding quotes
            en = re.split("<[^<>]*>", en)[2]
            assert(len(en) != 0)
            fout.write("\t".join((hu, en, audio)) + "\n")
