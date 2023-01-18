from ftplib import FTP

hostname="ftp.DriveHQ.com"
username="prashantkumar_123"
passowrd="iiith@1234"
def listfiles():
    with FTP(hostname) as ftp:
        ftp.login(user=username , passwd=passowrd)
        ftp.dir()
        ftp.quit()

def uploadfile(filename):
    with FTP(hostname) as ftp:
        ftp.login(user=username, passwd=passowrd)
        with open(filename,'rb') as fe:
            ftp.storbinary("STOR "+filename,fe)
        ftp.quit()

def downloadfile(filename):
    with FTP(hostname) as ftp:
        ftp.login(user=username, passwd=passowrd)
        with open(filename,'wb') as fe:
            ftp.retrbinary("RETR "+filename,fe.write,1024)
        print()    
        f = open(filename, "r")
        content = f.read()
        print(content)
        f.close()    
        ftp.quit()

def delete(filename):
    with FTP(hostname) as ftp:
        ftp.login(user=username, passwd=passowrd)
        try:
            response=ftp.delete(filename)
            print(response)
        except Exception as e:
            print(e)        
        ftp.quit()

if __name__=="__main__":
    flag=1
    while(flag):
        print()
        print("Press 1-> List All files")
        print("Press 2-> Upload the file")
        print("Press 3-> Download the file")
        print("Press 4-> Delete the file")
        print("Press 5-> Quit")
        userinput=int(input())
        if(userinput==1):
            listfiles()
            print("All the files listed...")
        elif(userinput==2):
            filename=input() 
            uploadfile(filename) 
            print("File Uploaded Successfully...")
        elif(userinput==3):
            filename=input()
            downloadfile(filename)
        elif(userinput==4):
            filename=input()
            delete(filename)
        else:
            flag=0



