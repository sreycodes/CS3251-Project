import socket
import sys
import argparse
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

parser = argparse.ArgumentParser(description='Welcome to the server')
parser.add_argument('port', nargs=1, type=int, help='Port to start server at (preferably between 13000 and 14000')

args = parser.parse_args()
port_num = args.port[0]
server_address = ('localhost', port_num)
current_msg = None
sock = None
char_lim = 150

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    logging.info('Server started at port %d', port_num)
except Exception as e:
    logging.error('Unable to start server %s', e)
    print('Unable to start server! Exiting.')
    sys.exit(0)

try:
    sock.listen(1)
    logging.info('Server is listening for incoming connections') 
except Exception as e:
    logging.error('Unable to listen %s', e)
    print('Unable to listen')
    sys.exit(0)

while True:
    connection, client_addr = sock.accept()
    logging.info('Received a connection from %s', client_addr)

    try:
        mode = connection.recv(1)
        print(mode)
        if mode == 'd':
            logging.info('Client wishes to download the message on the server')
            if current_msg is None:
                connection.send('013') # 13 is the size of the empty message    
                connection.send('Empty message')
            else:
                connection.send('%03d' % len(current_msg)) #Always format size as 3 characters
                connection.send(current_msg)
        elif mode == 'u':
            logging.info('Client wishes to upload message. Checking size first')
            size = int(connection.recv(3))
            if size > char_lim:
                logging.warning('Protocol Error: Client wishes to send message greater than character limit')
                connection.send('NA')
                print('Cant upload messages with size greater than ', char_lim)
            else:
                logging.info('Size within limit - %d', size)
                connection.send('OK')
                current_msg = connection.recv(size)
                logging.info('Client message received')
        else:
            logging.warning('Protocol error: Invalid mode %s', mode)
    except Exception as e:
        logging.error('Error in receiving or sending data from/to %s error - %s', client_addr,  e)
    finally:
        connection.close()
        logging.info('Connection closed with %s', client_addr)