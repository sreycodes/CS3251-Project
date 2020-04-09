import socket
import sys
import argparse
import logging
import re
import _thread
import shlex

def accept_message_from_server(socket):
    while True:
        try:
            _size = socket.recv(3).decode()
            size = int(_size)
            message = socket.recv(size).decode()
            if message == 'OK':
                print('operation success')
            elif message == 'NA':
                error_size = int(socket.recv(3).decode())
                error = socket.recv(error_size).decode()
                print(error)
            else:
                print(message)
        except Exception as e:
            logging.error('Encountered error %s. Closing connection', e)
            socket.close()
            sys.exit(1)

# The project doc specifies that exactly this error appears if not enough arguments are given, so the argparse default error doesn't work
if len(sys.argv) != 4:
    print('error: args should contain <ServerIP> <ServerPort> <Username>')
    sys.exit(1)

parser = argparse.ArgumentParser(description='Welcome to the client CLI')
parser.add_argument('ip', help='Server IP to connect with')
parser.add_argument('port', type=int, help='Server Port to connect with')
parser.add_argument('username', help='Username to be used to communicate with the Server')

args = parser.parse_args()
ip = args.ip
port_num = args.port
username = args.username

# Checks validity of the IP address using Regular Expression
if not re.search('^(([0-9]{1,2}|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]{1,2}|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', ip):
    print('error: server ip invalid, connection refused.')
    sys.exit(1)

# Checks validity of the Port number
if port_num < 0 or port_num > 65535:
    print('error: server port invalid, connection refused.')
    sys.exit(1)

# Checks validity of the username using regular expression
# Note: this only checks that no illegal characters were used, not that the username is unique
if not re.search('^[a-zA-Z0-9]+$', username):
    print('error: username has wrong format, connection refused.')
    sys.exit(1)

logging.basicConfig(filename='CLI-'+username+'.log', level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

server_addr = (ip, port_num)
sock = None
char_lim = 150

# Attempts to connect to the server specified by the inputted IP Address and Port number
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    logging.info('Connected to requested server %s', server_addr)
except Exception as e:
    logging.error('Server %s not found - %s', server_addr, e)
    print('error: server ip invalid, connection refused.')
    sys.exit(1)

# Sends initial message to the server to validate that the username is legal
try:
    # sock.send(('LO').encode())
    sock.send(('%03d' % len(username)).encode()) #Assuming username has less than 1000 characters
    sock.send(username.encode())
    status = sock.recv(2).decode()
    if status == 'OK':
        print('username legal, connection established.')
        # Starts a separate thread to accept messages from the server while the current thread
        # handles user input
        _thread.start_new_thread(accept_message_from_server, (sock, ))
    else:
        logging.error('username %s not accepted', username)
        print('username illegal, connection refused.')
        sys.exit(1)
except Exception as e:
    logging.error('username %s not accepted - %s', username, e)
    print('username illegal, connection refused.')
    sys.exit(1)

# Gets the commands inputted by the user
while (True):
    # Splits the input into an array representing the separate arguments
    command = shlex.split(input())
    
    if command[0] == 'tweet':
        if len(command) < 3:
            print('error: args should contain <Tweet> <Hashtag>')
        else:
            message = command[1]
            hashtag = command[2]
            if message == None or len(message) == 0:
                print('message format illegal.')
            elif len(message) > 150:
                print('message length illegal, connection refused.')
            elif not re.search('^(#[a-zA-Z0-9]{1,14}){1,5}$', hashtag):
                print('hashtag illegal format, connection refused.')
            else:
                hashtags = hashtag.split('#')[1:]
                if 'ALL' in hashtags:
                    print('hashtag illegal format, connection refused.')
                else:
                    sock.send('TW'.encode())
                    sock.send(('%03d' % len(message)).encode())
                    sock.send(message.encode())
                    sock.send(('%03d' % len(hashtag)).encode())
                    sock.send(hashtag.encode())


    elif command[0] == 'subscribe':
        if len(command) != 2:
            print('error: args should contain <Hashtag>')
        else:
            hashtag = command[1]
            if not re.search('^#[a-zA-Z0-9]{1,14}$', hashtag):
                print('hashtag illegal format, connection refused.')
            else: 
                sock.send('SU'.encode())
                sock.send(('%03d' % len(hashtag)).encode())
                sock.send(hashtag.encode())

    elif command[0] == 'unsubscribe':
        if len(command) != 2:
            print('error: args should contain <Hashtag>')
        else:
            hashtag = command[1]
            if not re.search('^#[a-zA-Z0-9]{1,14}$', hashtag):
                print('hashtag illegal format, connection refused.')
            else: 
                sock.send('US'.encode())
                sock.send(('%03d' % len(hashtag)).encode())
                sock.send(hashtag.encode())
                print('operation success')

    elif command[0] == 'timeline':
        sock.send('TL'.encode())

    elif command[0] == 'getusers':
        sock.send('GU'.encode())

    elif command[0] == 'gettweets':
        if len(command) != 2:
            print('error: args should contain <Username>')
        else:
            username = command[1]
            if not re.search('^[a-zA-Z0-9]+$', username):
                print('error: username has wrong format, connection refused.')
            else:
                sock.send('GT'.encode())
                sock.send(('%03d' % len(username)).encode())
                sock.send(username.encode())

    elif command[0] == 'exit':
        sock.send('EX'.encode())
        logging.info('Closing connection/socket')
        sock.close()
        print('bye bye')
        sys.exit(0)

    else:
        print('error: command not found')
