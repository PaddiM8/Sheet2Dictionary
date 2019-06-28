import csv
import json
import pickle
import os.path
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
options = {}

def run_setup():
    print("-= Setup =-")
    print("The spreadsheet id is in the spreadsheet URL. Example: 1K4ICqBO1N4HdhZ0sr3tq6EQHe5zDK0OPxd3Ik_rHAQf")
    print("The sheet name is shown on the tab on the bottom of the screen.")
    dictionaryName = input("Choose dictionary name: ")
    sheetId = input("Spreadsheet ID: ")
    sheetName = input("Sheet name: ")
    options["spreadsheetId"] = sheetId
    options["range"] = sheetName + "!A:ZZ"
    options["name"] = dictionaryName
    options["outputLocation"] = dictionaryName
    with open('options.json', 'w') as outfile:
        json.dump(options, outfile, ensure_ascii=False, indent=2)


if not os.path.exists('credentials.json') and not os.path.exists("token.pickle"):
    print("You need to enable the Google Sheets API and download the credentials.json file.")
    print("Then move the credentials.json file to this directory and re-run the script.")
    print("Enable Google Sheets API here: https://bit.ly/2vbwMH0")
    quit()
elif os.path.exists('options.json'):
    with open('options.json') as f:
        options = json.load(f)
else:
    run_setup()

def inject_name(name):
    with open(options["outputLocation"] + "/index.html", "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(data.replace("<!-- NAME -->", name, 2))
        f.truncate()

def copy_template(target):
    if not os.path.exists(options["outputLocation"]):
        os.makedir(options["outputLocation"])
    for filename in os.listdir("template"):
        target = options["outputLocation"] + "/" + filename
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

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
    spreadsheetId=options["spreadsheetId"], range=options["range"]).execute()
    rows = result.get('values', [])
    words = generate_words(rows)

    copy_template(options["outputLocation"])

    with open(options["outputLocation"] + '/scripts/words.js', 'w') as file:
        file.write("const words = " + json.dumps(words, separators=(',', ':')) + ";")
    inject_name(options["name"])
    print("Done! Open " + options["outputLocation"] + "/index.html")

if __name__ == '__main__':
    main()
