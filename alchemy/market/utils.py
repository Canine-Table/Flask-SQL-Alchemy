def string_to_dict(string):
    new_dict = {}
    for pairs in string.split(','):
        new_list = str(pairs).split(':')
        new_dict[new_list[0]] = new_list[1]
    return new_list
