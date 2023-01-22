# IAS - Assignment 3: Remote procedure server-client system

# Instructions regarding this assignment

- In the root of the assignment folder we have a "data" directory and inside "request" and "response" directories inside it. These will be used as FTP storage locations.
- request directory is used for query purpose and response is for storing result.

# To run this assignment

- To start the FTP server, run the command:-
  Goto ftpserver directory and run this command
  `python3.9 ftpserver.py`
- The master server will be started on running the server/server.py file using the command:-
  Goto server directory and run this command
  `python3.9 server.py run_master sv0`
  Here, I have named the master server as sv0.
- Now the input prompt of the master server will be displayed and if we want to start more slave servers simply enter the command:-
  `run_slave sv1 add sub`
  Here, I have named the slave server as sv1 and it will perform add and sub functionalities.
- To run the client,goto client directory and run the command:-
  `python3.9 client.py`
- Enter the username of the client
- To do a lookup on the client for the existing servers run the command:-
  `lookup`
- Now we'll get all the active servers along with their functionalities.
- If the client wants to perform addition functionality on sv1 run the command:-
  `sv1:add:1:2`
- If we want to exit the client code and server code run command
  `quit`
