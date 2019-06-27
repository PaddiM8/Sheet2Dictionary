import csv
import json

def parse_example_string(exampleString):
    if not exampleString: return None
    examples = []
    for example in exampleString.split('|'):
        examples.append(example.split('>'))
    return examples


words = []
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i, row in enumerate(csv_reader):
        lastDefinition = 5 if row[4] else 4
        types = [x.strip() for x in row[2].split(',')]
        word = {
                "id":          i,
                "word":        row[0],
                "english":     row[1],
                "types":       types,
                "definitions": row[3: lastDefinition],
                "examples":    []
                }
        for i in range(len(types)):
            word["examples"].append(parse_example_string(row[5 + i]))
        words.append(word)

with open('../scripts/words.js', 'w') as file:
    file.write("const words = " + json.dumps(words, separators=(',', ':')) + ";")
