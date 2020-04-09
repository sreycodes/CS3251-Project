Names - Sreyans Sipani, Brock Smith, Yash Vaidya
Class Name - CS 3251
Assignment Title - Programming Assignment 2
Date - Apr 9 2020

Division of Work:
Sreyans Sipani - Handled the communication between the Client and the Server
Brock Smith - Handled input on the client side and the backend functionality needed by the Server
				to process new commands
Yash Vaidya - Started working on Java version when we couldn't get Python version working at first, tested code

Files:
1. ttweetser.py - This is the server code. It runs till one manually stops the process.
2. ttweetcli.py - This is the client CLI to use to upload and donwload messages from the server.

Instructions:
Server: 
Run command: python ttweetser.py <Port>
Usage: <Port> is a compulsory argument

Client:
Run command: python ttweetcli.py <ServerIP> <ServerPort> <Username>
Usage: All are compulsory arguments. <ServerIP> and <ServerPort> are the IP address and the Port
number of the ttweet server and <Username> is the client's username, which mus be unique. This will
start the client and connect it to the server, then the following commands can be used.

tweet <Tweet> <Hashtag>
				Send a new tweet to the server with the body <Tweet> and the hashtag <Hashtag>
subscribe <Hashtag>
				Subscribe the client to the hashtag <Hashtag> so that they receive all future
				tweets with the hashtag <Hashtag>
unsubscribe <Hashtag>
				Unsubscribe the client from the hashtag <Hashtag> so that they stop receiving
				future tweets with the hashtag <Hashtag>
timeline
				Print all tweets that the client is or has been subscribed to
getusers
				Print all of the currently connected user's usernames
gettweets <Username>
				Print all of the tweets sent by the user with the username <Username>
exit
				Closes the connection and removes the user from the server

Note - Both processes log to their own respective files.

Dependent Packages:
None