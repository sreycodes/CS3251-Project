import socket
import sys
import argparse
import logging
import re

logging.basicConfig(filename='CLI.log', level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

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

if not re.search('^(([0-9]{1,2}|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]{1,2}|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', ip):
    print('error: server ip invalid, connection refused.')
    sys.exit(1)
if port_num < 0 or port_num > 65535:
    print('error: server port invalid, connection refused.')
    sys.exit(1)
if not re.search('^[a-zA-Z0-9]+$', username):
    print('error: username has wrong format, connection refused.')
    sys.exit(1)

server_addr = (ip, port_num)
sock = None
char_lim = 150

# try:
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect(server_addr)
#     logging.info('Connected to requested server %s', server_addr)
# except Exception as e:
#     logging.error('Server %s not found - %s', server_addr, e)
#     print('error: server ip invalid, connection refused.')
#     sys.exit(1)

while (True):
    command = input("$ ").split(' ')
    if command[0] == 'tweet':
        if len(command) != 3:
            print('error: args should contain <Tweet> <Hashtag>')
        else:
            message = command[1]
            hashtag = command[2]
            if len(message) == 0:
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


    elif command[0] == 'subscribe':
        if len(command) != 2:
            print('error: args should contain <Hashtag>')
        else:
            hashtag = command[1]
            if not re.search('^#[a-zA-Z0-9]{1,14}$', hashtag):
                print('hashtag illegal format, connection refused.')
            else: 
                pass

    elif command[0] == 'unsubscribe':
        if len(command) != 2:
            print('error: args should contain <Hashtag>')
        else:
            hashtag = command[1]
            if not re.search('^#[a-zA-Z0-9]{1,14}$', hashtag):
                print('hashtag illegal format, connection refused.')
            else: 
                pass

    elif command[0] == 'timeline':
        pass

    elif command[0] == 'getusers':
        pass

    elif command[0] == 'gettweets':
        if len(command) != 2:
            print('error: args should contain <Username>')
        else:
            username = command[1]
            if not re.search('^[a-zA-Z0-9]+$', username):
                print('error: username has wrong format, connection refused.')
            else:
                pass

    elif command[0] == 'exit':
        logging.info('Closing connection/socket')
        sock.close()
        print('bye bye')
        sys.exit(0)

    else:
        print('error: command not found')

# try:
#     if upload:
#         sock.send('u'.encode())
#         sock.send(('%03d' % len(msg)).encode())
#         ready = sock.recv(2).decode()
#         if ready == 'NA':
#             print('Server does not want message')
#             raise Exception('Server did not want message of size %d. This should not happen.', len(msg))    
#         sock.send(msg.encode())
#         logging.info('Succesfully uploaded %s after receiving %s', msg, ready)
#         print('Upload successful')
#     else:
#         sock.send('d'.encode())
#         #logging.info('[client] Sent d')
#         size = int(sock.recv(3).decode())
#         #logging.info('[client] Received size - ', r)
#         rcvd_msg = sock.recv(size).decode()
#         logging.info('Succesfully received %s of size %d', rcvd_msg, size)
#         print(rcvd_msg)
# except Exception as e:
#     logging.error('Error in receiving or sending data %s', e)
# finally:
#     logging.info('Closing connection/socket')
#     sock.close()
#     print('Thank you for using this CLI!')
