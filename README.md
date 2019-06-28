# Sheet2Dictionary
**I updated the instructions, so if you didn't get it to work before, you should be able to get it working now!**
This tool reads your word list spreadsheet and creates a portable HTML dictionary automatically. All you have to do is provide the Google spreadsheet id (and sheet name). This way you can easily edit your dictionary from anywhere(even collaboratively). You could for example make it periodically re-generate the dictionary and push it to netlify using a CRON job, all automatically.
 
* Search for words
* Word definitions
* Examples for words
* Static, no backend
* Generates the dictionary from a Google Sheet document
* Responsive, works on phones

![dictionary](https://i.imgur.com/lAUrPS1.png)

## Usage
1. Create the spreadsheet as shown below.
2. Install [Python 3](https://www.python.org/downloads/release/python-373/), then run the following in a command line/terminal: `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib` to install the Google API client the tool needs. If it fails, you may need to run it with sudo/admin privileges.
3. Clone/download [this repository](https://github.com/PaddiM8/Sheet2Dictionary/archive/master.zip) (and unzip). Then simply go to the Sheet2Dictionary/gen folder and run `gen.py` with python 3. In a terminal, that would be `python3 gen.py`
4. This will prompt you to enable the Google Sheets API. Simply follow [the link](https://developers.google.com/sheets/api/quickstart/python?authuser=1) and enable it. After that, download the configuration and place `credentials.json` in the `gen` directory. Run `gen.pỳ` again, and follow the instructions.
4. Open index.html in a browser

## Spreadsheet
The spreadsheet consists of the following columns:  

| Word | Translation | Part of Speech (1) | IPA(optional) | Definition | Examples |
|---|---|---|---|---|---|
| apfel| apple | noun | /ˈapfəl/ | Eine lesbare essbare Frucht | Er isst der Apfel |

The first row in the spreadsheet will not be included. The (1) after 'Part of Speech' indicates how many parts of speech one word can be. For example, if some some words could be either a noun or verb depending on context, you change this value to (2), and write "noun, verb" in cell. This means you also need two collumns for definitions and two columns for examples, so you can write definitions/examples for the words for the different situations. An example: 

| Word | Translation | Part of Speech (2) | Definition 1 | Definition 2 | Examples 1 | Example 2 |
|---|---|---|---|---|---|---|
| vālo| leg, walk, go | noun, verb | A limb | Moving using one's legs | vālosē > It is a leg | vālon toralu > I walk to the house |

As you can see, you can provide a translation after a `>`. You can also provide several examples for one "part of speech" by separating them by a pipe: `|`.  
[Example Sheet](https://docs.google.com/spreadsheets/d/1_te9ZTrF1mvLh3p8U_uhptGdGzOtBWBbvMA0dXGV15c/edit?usp=sharing)
(Colors are of purely for aesthetic purposes)  
[Example Sheet with an IPA column](https://docs.google.com/spreadsheets/d/1aku5t5W1UJcxVLz2l9HiSpuDXbgQT-3nQTrYV8dmo6k/edit?usp=sharing)
