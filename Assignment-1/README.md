# IAS - Assignment-1: Simple IM using FTP

# Instructions

- I've taken a FTP based file storage on driveHQ with the following credentials:-
- hostname="ftp.DriveHQ.com"
- username="prashantkumar_123"
- passowrd="iiith@1234"

- Because of the restrictions by driveHQ, we can only have two concurrent users active at any given point of time.
- I've hardcoded 5 person namely ujjwal, raghav, rishabh, priyank and prashant
- The user has to run the client code using this command
  `python3 client.py`
- After this he will enter any of the usernames from the list of above given users.
- If he wants to send a message to a person, the format would be like:
  `username:message`
  Example- If rishabh wants to send some message to prashant then he can send it by doing `prashant:IIIT Hyderabad`
- If a user wants to see new messages that have been sent to him, he can simply type in
  `fetch`
- Only those messages would be displayed to the user which he has not seen till now.
- We can see our identity by this command
  `who am i`
- At the end, `quit` to stop the client
