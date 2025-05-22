from os import system 
import sys

if (len(sys.argv) < 2):
    print("This is not a proper file.")

filename = sys.argv[1]

errorTypes = ["error", "exception", "fail", "warn", "null", "rejected"]
system(f"touch output{filename}.txt")

for error in errorTypes:
    system(f"grep {error} {filename} >> output.txt")

errorSummary = {}

with open('output.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line in errorSummary:
            errorSummary[line] += 1
        else:
            errorSummary[line] = 1

sorted_errors = sorted(
    errorSummary.items(), key=lambda pair: pair[1],
    reverse=True
)

top_5 = sorted_errors[:5]

for error, count in top_5:
    print(f"{error} shows up {count} times")