import os


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


create_directory('data')
create_directory('data/coat')
create_directory('data/shoes')
create_directory('data/skirt')
create_directory('data/trousers')

for sub_direct in ('coat', 'shoes', 'skirt', 'trousers'):
    create_directory('data/' + sub_direct + '/picture')
    create_directory('data/' + sub_direct + '/label')
    create_directory('data/' + sub_direct + '/label/raw')
    create_directory('data/' + sub_direct + '/label/output')
