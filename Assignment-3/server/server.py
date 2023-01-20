import sys
import subprocess
import time
import os
import shutil
from ftplib import FTP
from pathlib import Path
hostname, username, password = "127.0.0.1", "admin", "adminpass"
if __name__ == "__main__":
    ftp = FTP()
    ftp.connect('127.0.0.1', 3000)
    ftp.login("admin", "adminpass")
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
                ftp.cwd("/")
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
                                    allFunction = allFunction + \
                                        serverlist[idx]+" "
                                    idx = idx + 1
                                # create sub server
                                command = ['python3', 'server.py']
                                command += serverlist
                                proc = ""
                                try:
                                    proc = subprocess.Popen(command)
                                except Exception as e:
                                    print(e)
                                else:
                                    time.sleep(2)
                                    pid = proc.pid
                                    # update slave server operation in master server
                                    idx = 2
                                    operation = ""
                                    while idx < len(serverlist):
                                        operation = operation + \
                                            ":"+serverlist[idx]
                                        idx = idx + 1
                                    slaveServerEntry = slaveServerName+operation+"\n"
                                    with open(masterServerFileName, "a") as f:
                                        f.write(slaveServerEntry)
                                    # upload to ftp server
                                    ftp.cwd(ServerPath)
                                    with open(masterServerFileName, "rb") as file:
                                        try:
                                            ftp.storbinary(
                                                f"STOR {masterServerFileName}", file)
                                        except Exception as e:
                                            print(e)
                                    # ftp.cwd("/")
                                    slaveEntry = {
                                        "name": slaveServerName,
                                        "pid": pid,
                                        "process": proc,
                                    }
                                    allserverstatus.append(slaveEntry)
                    elif serverlist[0] == "quit":
                        for p in allserverstatus:
                            proc = p['process']
                            proc.kill()
                            print("process with pid " +
                                  str(p["pid"])+" is killed")
                            ftp.cwd(slavePath)
                            ftp.rmd(p["name"])
                            # ftp.cwd("/")
                            shutil.rmtree(p["name"])
                        ftp.cwd(ServerPath)
                        ftp.delete(masterServerFileName)
                        # ftp.cwd("/")
                        os.remove(masterServerFileName)
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
        ftp.cwd(slaveServerName)
        while (True):
            alldir = ftp.nlst()
            # download all files from ftp
            for fp in alldir:
                localPath = os.path.join(localrequest, fp)
                with open(localPath, "wb") as file:
                    try:
                        ftp.retrbinary(f"RETR {fp}", file.write)
                    except Exception as e:
                        print(e)
                    else:
                        ftp.delete(fp)
            allfiles = os.listdir(localrequest)
            # process all downloaded files
            for fileName in allfiles:
                # client file name= client+count+.txt
                clientNamewithoutex = fileName.split(".")
                clientName = clientNamewithoutex[0]
                path = os.path.join(localrequest, fileName)
                fileptr = open(path, "r")
                operation = fileptr.readlines()
                expression = operation[0].split(":")
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
                modifiedFileName = slaveServerName+"."+fileName
                resPath = os.path.join(localresponse, modifiedFileName)
                file_object = open(resPath, "w")
                file_object.write(str(result))
                file_object.close()
                fileptr.close()
                deletefilePath = os.path.join(localrequest, fileName)
                os.remove(deletefilePath)
                ftp.cwd(slavePathresponse+"/"+clientName)
                with open(resPath, "rb") as file:
                    try:
                        ftp.storbinary(f"STOR {resPath}", file)
                    except Exception as e:
                        print(e)
                os.remove(resPath)
                # break
    ftp.quit()
