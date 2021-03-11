import os

if not os.path.exists("raw"):
    os.makedirs("raw")

with open("raw/fsi2.txt") as fin, open("clean/fsi2.txt", 'w') as fout:
    for line in fin:
        fields = line.strip().split("\t")
        hu, audio, en = fields
        if hu[0].isalpha() or hu[0].isdigit():
            if hu[0].islower():
                hu = hu[0].upper() + hu[1:]
            fout.write("\t".join((hu, en, audio)) + "\n")
