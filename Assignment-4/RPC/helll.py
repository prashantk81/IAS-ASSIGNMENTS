# # ['{"name": "ConcatenateMessage", "args": ["str"]}',
# #     '{"name": "add", "args": ["int", "int"]}',
# #     '{"name": "mult", "args": ["int", "int"]}',
# #     '{"name": "divide", "args": ["int", "int"]}']


# def readJsonFile(jsonFile):
#     with open(jsonFile) as fp:
#         data = json.load(fp)
#     dataList = []
#     for itr in data['remote_procedures']:
#         dict = {}
#         dict['name'] = itr['procedure_name']
#         value = []
#         for i in itr['parameters']:
#             value.append(i['data_type'])
#         dict['args'] = value
#         dataList.append(dict)
#     return dataList


# class connectToServer:

#     def __init__(sef, HOSTNAME, PORTNUMBER):
#         sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sp.connect((HOSTNAME, PORTNUMBER))
#         jsonFile = 'contract.json'
#         jsonContent = readJsonFile(jsonFile)
#         for d in jsonContent:
#             funcDetails = json.loads(d)
#             newFunc = callableFunc(
#                 funcDetails['name'], len(funcDetails['args']), sp)
#             setattr(connectToServer, funcDetails['name'], newFunc)
