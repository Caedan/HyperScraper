from src.website import Website
import json

# Create a Website object
cfc = Website('https://www.cfcunderwriting.com/')

# Dumping the JSON dictionary to a file
with open(cfc.domain + '.json', 'w') as outfile:
    json.dump(cfc.to_json(), outfile)

print(cfc.to_json())
