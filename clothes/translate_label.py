# -*- coding: utf-8 -*-

import codecs

import os

import json_load

# coat_label = ['袖型', '版型', '衣长', '图案', '风格', '材质', '袖长', '领型']
coat_label = ['袖型', '版型', '衣长', '风格', '袖长', '领型']
# skirt_label = ['裙长', '材质', '裙型', '尺码', '风格', '季节', '颜色', '图案']
skirt_label = ['裙长', '材质', '裙型', '风格', '图案']
# trousers_label = ['尺码', '风格', '材质', '闭合方式', '季节', '裤长', '颜色', '厚薄']
trousers_label = ['风格', '材质', '裤长', '厚薄']

coat = ['data/coat/label/', coat_label]
skirt = ['data/skirt/label/', skirt_label]
trousers = ['data/trousers/label/', trousers_label]


def get_json_file_names(root_path):
    return os.listdir(root_path)


def get_json_obj(path):
    json_file = codecs.open(path, 'r', 'utf-8')
    json_raw = json_file.read()
    json_file.close()
    return json_load.json_loads_byteified(json_raw)


def create_description_file(obj_map, category):
    description_data = {}
    for label in category[1]:
        description_data[label] = []

    for k, obj in obj_map.iteritems():
        for obj_key, obj_value in obj.iteritems():
            if obj_key in description_data.keys():
                if obj_value.find(',') != -1:
                    obj_value = obj_value[0:obj_value.find(',')]
                if obj_value not in description_data[obj_key]:
                    description_data[obj_key].append(obj_value)

    # print description_data

    description_file = codecs.open(category[0] + 'description.txt', 'w')
    for label in description_data.keys():
        description_file.write(label + '\n')
        index = 0
        for item in description_data[label]:
            description_file.write(str(index) + ': ' + item + '\n')
            index += 1
        description_file.write('\n')
    description_file.close()

    return description_data


def create_label_file(obj_map, category, description_data):
    for label, tags in description_data.iteritems():
        # For example: label == '袖型', tags == ['长袖', '短袖', ...]
        label_data = {}
        for good_id, obj in obj_map.iteritems():
            if label in obj.keys():  # 确保商品含有此项数据
                if obj[label] in tags:  # 确保此数据是已知类型
                    label_data[good_id] = tags.index(obj[label])
                else:
                    label_data[good_id] = -1
            else:
                label_data[good_id] = -2

        label_file = open(category[0] + 'output/' + label.decode('utf-8') + '.txt', 'w')
        for item_key, item_val in label_data.iteritems():
            label_file.write(item_key + ' ' + str(item_val) + '\n')
        label_file.close()


def get_obj_map(category):
    json_file_name_list = get_json_file_names(category[0] + 'raw/')
    # labels = category[1]
    obj_map = {}
    for json_file_name in json_file_name_list:
        if json_file_name.find('.json') != -1:
            obj_map[json_file_name[:-5]] = (get_json_obj(category[0] + 'raw/' + json_file_name))
        # print json_file_name
        # break
    return obj_map


def run(category):
    obj_map = get_obj_map(category)

    description_data = create_description_file(obj_map, category)
    create_label_file(obj_map, category, description_data)


def test_label(category):
    count = 0
    key_value = {}
    obj_map = get_obj_map(category)
    for k, obj in obj_map.iteritems():
        for obj_key in obj.keys():
            if obj_key in key_value.keys():
                key_value[obj_key] += 1
            else:
                key_value[obj_key] = 1

        count += 1
        if count >= 50:
            break

    for key in key_value:
        if key_value[key] >= 45:
            print key.decode('utf-8') + '  ' + str(key_value[key])


def main():
    # run(coat)
    # test_label(skirt)
    # run(skirt)
    # test_label(trousers)
    run(trousers)


if __name__ == '__main__':
    main()
