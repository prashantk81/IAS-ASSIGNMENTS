from ftplib import FTP

hostname, username, password = "127.0.0.1", "admin", "adminpass"
# ftp_client = FTP(hostname, username, password)
# ftp_client = FTP(host = hostname, user = username, passwd = password, acct = '', timeout = None)
ftp = FTP()
ftp.connect('127.0.0.1', 3000)
ftp.login(username, password)
