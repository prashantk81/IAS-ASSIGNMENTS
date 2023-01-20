import sys
import subprocess
import time
import os
import shutil
from ftplib import FTP
from pathlib import Path
hostname, username, password = "127.0.0.1", "admin", "adminpass"
ftp = FTP()
ftp.connect('127.0.0.1', 3000)
ftp.login("admin", "adminpass")
ServerPath = "/data"
slavePath = "/data/request"
if __name__ == "__main__":
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
        else:
            print("Invalid Command!!!")
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
                        print("slave and master server name should not be same")
                    else:
                        try:
                            ftp.mkd(slavePath+"/"+slaveServerName)
                            flag = 0
                        except Exception as e:
                            flag = 1
                            print(e)
                        ftp.cwd("/")
                        os.mkdir(slaveServerName)
                        p = os.path.join(
                            os.getcwd(), slaveServerName, "request")
                        os.mkdir(p)
                        p = os.path.join(
                            os.getcwd(), slaveServerName, "response")
                        os.mkdir(p)

                        # update slave server operation in master server
                        idx = 2
                        operation = ""
                        while idx < len(serverlist):
                            operation = operation+":"+serverlist[idx]
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
                        ftp.cwd("/")
                        # update in data structure
                        allFunction = ""
                        while idx < len(serverlist):
                            allFunction = allFunction+serverlist[idx]+" "
                            idx = idx + 1
                        # create sub server
                        proc = subprocess.Popen(
                            ['python3', 'server.py', 'run_slave', allFunction])
                        time.sleep(2)
                        pid = proc.pid
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
                    print("process with pid "+str(p["pid"])+" is killed")
                    ftp.cwd(slavePath)
                    ftp.rmd(p["name"])
                    ftp.cwd("/")
                    shutil.rmtree(p["name"])
                ftp.cwd(ServerPath)
                ftp.delete(masterServerFileName)
                ftp.cwd("/")
                os.remove(masterServerFileName)
                break

            else:
                print("Wrong Command")
    elif args[1] == "run_slave":
        # while(True):
