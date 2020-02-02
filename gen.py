import csv
import ntpath
import json
import os.path
import shutil
import sys

def inject_name(name):
    with open(name + "/index.html", "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(data.replace("<!-- NAME -->", name, 2))
        f.truncate()

def copy_template(name):
    if not os.path.exists(name):
        os.makedirs(name)
    for filename in os.listdir("template"):
        target = name + "/" + filename
        templateFile = "template/" + filename
        if os.path.isdir(templateFile):
            if os.path.exists(target): shutil.rmtree(target)
            shutil.copytree(templateFile, target) # copy template
        else:
            if os.path.exists(target): os.remove(target)
            shutil.copy(templateFile, target) # copy template

def parse_example_string(exampleString):
    if not exampleString: return None
    examples = []
    for example in exampleString.split('|'):
        examples.append(example.split('>'))
    return examples

def generate_words(rows):
    words = []
    maxTypes = 1
    try: maxTypes = int(rows[0][2][-2:][0]) # get second last character (a number)
    except: pass
    hasIPA = rows[0][3].lower().strip() == "ipa"
    startDefinitions = 4 if hasIPA else 3
    endDefinitions = startDefinitions + maxTypes

    for i, row in enumerate(rows):
        if (i == 0): continue
        types = "" if len(row) < 3 else [x.strip() for x in row[2].split(',')]
        word = {
                "id":          i - 1,
                "word":        row[0],
                "english":     row[1],
                "types":       types,
                "definitions": row[startDefinitions:endDefinitions],
                "examples":    []
                }

        if hasIPA and len(row) > 3: word["ipa"] = row[3]
        for i in range(len(types)):
            if len(row) <= endDefinitions + i: break # break if there are no more examples
            word["examples"].append(parse_example_string(row[endDefinitions + i]))
        words.append(word)
    return words

def getRowsFromFile(fileLocation):
    with open(fileLocation, "r") as f:
        return list(csv.reader(f))


def main():
    fileLocation = sys.argv[1]
    name = ntpath.basename(fileLocation).split(".")[0]

    rows = getRowsFromFile(fileLocation)
    words = generate_words(rows)
    copy_template(name)

    with open(name + '/scripts/words.js', 'w') as file:
        file.write("const words = " + json.dumps(words, separators=(',', ':')) + ";")
    inject_name(name)
    print("Done! Open " + name + "/index.html")

if __name__ == '__main__':
    main()
