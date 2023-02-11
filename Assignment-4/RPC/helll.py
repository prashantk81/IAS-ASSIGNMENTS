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


import socket
import json
import sys


class fxnCalculationRecv:
    def __init__(self, fxnname, totalArg, sp):
        self.fxnname = fxnname
        self.totalArg = totalArg
        self.sp = sp

    def __call__(self, *args):
        lengthOfArgs = len(args)
        if lengthOfArgs == self.totalArg:
            fxndict = {'name': self.fxnname, 'args': args}
            allFxnArgs = json.dumps(fxndict)
            self.sp.sendall(str.encode(allFxnArgs))
            responseFromServer = self.sp.recv(1024).decode('utf-8')
            return responseFromServer
        else:
            print("Incorrect Arguments in {} function".format(self.fxnname))
            exit()


def serverConnection(HOSTNAME, PORTNUMBER):
    sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sp.connect((HOSTNAME, PORTNUMBER))
    return sp


def findCallableFxn(receivedFxnDetails, sp):
    i = 0
    while i < len(receivedFxnDetails):
        allfunction = json.loads(receivedFxnDetails[i])
        i = i+1
        calledFunction = fxnCalculationRecv(
            allfunction['name'], len(allfunction['args']), sp)
        setattr(connectToServer, allfunction['name'], calledFunction)


class connectToServer:
    def __init__(self, HOSTNAME, PORTNUMBER):
        # connect to server through socket
        sp = serverConnection(HOSTNAME, PORTNUMBER)
        jsonFile = {}
        sp.sendall(b'getFunctions')
        data = sp.recv(1024).decode('utf-8')
        receivedFxnDetails = data.split('$')
        findCallableFxn(receivedFxnDetails, sp)
