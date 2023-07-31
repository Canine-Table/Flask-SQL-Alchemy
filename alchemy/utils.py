from datetime import datetime
import secrets
import json
import os
import re

def return_type(boolean):
    if boolean:
        return True
    else:
        return False

def get_configurations(is_enabled):
    if os.getenv('GUNICORN_CMD_ARGS') and is_enabled:
        return is_enabled
    return not is_enabled



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


def get_date_string(**kwargs):
    if kwargs.get('date_format',False):
        if kwargs['date_format'] == 'ISO 8601':
            return datetime.now().strftime('%Y-%m-%d')
        elif kwargs['date_format'] == 'RFC 5322':
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z (%Z)')
        elif kwargs['date_format'] == 'RFC 3339':
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        elif kwargs['date_format'] == 'ANSI X3.30':
            return datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        elif kwargs['date_format'] == 'get_year':
            return datetime.now().strftime('%Y')
        elif kwargs['date_format'] == 'get_month':
            return datetime.now().strftime('%M')
        elif kwargs['date_format'] == 'get_week':
            return datetime.now().strftime('%D')
        elif kwargs['date_format'] == 'get_hour':
            return datetime.now().strftime('%H')
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
        "headers":["datetime","name","message","full"],
        "messages":[{
            str(secrets.token_hex(128)):[str(error_date),str(name),str(msg),str(error)]
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

