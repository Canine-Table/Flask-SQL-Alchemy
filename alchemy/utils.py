from datetime import datetime
import secrets
import json
import os
import re

def error_string(**kwargs):
    error = kwargs['error']
    match =  re.findall(r'"(.*?)"', str(error))
    if match:
        return str(match[0])
    else:
        match =  re.findall(r"'(.*?)'", str(error))
        if match:
            return str(match[0])
        else:
            if kwargs.get('get_none',False):
                return None
            return str(error)


def get_date_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def error_log(**kwargs):

    error = kwargs['error']
    error_date = get_date_string()

    msg = error_string(error=error,get_none=True)
    name = type(error).__name__

    file_dump = kwargs.get('file_dump',os.path.join(os.path.realpath('./alchemy'),'static','json','_error_logs.json'))
    if not os.path.exists(file_dump):
        with open(file_dump, 'w'):
            pass

    error_msg = {
        "messages":[{
            str(secrets.token_hex(128)):{
                "datetime":str(error_date),
                "name":str(name),
                "message":str(msg),
                "full":str(error)
            }
        }]
    }

    if os.path.getsize(file_dump) != 0:
        with open(str(file_dump), 'r') as f:
            json_object = json.loads(f.read())
            updated_msg = json_object.copy()
            updated_msg['messages'].extend(error_msg['messages'])
    else:
        updated_msg = error_msg

    with open(str(file_dump), 'w') as f:
        json.dump(updated_msg,f,indent=4)
