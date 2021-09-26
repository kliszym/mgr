import json

json_file = open('cost.json', mode='r')
json_file_content = json_file.read()
json_file.close()

data = json.loads(json_file_content)
