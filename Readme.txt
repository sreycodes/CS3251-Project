Name - Sreyans Sipani
Email - ssipani6@gatech.edu
Class Name - CS3251
Assignment Title - Programming Assignment 1
Date - Feb 12 2020

Files:
1. ttweetser.py - This is the server code. It runs till one manually stops the process.
2. ttweetcli.py - This is the client CLI to use to upload and donwload messages from the server.

Instructions:
Server: 
Run command: python ttweetser.py port
Usage: port is a compulsory argument

Client:
Run command: python ttweetcli.py [-u] [-d] ip port [message]
Usage: Set -u flag for upload and -d flag for download. ONLY one flag should be set at a time. 
ip and port are compulsory arguments. message is only used in upload mode.

Note - Both processes log to their own respective files.

Test Case Scenario: Refer Sample.txt

Protocol:
1. Client sends one character specifying the mode - 'u' or 'd'
In case of upload:
    2a. Client sends three characters (zero padded if required) specifying the size of the message.
        Eg - '013', '130', '002'
    2b. Server sends 'OK' if size is fine and 'NA' if not.
    2c. Client sends message if it doesn't receive 'NA'.
In case of download:
    3a. Server sends three characters (zero padded if required) specifying the size of the message.
        Eg - '013', '130', '002'
    3b. Server sends the message and client receives it.
4. Connection is closed.

Bugs and Limitations - 
1. The program makes more checks than required.
2. The program allows an empty string to be uploaded (i.e '') as the specification doesn't disallow
    it. When an empty string is downloaded, the program will print an empty line.