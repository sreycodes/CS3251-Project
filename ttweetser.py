import socket
import sys
import argparse
import logging

users = {}

class Tweet:
    body, user, hashtag, hashtags

    __init__(self, body, user, hashtag):
        self.body = body
        self.user = user
        self.hashtag = hashtag # Single string used to display
        self.hashtags = hashtag.split('#')[1:] # Array of all hashtags used in computation

class User:
    username, tweets, subscriptions, timeline

    __init__(self, username):
        self.username = username
        self.tweets = []
        self.subscriptions = []

    add_tweet(self, tweet):
        self.tweets.append(tweet)

    subscribe(self, hashtag):
        if (len(self.subscriptions) < 3):
            self.subscriptions.append(hashtag[1:])
            return True
        return False

    unsubscribe(self, hashtag):
        self.subscriptions.remove(hashtag[1:])

    add_to_timeline(self, tweet):
        timeline.append(tweet)




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
        mode = connection.recv(1).decode()
        print(mode)
        if mode == 'd':
            logging.info('Client wishes to download the message on the server')
            if current_msg is None:
                connection.send('013'.encode()) # 13 is the size of the empty message    
                connection.send('Empty message'.encode())
            else:
                connection.send(('%03d' % len(current_msg)).encode()) #Always format size as 3 characters
                connection.send(current_msg.encode())
        elif mode == 'u':
            logging.info('Client wishes to upload message. Checking size first')
            size = int(connection.recv(3).decode())
            if size > char_lim:
                logging.warning('Protocol Error: Client wishes to send message greater than character limit')
                connection.send('NA'.encode())
                print('Cant upload messages with size greater than ', char_lim)
            else:
                logging.info('Size within limit - %d', size)
                connection.send('OK'.encode())
                current_msg = connection.recv(size).decode()
                logging.info('Client message received')
        else:
            logging.warning('Protocol error: Invalid mode %s', mode)
    except Exception as e:
        logging.error('Error in receiving or sending data from/to %s error - %s', client_addr,  e)
    finally:
        connection.close()
        logging.info('Connection closed with %s', client_addr)


# Creates a new user upon the connection of a new client
def new_user(username):
    if not username in users:
        users[username] = User(username)
        return True
    return False

# Creates a new tweet
def new_tweet(username, body, hashtag):
    tweet = Tweet(body, username, hashtag)
    users[username].add_tweet(tweet)
    for user in users:
        for tweet_hashtag in tweet.hashtags:
            if tweet_hashtag in users[user].subscriptions:
                users[user].add_to_timeline(tweet)

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
def close_user(username):
    users.pop(username, None)