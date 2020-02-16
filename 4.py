import os
import os.path
gaosan = list()

with open("4.csv", "r") as f:
    gaosan = f.read().split("\n")
gaosan = list(set(gaosan))
with open("4,csv","w") as f:
    for te in gaosan:
        f.write(te + "\n")