json_string = 'id:purchased_item.id,name:purchased_item.name,price:purchased_item.price,barcode:purchased_item.barcode,description:purchased_item.description,stock:purchased_item.stock}'

json_list = json_string.split(',')

my_dict = {}

for index in json_list:
    json_dict = str(index).split(':')
    my_dict[json_dict[0]] = json_dict[1]

print(my_dict)
