# 创建任务列表
import json

dict = {"任务一": "task1.json",
        "任务二": "task2.json",
        "任务三": "task3.json"}
json.dump(dict, open('all_tasks.json', 'w', encoding='utf-8'), ensure_ascii=False)
p = json.load(open('all_tasks.json','r',encoding='utf-8'))
print(p)

# 创建单项任务
# for i in range(3):
dict = {"task":"任务一",
        "batch":0,
        "name": '1',
        "batch_name":[],
        "model":"Model1"}
json.dump(dict, open('task1.json', 'w', encoding='utf-8'), ensure_ascii=False)

dict = {"task":"任务二",
        "batch":1,
        "name": '',
        "batch_name":['1', '2', '3', '4', '5', '6', '7', '8'],
        "model":"Model2"}
json.dump(dict, open('task2.json', 'w', encoding='utf-8'), ensure_ascii=False)

dict = {"task":"任务三",
        "batch":0,
        "name": '3',
        "batch_name":[],
        "model":"Model3"}
json.dump(dict, open('task3.json', 'w', encoding='utf-8'), ensure_ascii=False)