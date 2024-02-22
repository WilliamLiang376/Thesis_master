import json

up_info = []

with open('Up_info.txt','r') as file:
    data = file.readlines()
    for line in data:
        info = line.split(' ')
        up_info_dict = {}
        up_info_dict['name'] = info[0]
        up_info_dict['uid'] = info[1].strip()
        up_info.append(up_info_dict)

with open('Up_info.json','w',encoding='utf-8') as f_up:
    json.dump(up_info, f_up, ensure_ascii=False, sort_keys=True, indent=4)
        