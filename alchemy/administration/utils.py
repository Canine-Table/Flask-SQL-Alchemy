from alchemy.utils import get_date_string
import secrets
import json
import os

def json_database(query,data):

    rows = []
    index = []
    for k,v in enumerate(data['rows']()):
        index.append(k)
        tmp = []
        for column in v:
            tmp.append(str(column))
        rows.append(tmp)


    history_log = {
        "query_history":[{
            str(secrets.token_hex(128)):{
                "date_queried":get_date_string(),
                "raw_query":query,
                "table_data":{int(k):str(v) for k,v in zip(index,data['headers'])},
                "table_body":[{int(k):list(v) for k,v in zip(index,rows)}]
            }
        }]
    }

    file_dump = os.path.join(os.path.realpath('./alchemy'),'administration','static','json','_query_logs.json')
    if not os.path.exists(file_dump):
        with open(file_dump, 'w'):
            pass

    if os.path.getsize(file_dump) != 0:
        with open(str(file_dump), 'r') as f:
            json_object = json.loads(f.read())
            updated_msg = json_object.copy()
            updated_msg['query_history'].extend(history_log['query_history'])
    else:
        updated_msg = history_log

    with open(str(file_dump), 'w') as f:
        json.dump(updated_msg,f,indent=4)
