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
        jsonFile = 'contract.json'

        sp.sendall(b'getFunctions')
        data = sp.recv(1024).decode('utf-8')
        receivedFxnDetails = data.split('$')
        findCallableFxn(receivedFxnDetails, sp)
