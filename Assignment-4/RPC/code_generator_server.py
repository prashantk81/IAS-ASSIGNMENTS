import sys
fileName = "rpc_server.py"


def generateRPCFile(jsonFile):
    fileContent = '''from os import path
import socket
import json
import server_procedures
HOSTNAME = '127.0.0.1'
PORTNUMBER = 1234
jsonFile = '%s'


class functionDetails:
    def __init__(self, fxnname, argument):
        self.name = fxnname
        self.args = argument


def isFunctionDefined(fxnptr: functionDetails):
    function_names = []
    for idx in dir(server_procedures):
        if (not idx.startswith('__')):
            function_names.append(idx)
    if fxnptr.name in function_names:
        return True
    return False


def storeDetails(jsonData):
    functionNameAndType = []
    for key in jsonData['remote_procedures']:
        functionName = key['procedure_name']
        argumentType = []
        i = 0
        while i < len(key['parameters']):
            if len(key['parameters'][i]) == 0:
                continue
            else:
                argumentType.append(key['parameters'][i]['data_type'])
            i = i+1
        allfunctiondetail = functionDetails(functionName, argumentType)
        if isFunctionDefined(allfunctiondetail) == True:
            functionNameAndType.append(allfunctiondetail)
        else:
            print("{} is not defined.".format(functionName))
            exit()
    return functionNameAndType


def readJsonFile():
    # read json file ans store details
    if not (path.exists(jsonFile)):
        print("{} file does not exists".format(jsonFile))
        exit()
    else:
        fp = open(jsonFile)
        jsonData = json.load(fp)
        return storeDetails(jsonData)


def serverConnetionAndListener(HOSTNAME, PORTNUMBER):
    # connection establish and listen
    sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sp.bind((HOSTNAME, PORTNUMBER))
    sp.listen()
    return sp


def acceptConnectionRequest(sp):
    return sp.accept()


def calculation(dataReceivedFromClient):
    dataReceivedFromClient = dataReceivedFromClient.decode(
        'utf-8')
    allfxn = json.loads(dataReceivedFromClient)
    fxncallcalculation = getattr(
        server_procedures, allfxn['name'])
    return fxncallcalculation(*allfxn['args'])


def jsonify(functions):
    ans = ""
    for f in functions:
        ans += json.dumps(vars(f)) + '$'
    ans = ans[:-1]
    return ans


if __name__ == "__main__":
    # Read json file ans function details in list of dict
    allfxnNameType = readJsonFile()
    # listening server for client
    sp = serverConnetionAndListener(HOSTNAME, PORTNUMBER)
    print("Server is ready to listen...")
    flag = True
    while flag:
        connection, clientaddress = acceptConnectionRequest(sp)
        with connection:
            print("client with address {} is connected to server".format(clientaddress))
            while flag:
                dataReceivedFromClient = connection.recv(1024)
                if not dataReceivedFromClient:
                    break
                elif dataReceivedFromClient == b'getFunctions':
                    funcNamesJson = jsonify(allfxnNameType)
                    connection.sendall(str.encode(funcNamesJson))
                else:
                    finalResult = calculation(dataReceivedFromClient)
                    connection.sendall(str.encode(str(finalResult)))
''' % jsonFile
    f = open(fileName, "w")
    f.write(fileContent)
    f.close()


if __name__ == "__main__":
    if (len(sys.argv) > 2):
        print("imvalid Arguments")
    else:
        jsonFile = sys.argv[1]
    generateRPCFile(jsonFile)
