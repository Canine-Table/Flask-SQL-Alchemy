from alchemy.utils import get_date_string
import secrets
import json
import os

def json_database(query,data):

    rows = []
    index = []
    for k,v in enumerate(data['frozen_rows']()):
        index.append(k)
        tmp = []
        for column in v:
            tmp.append(str(column))
        rows.append(tmp)

    history_log = {
        "headers":["date_queried","raw_query"],
        "query_history":[{
            str(secrets.token_hex(128)):{
                "query_string":[get_date_string(),query],
                "table_data":[str(header) for header in data['frozen_headers']],
                "table_body":[{int(k):list(v) for k,v in zip(index,rows)}]
            }
        }]
    }

    file_dump = os.path.join(os.path.realpath('./alchemy'),'administration','static','json','_query_logs.json')

    if os.path.getsize(file_dump) != 0:
        with open(str(file_dump), 'r') as f:
            json_object = json.loads(f.read())
            updated_msg = json_object.copy()
            updated_msg['query_history'].extend(history_log['query_history'])
    else:
        updated_msg = history_log

    with open(str(file_dump), 'w') as f:
        json.dump(updated_msg,f,indent=4)

def delete_json_column(file_path,file_data,md5_hash,json_key):

    if md5_hash == 'delete_all_entries':
        file_data[json_key].clear()
    else:
        key = 0
        for index in file_data[json_key]:
            for value in index:
                if value == md5_hash:
                    del file_data[json_key][key]
                    break
                key += 1
    with open(str(file_path), 'w') as f:
        json.dump(file_data,f,indent=4)
