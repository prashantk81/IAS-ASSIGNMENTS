from ftplib import FTP
from pathlib import Path
import os
hostname, username, password = "127.0.0.1", "admin", "adminpass"
ftp = FTP()
ftp.connect('127.0.0.1', 3000)
if __name__ == "__main__":

    while (True):
