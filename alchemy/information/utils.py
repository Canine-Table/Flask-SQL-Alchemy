import re

def filter_results(regexpr_,list_):
    result = []
    for matches in [re.match(f".*(?i){regexpr_}.*", item) for item in list_]:
        if matches != None:
            result.append(matches.group())
    return result or None

def n_to_br(list_):
    return re.sub('\n','<br>',list_)
