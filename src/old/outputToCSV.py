import csv
import pickle

with open('scrappedIPOs.pkl', 'rb') as input:
    IPOs = pickle.load(input)

# print(IPOs)
header = []
for k,v in IPOs.items():
    if v.getLabels():
        header = v.getLabels()
print(header)

for k,v in IPOs.items():
    v.formatAttributes()

num = "30%)"
print(int(float(num.strip("%)"))))

# print(float("2,100,000.00".strip(',')))
exit()
with open("output.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(header)

    for k, v in IPOs.items():
        # print(v.getLabels())
        writer.writerow(v.getValues())