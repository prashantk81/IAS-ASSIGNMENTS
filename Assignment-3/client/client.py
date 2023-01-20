from ftplib import FTP
from pathlib import Path
import os
import time
hostname, username, password = "127.0.0.1", "admin", "adminpass"
if __name__ == "__main__":
    ftp = FTP()
    ftp.connect('127.0.0.1', 3000)
    ftp.login("admin", "adminpass")
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
            fileptr.close()
            os.remove(mainserverfilename)
        else:
            messagecontent = command.split(":")
            serverName = messagecontent[0]
            message = messagecontent[1]+":"
            message += messagecontent[2]+":"+messagecontent[3]
            clientFileName = userName+str(count)+".txt"
            count += 1
            # create file locally
            file_object = open(clientFileName, "w")
            file_object.write(message)
            file_object.close()
            # upload to corresponding server
            ftp.cwd(clientRequest+"/"+serverName)
            with open(clientFileName, "rb") as file:
                try:
                    ftp.storbinary(f"STOR {clientFileName}", file)
                except Exception as e:
                    print(e)
            os.remove(clientFileName)
            # after uploading check output in data/response folder
            time.sleep(5)
            ftp.cwd(clientResponse+"/"+userName)
            allfiles = ftp.nlst()
            for fp in allfiles:
                path = os.path.join(os.getcwd(), userName, fp)
                with open(path, "wb") as file:
                    try:
                        ftp.retrbinary(f"RETR {fp}", file.write)
                    except Exception as e:
                        print(e)
                    else:
                        ftp.delete(fp)
                fileptr = open(path, "r")
                content = fileptr.readlines()
                print(content[0])
                fileptr.close()
                os.remove(path)
    ftp.quit()
