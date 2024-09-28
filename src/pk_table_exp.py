"""
this script shows that the openfda label dataset's pharmacokinetic_table field
is not suitable for facile mining of PK data; each table in each separate
application contains a different format, and only a few of the labels
have these values populated

NLP or equivalent on the freeform "pharmacokinetics" field is probably easier
for data mining purposes

author: francis prael
date: 2024 09 28
"""
import os
import requests
import pandas as pd

# shared values
api_url_base = 'https://api.fda.gov/drug/label.json?search=_exists_:pharmacokinetics+AND+openfda.route:"ORAL"'
step = 1000
limit = f"&limit=1000" # largest allowed limit parameter is 1000
skip_value = 0
skip = f"&skip={skip_value}" 

# get total result size
response = requests.get(api_url_base)
r = response.json()
total = r['meta']['results']['total']
total
# page through to pull out PK tables
good_res = []
while skip_value < total:
    # get batch
    url = api_url_base + limit + skip
    response = requests.get(url)
    r = response.json()

    for i, res in enumerate(r['results']):
        try:
            good_res.append(pd.read_html(res['pharmacokinetics_table'][0])[0])
            break
        except:
            pass
    
    if len(good_res) >= 10:
        break
    # adjust skip value
    skip_value += step
    skip = f"&skip={skip_value}"

    print(f'working on value of {skip_value} out of {total} results')

# this table
print(good_res[9])

# has a very different layout from this table (as does each other table)
print(good_res[8])
