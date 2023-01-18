from ftplib import FTP
from pathlib import Path
import os
hostname, username, password = "127.0.0.1", "admin", "adminpass"
# ftp_client = FTP(hostname, username, password)
# ftp_client = FTP(host = hostname, user = username, passwd = password, acct = '', timeout = None)
ftp = FTP()
ftp.connect('127.0.0.1', 3000)
ftp.login(username, password)
count=0
count2=0
result=0
def makefolder(name): 
    inPath = '/Input/'+name
    outPath= '/Output/'+name
    ftp.mkd(inPath) 
    ftp.mkd(outPath)

def sendingmsg(userinput):
    ## all parameters
    global count
    userinput=userinput.split(":")
    touser=userinput[0]
    fromuser=name
    operation=userinput[1]
    operand1,operand2=userinput[2],userinput[3]
    ## check dir exist or not
    ftp.cwd('/Input')
    alldir=ftp.nlst()
    if touser in alldir:
        ## dir exists
        ## filename
        file_name = fromuser+str(count)+".txt"
        count=count+1
        ## message
        message=fromuser+":"+operation+":"+operand1+":"+operand2

        with open(file_name, "w") as f:
            f.write(message)

        ftp.cwd(touser)
        uploadfilepath=file_name
        with open(uploadfilepath, "rb") as file:
            try:
                ftp.storbinary(f"STOR {file_name}", file)
            except Exception as e:
                print(e)
    else:
        ## dir not exists
        print("there is no such active user...")  
    ftp.cwd("/")
    os.remove(file_name) 

def processData(operation):
    opers=operation.split(":")
    fromuser=opers[0]
    operation=opers[1]
    oprd1=opers[2]
    oprd2=opers[3]
    global result
    if(operation=="add"):
        result=int(oprd1)+int(oprd2)
    elif(operation=="sub"):
        result=int(oprd1)-int(oprd2)
    elif(operation=="mul"):
        result=int(oprd1)*int(oprd2)
    elif(operation=="div"):
        try:
            result=int(oprd1)/int(oprd2)
        except Exception as e:
            result=e
    else:
       result="Invalid Operation.."
    ## writing output in receiver file   
    global count2
    ftp.cwd("/Output/"+fromuser)
    outputfilename=name+str(count2)+".txt"
    count2=count2+1
    message=operation+" of "+oprd1+" and "+oprd2+" = "+str(result)+"\n"+"******* received from "+name
    with open(outputfilename, "w") as f:
        f.write(message)
    with open(outputfilename, "rb") as file:
        try:
            ftp.storbinary(f"STOR {outputfilename}", file)
        except Exception as e:
            print(e)
    ftp.cwd("/")
    os.remove(outputfilename)            

def performPendingOperation():
    ftp.cwd("/Input/"+name)
    allfiles=ftp.nlst()
    length=len(allfiles)
    ftp.cwd("/")
    if(length==0):
        print("No opertions for you...")
    else:
        for downloadfile in allfiles:
            flag=0
            ftp.cwd("/Input/"+name)
            with open(downloadfile, "wb") as file:
                try:
                    ftp.retrbinary(f"RETR {downloadfile}", file.write)
                except Exception as e:
                    print(e)
                else:
                    flag=1  
            if(flag):
                ftp.delete(downloadfile)
                ftp.cwd("/") 
                with open(downloadfile, "r") as f:
                    msgs = f.readlines()
                    processData(msgs[0])
                    os.remove(downloadfile)                        

def performFetch():
    ftp.cwd("/Output/"+name)
    allfiles=ftp.nlst()
    length=len(allfiles)
    if(length==0):
        print("First give parameters")
    else:
        for outputfile in allfiles:
            flag=0
            with open(outputfile, "wb") as file:
                try:
                    ftp.retrbinary(f"RETR {outputfile}", file.write)
                except Exception as e:
                    print(e)
                else:
                    flag=1  
            if(flag):
                ftp.delete(outputfile) 
                with open(outputfile, "r") as f:
                    msgs = f.readlines()
                    print(msgs[0])
                    print(msgs[1])
                    os.remove(outputfile)   
    ftp.cwd("/")                                     




if __name__=="__main__":
    global name
    name=input("Enter Username:- ")
    makefolder(name)
    while(True):
        print()
        userinput=input("Enter operation:-")
        if(userinput=="fetch output"):
            performFetch()
        elif(userinput=="pending operation"):
            performPendingOperation()
        elif(userinput=="quit"):
            ftp.cwd("/")
            ftp.cwd("/Input")
            ftp.rmd(name)
            ftp.cwd("/")
            ftp.cwd("/Output")
            ftp.rmd(name)
            break
        else:
            sendingmsg(userinput)


