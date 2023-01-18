# IAS - Assignment-2:

# Simple Remote Procedure Solution (CLI based)

# Instructions

- I've hardcoded 5 users namely prashant, ujjwal, raghav, priyank and rishabh. The password for each of the user is same as their usernames.
- we can perform four operations :-
- Addition
- Subtraction
- Multiplication
- Division

- First user has to run the server using the command
  `python server.py`
- Then user has to run the client using the command
  `python client.py`
- After this he will enter any of the usernames from the list of above given users.
- If clientA wants clientB to sub up 6 and 2 then he will send,
  `clientB:sub:6:2`
  same for add , mul and div
- To process all the requests pending against any client, the client will type the command
  enter command `process`
- To fetch the results, the client will type the command
  `fetch`
- To quit, the client will type the command
  `quit`
