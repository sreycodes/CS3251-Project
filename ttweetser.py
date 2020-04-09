import socket
import sys
import argparse
import logging
import _thread

users = {}
addrs = []

class Tweet:

    def __init__(self, body, user, hashtag):
        self.body = body
        self.user = user
        self.hashtag = hashtag # Single string used to display
        self.hashtags = hashtag.split('#')[1:] # Array of all hashtags used in computation

    def __repr__(self):
        return self.user + ': "' + self.body + '" ' + self.hashtag

    def __str__(self):
        return self.user + ': "' + self.body + '" ' + self.hashtag

class User:

    def __init__(self, username, conn):
        self.username = username
        self.tweets = []
        self.subscriptions = []
        self.timeline = []
        self.conn = conn

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def subscribe(self, hashtag):
        if (len(self.subscriptions) < 3):
            self.subscriptions.append(hashtag[1:])
            return True
        return False

    def unsubscribe(self, hashtag):
        self.subscriptions.remove(hashtag[1:])

    def add_to_timeline(self, tweet):
        self.timeline.append(tweet)

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username

# Creates a new user upon the client_connection of a new client
def new_user(username, addr, conn):
    if not username in users and not addr in addrs:
        users[username] = User(username, conn)
        addrs.append(addr)
        return True
    return False

# Creates a new tweet
def new_tweet(username, body, hashtag):
    tweet = Tweet(body, username, hashtag)
    users[username].add_tweet(tweet)
    for user in users:
        messages = set()
        for tweet_hashtag in tweet.hashtags:
            if tweet_hashtag in users[user].subscriptions or 'ALL' in users[user].subscriptions:
                users[user].add_to_timeline(tweet)
                messages.add(tweet.user + ' "' + tweet.body + '" ' + tweet.hashtag)
        for message in messages:
            try:
                users[user].conn.send(('%03d' % len(message)).encode())
                users[user].conn.send(message.encode())
            except Exception as e:
                logging.error('Error sending message %s to %s', message, users[user].username)

# Gets all tweets in the specified user's timeline
def get_timeline(username):
    return users[username].timeline

# Gets all currently online usernames
def get_usernames():
    return users.keys()

# Gets all tweets by the specified user
def get_tweets_by_username(username):
    if username in users:
        return users[username].tweets
    return None

# Removes the user when the client exits
def close_user(username, addr, conn):
    users.pop(username, None)
    addrs.remove(addr)
    conn.close()

def handle_client(client_connection, username, addr):
    while True:
        try:
            command = client_connection.recv(2).decode()
            if command == "TW":
                msg_size = int(client_connection.recv(3).decode())
                msg = client_connection.recv(msg_size).decode()
                hashtag_size = int(client_connection.recv(3).decode())
                hashtag = client_connection.recv(hashtag_size).decode()
                new_tweet(username, msg, hashtag)

            elif command == "SU":
                hashtag_size = int(client_connection.recv(3).decode())
                hashtag = client_connection.recv(hashtag_size).decode()
                client_connection.send('002'.encode())
                if users[username].subscribe(hashtag):
                    client_connection.send('OK'.encode())
                else:
                    client_connection.send('NA'.encode())
                    error_msg = "operation failed: sub " + hashtag + " failed, already exists or exceeds 3 limitation"
                    client_connection.send(('%03d' % len(error_msg)).encode())
                    client_connection.send(error_msg.encode())

            elif command == "US":
                hashtag_size = int(client_connection.recv(3).decode())
                hashtag = client_connection.recv(hashtag_size).decode()
                users[username].unsubscribe(hashtag)

            elif command == "TL":
                res_timeline = get_timeline(username)
                for tweet in res_timeline:
                    message = str(tweet)
                    try:
                        users[username].conn.send(('%03d' % len(message)).encode())
                        users[username].conn.send(message.encode())
                    except Exception as e:
                        logging.error('Error sending message %s to %s', message, users[username].username)

            elif command == "GU":
                for user in get_usernames():
                    message = str(user)
                    try:
                        users[username].conn.send(('%03d' % len(message)).encode())
                        users[username].conn.send(message.encode())
                    except Exception as e:
                        logging.error('Error sending message %s to %s', message, users[username].username)

            elif command == "GT":
                req_username_size = int(client_connection.recv(3).decode())
                req_username = client_connection.recv(req_username_size).decode()
                if get_tweets_by_username(req_username) == None:
                    client_connection.send('002'.encode())
                    client_connection.send('NA'.encode())
                    error_msg = "no user " + req_username + " in the system"
                    client_connection.send(('%03d' % len(error_msg)).encode())
                    client_connection.send(error_msg.encode())
                else:
                    for tweet in get_tweets_by_username(req_username):
                        message = str(tweet)
                        try:
                            users[username].conn.send(('%03d' % len(message)).encode())
                            users[username].conn.send(message.encode())
                        except Exception as e:
                            logging.error('Error sending message %s to %s', message, users[username].username)

            elif command == "EX":
                close_user(username, addr, client_connection)
                logging.info('Connection closed with %s', addr)
                break

            else:
                logging.warning('Unknown command %s received', command)

        except Exception as e:
            logging.error('Encountered error %s. Closing connection with %s.', e, addr)
            close_user(username, addr, client_connection)
            break

logging.basicConfig(filename='server.log', level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s", filemode='w')

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
    sock.listen(5)
    logging.info('Server is listening for incoming connections') 
except Exception as e:
    logging.error('Unable to listen %s', e)
    print('Unable to listen')
    sys.exit(0)

while True: #For connections
    connection, client_addr = sock.accept()
    logging.info('Received a connection from %s', client_addr)
    try:
        size = int(connection.recv(3).decode())
        username = connection.recv(size).decode()
        if new_user(username, client_addr, connection):
            connection.send('OK'.encode())
        else:
            connection.send('NA'.encode()) #Not accepted
            connection.close()
        _thread.start_new_thread(handle_client, (connection, username, client_addr))
    except Exception as e:
        logging.error('Error in receiving or sending data from/to %s error - %s', client_addr, e)
        



