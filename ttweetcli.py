import socket
import sys
import argparse
import logging

logging.basicConfig(filename='CLI.log', level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

parser = argparse.ArgumentParser(description='Welcome to the client CLI')
parser.add_argument('-u', action='store_true') # To set upload mode
parser.add_argument('-d', action='store_true') # To set download mode
parser.add_argument('ip', help='Server IP to connect with')
parser.add_argument('port', type=int, help='Server Port to connect with')
parser.add_argument('message', nargs='?', help='Message to upload if -u is set', default='') #Only for upload

args = parser.parse_args()
upload = args.u
download = args.d
ip = args.ip
port_num = args.port
msg = args.message
char_lim = 150

if upload == download:
	logging.warning('Invalid combination of upload and download flags')
	print('Cannot upload and download at the same time OR no mode was set')
	sys.exit(0)
if download and msg != '':
	logging.warning('Message argument will be ignored in download mode')
if upload and len(msg) > 150:
	logging.warning('Attempted to upload message with size greater than %d', char_lim) 
	print('Cannot upload a message with size greater than ', char_lim)
	sys.exit(0)

server_addr = (ip, port_num)
sock = None
char_lim = 150

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    logging.info('Connected to requested server %s', server_addr)
except Exception as e:
    logging.error('Server %s not found - %s', server_addr, e)
    print('Server not found')
    sys.exit(0)

try:
    if upload:
        sock.send('u'.encode())
        sock.send(('%03d' % len(msg)).encode())
        ready = sock.recv(2).decode()
        if ready == 'NA':
            print('Server does not want message')
            raise Exception('Server did not want message of size %d. This should not happen.', len(msg))    
        sock.send(msg.encode())
        logging.info('Succesfully uploaded %s after receiving %s', msg, ready)
        print('Upload successful')
    else:
        sock.send('d'.encode())
        #logging.info('[client] Sent d')
        size = int(sock.recv(3).decode())
        #logging.info('[client] Received size - ', r)
        rcvd_msg = sock.recv(size).decode()
        logging.info('Succesfully received %s of size %d', rcvd_msg, size)
        print(rcvd_msg)
except Exception as e:
    logging.error('Error in receiving or sending data %s', e)
finally:
    logging.info('Closing connection/socket')
    sock.close()
    print('Thank you for using this CLI!')