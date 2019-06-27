import csv
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = "1K4ICqBO1N4HdhZ0sr3tq6EQHe5zDK0OPxd3Ik_rHAQ8"
RANGE = "Lexicon!A:G"

def parse_example_string(exampleString):
    if not exampleString: return None
    examples = []
    for example in exampleString.split('|'):
        examples.append(example.split('>'))
    return examples

def generate_words(rows):
    words = []
    for i, row in enumerate(rows):
        if (i == 0): continue
        lastDefinition = 5 if len(row) >= 5 else 4
        types = "" if len(row) < 3 else [x.strip() for x in row[2].split(',')]
        word = {
                "id":          i - 1,
                "word":        row[0],
                "english":     row[1],
                "types":       types,
                "definitions": row[3: lastDefinition],
                "examples":    []
                }
        for i in range(len(types)):
            if len(row) < 6 + i: continue
            word["examples"].append(parse_example_string(row[5 + i]))
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
    spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    rows = result.get('values', [])
    words = generate_words(rows)
    #words = []
    #with open('test.csv') as csv_file:
    #    csv_reader = csv.reader(csv_file, delimiter=',')
    #    words = generate_word(csv_reader)
    #
    with open('../scripts/words.js', 'w') as file:
        file.write("const words = " + json.dumps(words, separators=(',', ':')) + ";")

if __name__ == '__main__':
    main()
