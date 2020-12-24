import csv
import pickle

filename = "scrappedIPOsFull"

pklFilename = filename + ".pkl"
csvFilename = filename + ".csv"

with open(pklFilename, 'rb') as input:
    IPOs = pickle.load(input)


print("there are ", len(IPOs), " IPOs")

for k,v in IPOs.items():
    if v.validIPO():
        print(k, " is a valid IPO")
        v.formatAttributes()
    else:
        print(k, " IS NOT A VALLID IPO")
        print(v.info)


header = []
for k,v in IPOs.items():
    if v.validIPO():
        header = v.getLabels()
print(header)
with open(csvFilename, "w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(header)

# need to align labels, correct attributes removed/added
    for k, v in IPOs.items():
        # print(v.getLabels())
        if v.validIPO():
            writer.writerow(v.getValues())