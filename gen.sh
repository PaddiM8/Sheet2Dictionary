#!/bin/bash
curl https://ethercalc.org/_/qf3wk99ybry0/csv -o Smirkian.csv
python3 ./gen.py Smirkian.csv

# git
cd SmirkianDictionary
git add .
git commit -m "updated dictionary"
git push origin master
