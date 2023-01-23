import sys
import subprocess
import time
import os
import shutil
from ftplib import FTP
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
hostname, username, password = "127.0.0.1", "server", "adminpass"
if __name__ == "__main__":
    ftp = FTP()
    ftp.connect(hostname, 3000)
    ftp.login(username, password)
    ServerPath = "/data"
    slavePath = "/data/request"
    slavePathresponse = "/data/response"
    masterServerStatus = 0
    masterServerName = ""
    masterServerFileName = ""
    allserverstatus = []
    args = sys.argv
    if (args[1] == "run_master"):
        if (len(args) == 3):
            if (masterServerStatus):
                print("Master server is already running")
            else:
                masterServerFileName = args[2]+".txt"
                file_object = open(masterServerFileName, "w")
                file_object.close()
                ftp.cwd(ServerPath)
                with open(masterServerFileName, "rb") as file:
                    try:
                        ftp.storbinary(f"STOR {masterServerFileName}", file)
                    except Exception as e:
                        print(e)
                masterServerStatus = 1
                masterServerName = args[2]
                print("Master Server is running now...")
                while (True):
                    serverInput = input("Enter your message:- ")
                    serverlist = serverInput.split(" ")
                    if serverlist[0] == "run_slave":
                        if (masterServerStatus == 0):
                            print("First Run Master Server")
                        else:
                            # slave server start
                            slaveServerName = serverlist[1]
                            if (slaveServerName == masterServerName):
                                print(
                                    "slave and master server name should not be same")
                            else:
                                allFunction = ""
                                idx = 2
                                while idx < len(serverlist):
                                    allFunction += serverlist[idx]+" "
                                    idx = idx + 1
                                # create sub server
                                command = ['nohup', 'python3.9', 'server.py']
                                command += serverlist
                                command.append('&')
                                proc = ""
                                try:
                                    proc = subprocess.Popen(command)
                                except Exception as e:
                                    print(e)
                                else:
                                    time.sleep(1)
                                    pid = proc.pid
                                    # update slave server operation in master server
                                    idx = 2
                                    operation = ""
                                    while idx < len(serverlist):
                                        operation += ":"+serverlist[idx]
                                        idx = idx + 1
                                    slaveServerEntry = slaveServerName+operation+"\n"
                                    with open(masterServerFileName, "a") as f:
                                        f.write(slaveServerEntry)
                                    slaveEntry = {
                                        "name": slaveServerName,
                                        "pid": pid,
                                        "process": proc,
                                    }
                                    allserverstatus.append(slaveEntry)
                                    # upload to ftp server
                                    ftp.cwd(ServerPath)
                                    with open(masterServerFileName, "rb") as file:
                                        try:
                                            ftp.storbinary(
                                                f"STOR {masterServerFileName}", file)
                                        except Exception as e:
                                            print(e)
                                    print("slave server " +
                                          slaveServerName+" is running... ")
                    elif serverlist[0] == "quit":
                        flag = 0
                        ftp.cwd(slavePath)
                        for p in allserverstatus:
                            proc = p['process']
                            proc.kill()
                            print(" Slave process with pid " +
                                  str(p["pid"])+" is killed")
                            ftp.rmd(p["name"])
                            shutil.rmtree(p["name"])
                            flag = 1
                        if flag:
                            ftp.cwd(ServerPath)
                            ftp.delete(masterServerFileName)
                        os.remove(masterServerFileName)
                        os.remove("nohup.out")
                        ftp.quit()
                        break
                else:
                    print("Wrong Command")
    elif args[1] == "run_slave":
        slaveServerName = args[2]
        ftp.cwd(slavePath)
        try:
            ftp.mkd(slaveServerName)
        except Exception as e:
            print(e)
        path = os.path.join(os.getcwd(), slaveServerName)
        os.mkdir(path)
        localrequest = os.path.join(
            path, "request")
        os.mkdir(localrequest)
        localresponse = os.path.join(
            path, "response")
        os.mkdir(localresponse)

        while (True):
            ftp.cwd(slavePath+"/"+slaveServerName)
            try:
                alldir = ftp.nlst()
            except Exception as e:
                print(e)
            # download all files from ftp
            else:
                path = os.path.join(os.getcwd(), slaveServerName, "request")
                for fp in alldir:
                    localPath = os.path.join(path, fp)
                    status = 0
                    with open(localPath, "wb") as file:
                        try:
                            ftp.retrbinary(f"RETR {fp}", file.write)
                        except Exception as e:
                            print(e)
                        else:
                            status = 1
                    if (status):
                        ftp.delete(fp)

            # process all downloaded files
                for fileName in alldir:
                    # client file name= client+count+.txt
                    clientNamewithoutex = fileName.split(".")
                    clientNamewithspecial = clientNamewithoutex[0].split("@")
                    clientName = clientNamewithspecial[0]
                    path1 = os.path.join(os.getcwd(), slaveServerName)
                    localrequest = os.path.join(
                        path1, "request")
                    path = os.path.join(localrequest, fileName)
                    fileptr = open(path, "r")
                    operation = fileptr.readlines()
                    expression = operation[0].split(":")
                    fileptr.close()
                    operation = expression[0]
                    operand1 = expression[1]
                    operand2 = expression[2]
                    result = 0
                    if (operation == "add"):
                        result = int(operand1)+int(operand2)
                    elif (operation == "sub"):
                        result = int(operand1)-int(operand2)
                    elif (operation == "mul"):
                        result = int(operand1)*int(operand2)
                    else:
                        result = "Invalid Opeartion"
                    modifiedFileName = fileName
                    temp = os.path.join(os.getcwd(), slaveServerName)
                    localresponse = os.path.join(
                        temp, "response")
                    resPath = os.path.join(localresponse, modifiedFileName)
                    file_object = open(resPath, "w")
                    resultmessage = "From "+slaveServerName+" : "+operation
                    resultmessage += " of "+operand1
                    resultmessage += " and "+operand2+" is "+str(result)
                    file_object.write(resultmessage)
                    file_object.close()
                    deletefilePath = os.path.join(
                        os.getcwd(), slaveServerName, "request", fileName)
                    os.remove(deletefilePath)
                for filename in alldir:
                    localresponse = os.path.join(
                        os.getcwd(), slaveServerName, "response")
                    resPath = os.path.join(localresponse, fileName)
                    ftp.cwd(slavePathresponse)
                    ftp.cwd(clientName)
                    with open(resPath, "rb") as file:
                        try:
                            ftp.storbinary(f"STOR {filename}", file)
                        except Exception as e:
                            print(e)
                        else:
                            os.remove(resPath)
