from signal import signal, SIGPIPE, SIG_DFL
from ftplib import FTP
from pathlib import Path
import os
import time
hostname, username, password = "127.0.0.1", "client", "adminpass"
signal(SIGPIPE, SIG_DFL)
if __name__ == "__main__":
    ftp = FTP()
    ftp.connect(hostname, 3000)
    ftp.login(username, password)
    clientResponse = "/data/response"
    clientRequest = "/data/request"
    mainserverpath = "/data"
    userName = input("Enter Username:- ")
    # create username directory locally and ftpserver
    os.mkdir(userName)
    ftp.cwd(clientResponse)
    try:
        ftp.mkd(userName)
    except Exception as e:
        print(e)
    count = 0
    while (True):
        command = input("Enter Message:- ")
        if (command == "quit"):
            os.rmdir(userName)
            ftp.cwd(clientResponse)
            ftp.rmd(userName)
            break
        elif (command == "lookup"):
            ftp.cwd(mainserverpath)
            allfilesanddir = ftp.nlst()
            for dir in allfilesanddir:
                if (dir.find(".")):
                    mainserverfilename = dir
            with open(mainserverfilename, "wb") as file:
                try:
                    ftp.retrbinary(f"RETR {mainserverfilename}", file.write)
                except Exception as e:
                    print(e)
            fileptr = open(mainserverfilename, "r")
            slavedetails = fileptr.readlines()
            fileptr.close()
            if (len(slavedetails) > 0):
                message = ""
                i = 0
                while i < len(slavedetails)-1:
                    temp = slavedetails[i][0:len(slavedetails[i])-1]
                    details = temp.split(":")
                    message = details[0]+"-> "
                    idx = 1
                    while (idx < len(details)):
                        message += details[idx]+", "
                        idx += 1
                    message = message[0:len(message)-2]
                    print(message)
                    i += 1
                temp = slavedetails[len(slavedetails)-1] .split(":")
                lastmessage = ""
                lastmessage = temp[0]+"-> "
                idx = 1
                while (idx < len(temp)):
                    lastmessage += temp[idx]+", "
                    idx += 1
                lastmessage = lastmessage[0:len(lastmessage)-2]
                print(lastmessage)
            os.remove(mainserverfilename)
        else:
            messagecontent = command.split(":")
            serverName = messagecontent[0]
            message = messagecontent[1]+":"
            message += messagecontent[2]+":"+messagecontent[3]
            clientFileName = userName+"@"+str(count)+".txt"
            count += 1
            # create file locally
            file_object = open(clientFileName, "w")
            file_object.write(message)
            file_object.close()
            # upload to corresponding server
            ftp.cwd(clientRequest)
            ftp.cwd(serverName)
            status = 0
            with open(clientFileName, "rb") as file:
                try:
                    ftp.storbinary(f"STOR {clientFileName}", file)
                except Exception as e:
                    print(e)
                else:
                    status = 1
            if (status):
                time.sleep(1)
                os.remove(clientFileName)
            # after uploading check output in data/response folder
            newpath = clientResponse+"/"+userName
            ftp.cwd(newpath)
            allfiles = ftp.nlst()
            for fp in allfiles:
                path = os.path.join(os.getcwd(), userName, fp)
                with open(path, "wb") as file:
                    try:
                        ftp.retrbinary(f"RETR {fp}", file.write)
                    except Exception as e:
                        print(e)
                tmp = 0
                with open(path, "r+") as fileptr:
                    try:
                        content = fileptr.readlines()
                        print(content[0])
                    except Exception as e:
                        print(e)
                    else:
                        tmp = 1
                if (tmp):
                    time.sleep(1)
                    ftp.delete(fp)
            os.remove(path)
    ftp.quit()
