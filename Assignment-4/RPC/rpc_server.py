from inspect import signature
from os import path
import inspect
import socket
import json
import server_procedures


def printError(msg):
    print(msg)
    exit()


class functionDetails:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        # self.response = response


def functionExists(f: functionDetails):
    function_names = [func for func in dir(
        server_procedures) if not func.startswith('__')]
    if f.name in function_names:
        return True
    return False


class RPC:
    functionsRegistered = []

    def registerFunctions(self, filePath):
        if not (path.exists(filePath)):
            printError(filePath+" does not exists")
        f = open('contract.json')
        data = json.load(f)
        for f in data['remote_procedures']:
            functionName = f['procedure_name']
            x = f['parameters']
            args = []
            for d in x:
                if len(d) != 0:
                    a = d['data_type']
                    args.append(a)
            print(functionName, args)
            func = functionDetails(functionName, args)
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
    jsonFile = 'contract.json'
    rpc.registerFunctions(jsonFile)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 12346
    s.bind(('127.0.0.1', PORT))
    s.listen()
    while True:
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print("recvd form client", data)
                if not data:
                    break
                elif data == b'getFunctions':
                    funcNamesJson = jsonify(rpc.functionsRegistered)
                    conn.sendall(str.encode(funcNamesJson))
                else:
                    data = data.decode('utf-8')
                    funcDetails = json.loads(data)
                    print(funcDetails)
                    methodToCall = getattr(
                        server_procedures, funcDetails['name'])
                    ans = methodToCall(*funcDetails['args'])
                    conn.sendall(str.encode(str(ans)))


if __name__ == "__main__":
    main()
