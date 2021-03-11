import os

if not os.path.exists("raw"):
    os.makedirs("raw")

with open("raw/fsi1.txt") as fin, open("clean/fsi1.txt", 'w') as fout:
    for line in fin:
        fields = line.strip().split("\t")
        hu, audio, en = fields
        if hu[0].isalpha():
            if hu[-1] == "." or hu[-1] == "!" or hu[-1] == "?":
                if hu[0].islower():
                    hu = hu[0].upper() + hu[1:]
                fout.write("\t".join((hu, en, audio)) + "\n")
