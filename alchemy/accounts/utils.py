import os

def crop_to_square(image):
    width, height = image.size
    if width == height:
        return image
    elif width > height:
        offset = int(abs(height - width) / 2)
        return image.crop((offset, 0, width - offset, height))
    else:
        offset = int(abs(width - height) / 2)
        return image.crop((0, offset, width, height - offset))

def after_create_account_table():
    root_user = {
        'username':'root',
        'password':os.environ['ROOT_PASSWORD'],
        'first_name':'root',
        'last_name':'None',
        'email_address': 'root@flask.ca',
        'phone_number':'000-000-0001',
        'balance': 999999,
        'uid':1,
        'age':'1970-01-01',
        'group': 'root_users',
        'privilages': 777
    }
    admin_user = {
        'username':'administrator',
        'password':os.environ['ADMIN_PASSWORD'],
        'first_name':'administrator',
        'last_name':'None',
        'email_address': 'administrator@flask.ca',
        'phone_number':'000-000-0002',
        'balance': 999999,
        'uid':2,
        'age':'1970-01-01',
        'group': 'root_users',
        'privilages': 777
    }
    info_user = {
        'username':'information',
        'password':os.environ['INFO_PASSWORD'],
        'first_name':'information',
        'last_name':'None',
        'email_address': 'information@flask.ca',
        'phone_number':'111-000-0001',
        'balance': 999999,
        'uid':3,
        'age':'1970-01-01',
        'group': 'privilaged_users',
        'privilages': 774
    }
    test_user_one = {
        'username':'johndoe0123',
        'password':os.environ['TEST_PASSWORD_ONE'],
        'first_name':'john',
        'last_name':'doe',
        'email_address': 'johndoe0123@flask.ca',
        'phone_number':'111-000-0002',
        'balance': 999999,
        'uid':4,
        'age':'1970-01-01',
        'group': 'root_users',
        'privilages': 774
    }
    test_user_two = {
        'username':'janedoe0123',
        'password':os.environ['TEST_PASSWORD_TWO'],
        'first_name':'jane',
        'last_name':'doe',
        'email_address': 'janedoe0123@flask.ca',
        'phone_number':'111-000-0003',
        'balance': 999999,
        'uid':5,
        'age':'1970-01-01',
        'group': 'privilaged_users',
        'privilages': 774
    }

    return [root_user,admin_user,info_user,test_user_one,test_user_two]
