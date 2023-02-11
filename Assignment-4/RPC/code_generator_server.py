import sys
fileName = "rpc_server.py"


def generateRPCFile(jsonFile):
    fileContent = '''from inspect import signature
from os import path
import inspect
import server
import socket
import json



def printError(msg):
    print(msg)
    exit()

class functionDetails:
    def __init__(self,name,args):
        self.name = name
        self.args = args
        #self.response = response

def functionExists(f: functionDetails):
    function_names = [func for func in dir(server) if not func.startswith('__')]
    if f.name in function_names:
        return True
    return False

class RPC:
    functionsRegistered = []
    def registerFunctions(self,filePath):
        if not (path.exists(filePath)):
            printError(filePath+" does not exists")
        file1 = open(filePath,'r')
        Lines = file1.readlines()
        for  f in Lines:
            tokens = f.split()
            functionName = tokens[0]
            args = []
            for x in range(1,len(tokens)):
                args.append(tokens[x])
            func = functionDetails(functionName,args)
            if functionExists(func):
                self.functionsRegistered.append(func)
            else:
                printError(functionName + " does not exists in module")
    
def jsonify(functions):
    ans = ""
    for f in functions:
        ans += json.dumps(vars(f)) + '$'
    ans = ans[:-1]
    return ans

def main():
    rpc = RPC()
    jsonFile='%s'
    rpc.registerFunctions("functionNames.txt")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    PORT = 12346
    s.bind(('127.0.0.1',PORT))
    s.listen()
    while True:
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("recvd form client",data)
                if not data:
                    break
                elif data == b'getFunctions':
                    funcNamesJson = jsonify(rpc.functionsRegistered)
                    conn.sendall(str.encode(funcNamesJson))
                else:
                    data = data.decode('utf-8')
                    funcDetails = json.loads(data)
                    print(funcDetails)
                    methodToCall = getattr(server,funcDetails['name'])
                    ans = methodToCall(*funcDetails['args'])
                    conn.sendall(str.encode(str(ans)))
    

if __name__ == "__main__":
    main()''' % jsonFile
    f = open(fileName, "w")
    f.write(fileContent)
    f.close()


if __name__ == "__main__":
    if (len(sys.argv) > 2):
        print("imvalid Arguments")
    else:
        jsonFile = sys.argv[1]
    generateRPCFile(jsonFile)
