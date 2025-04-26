import json

my_Data = [{'a':None}] # python
my_json_data = json.dumps(my_Data) # json
my_python_data = json.loads(my_json_data) # python

print(my_json_data)
print(my_python_data)