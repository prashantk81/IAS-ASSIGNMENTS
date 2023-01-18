from ftplib import FTP as ftp
import os

hostname="ftp.DriveHQ.com"
username="prashantkumar_123"
passowrd="iiith@1234"

client=ftp(hostname,username,passowrd)
def fetchallmsg(userid):
    filename=userid+".txt"
    with open(filename,'wb') as fe:
        client.retrbinary("RETR "+filename,fe.write,1024)   
    f = open(filename, "r")
    lines=f.readlines()
    f.close() 
    finalmsg=[]
    printmessage=[]       
    for line in lines:
        temp=[]
        temp=line.split(':')
        lastchar=temp[2]
        if(lastchar=="u\n"):
            printmessage.append(temp[0]+":"+temp[1])
            temp[2]="r\n"
            line=":".join(temp)
        finalmsg.append(line)
    if(len(printmessage)==0):
        print("There is no message for you...")
    else:
        for x in range(len(printmessage)):
            print (printmessage[x]),      
    with open(filename,"w") as f:
        for line in finalmsg:
            f.write(line)
    with open(filename,'rb') as fe:
        client.storbinary("STOR "+filename,fe)                            
    os.remove(filename)


def sendingmsg(msg):
    temp=[]
    temp=msg.split(':')
    tomsg=temp[0]
    message=temp[1]
    filename=tomsg+".txt"
    with open(filename,'wb') as fe:
        client.retrbinary("RETR "+filename,fe.write,1024)
    uploadedmsg=name+":"+message+":u\n"    
    with open (filename, 'a') as file:  
        file.write(uploadedmsg)  
    with open(filename,'rb') as fe:
        client.storbinary("STOR "+filename,fe)
    os.remove(filename)
    
if __name__=="__main__":
    global name
    name=input("Enter username :- ")
    while(True):
        print()
        message=input("Enter Message :- ")
        if(message=="fetch"):
            fetchallmsg(name)
        elif(message=="who am i"):
            print(name)   
        elif(message=="quit"):
            break     
        else:
            sendingmsg(message)
    client.quit()        
