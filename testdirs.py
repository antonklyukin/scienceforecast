import os
import json
import pickle

dir = 'pkl'

journal_data = '''
{
"primary": "Physical Sciences and Engineering",
"domain": "Chemical Engineering",
"subdomain": "Catalysis",
"journal name": "Journal of Catalysis"
}
'''



journal_data = json.loads(journal_data)

file_name = journal_data['journal name'].replace(' ', '') + '.pkl'

run_path = os.path.dirname(os.path.abspath(__file__))

pkl_path = os.path.join(run_path, 'pkl')

if not os.path.exists(pkl_path):
    os.mkdir(pkl_path)

pkl_file_path = os.path.join(pkl_path, file_name)
print(pkl_file_path)
with open(pkl_file_path, 'wb') as file:
    pickle.dump(journal_data, file)
