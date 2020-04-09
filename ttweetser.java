import java.net.*;
import java.io.*;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.*;

/**
 * Class file that handles server sided code and creates threads for client to run
 */
public class ttweetser {
    //initialize socket and input stream 
    private Socket socket;
    private ServerSocket server;
    List<String> usernames = new ArrayList<>();
    private String clientUsername;
    private static final int MAX_CONN = 5;
    private int connCount = 0;
    HashMap<String, List<String[]>> map = new HashMap<>();
    HashMap<String, List<String>> timel = new HashMap<>();
    HashMap<String, String> diff = new HashMap<>();
    HashMap<String, String> gett = new HashMap<>();

    /**
     * Constructor to create a new instance of multithreaded server
      * @param port the port to connect to
     * @throws IOException
     */
    public ttweetser(int port) throws IOException {
        server = new ServerSocket(port);
        /**
         * Handles reading and writing of data server side
         * Performs logic check for unique username, number of connections
         */
        while (true) {
            Socket socket = null;
            try {
                socket = server.accept();

                DataInputStream dataInput = new DataInputStream(socket.getInputStream());
                DataOutputStream dataOutput = new DataOutputStream(socket.getOutputStream());
                clientUsername = dataInput.readUTF();
                if (userExists(clientUsername)) {
                    dataOutput.writeUTF("User, " + clientUsername + ", already exists! Closing connection...");
                    socket.close();
                } else if (connCount == MAX_CONN) {
                    dataOutput.writeUTF("No more connections available. Closing connection...");
                    socket.close();
                } else if(clientUsername.equals("")) {
                    dataOutput.writeUTF("error: username has wrong format, connection refused.");
                    socket.close();
                } else {
                    dataOutput.writeUTF("username: " + clientUsername + " legal, connection established.");
                    connCount += 1;
                    // Creates thread on which instance of server will run to communicate with client
                    Thread t = new ClientHandler(socket, dataInput, dataOutput, clientUsername);
                    t.start();
                }
            } catch (Exception e) {
                socket.close();
                e.printStackTrace();
            }
        }
    }

    /**
     * Handler class runs server sided code on thread
     * Reference: https://www.geeksforgeeks.org/introducing-threads-socket-programming-java/
     */
    class ClientHandler extends Thread {
        final DataInputStream dataInput;
        final DataOutputStream dataOutput;
        final Socket socket;
        final String clientUsername;
        private Map<String, Long> subList = new HashMap<String, Long>();
        private List<String> trythis = new ArrayList<>();
        boolean subbedAll = false;
        Long timeCalled = System.currentTimeMillis();

        /**
         * Constructor for new handler
         * @param socket to connect to
         * @param dataInput InputStream for reading
         * @param dataOutput OutputStream for writing
         * @param clientUsername Username of the current connection
         */
        public ClientHandler(Socket socket, DataInputStream dataInput, DataOutputStream dataOutput, String clientUsername) {
            this.socket = socket;
            this.dataInput = dataInput;
            this.dataOutput = dataOutput;
            this.clientUsername = clientUsername;
        }

        /**
         * Threaded server side logic for reading and processing commands
         */
        @Override
        public void run() {
            String received;

            while (true) {
                try {
                    //ask client for command
                    dataOutput.writeUTF("");

                    received = dataInput.readUTF();
                    //Exit logic
                    if (received.equals("exit")) {
                        dataOutput.writeUTF("Connection has been closed.");
                        usernames.remove(clientUsername);
                        subList.clear();
                        connCount--;
                        this.socket.close();
                        break;
                    }
                    //Parsing of input commands for command, message, and hashtags
                    String split[] = received.split(" ", 2);
                    String hashtag[];
                    switch (split[0]) {

                        /**
                         * Tweet command
                         */
                        case "tweet":
                        	String []re = received.split(" \"",2);
                            String hashes[] = re[1].split("\" ", 2);
                            String tags[] = hashes[1].split("#");
                            String ne = hashes[0].substring(0);
                            String[] text={ne};
                            if (text[0].length() <= 0 || text[0].length() > 150) {
                                dataOutput.writeUTF("Message must be between 1 to 150 characters.");
                                break;
                            }
                            if (tags.length > 6) {
                                dataOutput.writeUTF("Maximum of 5 hashtags allowed.");
                                break;
                            }
                            for (int i = 1; i < tags.length; i++) {
                                if (tags[i].equals("ALL")) {
                                    dataOutput.writeUTF("Cannot use #ALL as a hashtag.");
                                    break;
                                }
                                if (tags[i].length() < 1 || tags[i].length() > 14) {
                                    dataOutput.writeUTF("Hashtags must been between 2 to 15 characters.");
                                    break;
                                }
                            }
                            for (int i = 1; i < tags.length; i++) {
                                addMsgToHash(tags[i], text[0], clientUsername, hashes[1]);
                            }
                        	Iterator hmIteratorr = timel.entrySet().iterator(); 
                        	String ll="";
                        	int lmao= 0 ;
                            if(gett.containsKey(clientUsername)==false){
                                    diff.put(clientUsername,"");
                            }
                            String udp = gett.get(clientUsername);
                            if(udp==null){
                                udp="";
                            }
                            udp += clientUsername + ": \"" + text[0] + "\" " + hashes[1] + "\n";
                            gett.put(clientUsername,udp);

                            while(hmIteratorr.hasNext()) {

                                Map.Entry mapElement = (Map.Entry)hmIteratorr.next(); 
                                ll = (String)mapElement.getKey();
                                if(diff.containsKey(ll)==false){
                                	diff.put(ll,"");
                                }
                                String test = diff.get(ll);
                                List<String> subsc = timel.get(ll);
                                for(int o=0;o<subsc.size();o++){
                                	for(int k=0;k<tags.length;k++){
                                		if(subsc.get(o).equals("ALL") || tags[k].equals(subsc.get(o))){
                                			test += clientUsername + ": \"" + text[0] + "\" " + hashes[1] + "\n";
                                			break;
                                		}
                                	}
                                }
                                diff.put(ll,test);
                                }
                                

                            dataOutput.writeUTF("operation success");

                            break;

                        /**
                         * Subscribe command
                         */
                        case "subscribe":
                            if (subList.size() == 3) {
                                dataOutput.writeUTF("Cannot add anymore subscriptions. Please remove subs to add more.");
                            } else {
                                hashtag = split[1].split("#", 2);
                                if (hashtag[1].equals("ALL")) {
                                    subbedAll = true;

                                }
                                subList.put(hashtag[1], System.currentTimeMillis());
                                trythis.add(hashtag[1]);
                                timel.put(clientUsername,trythis);
                                dataOutput.writeUTF("operation success");
                            }
                            timeCalled = System.currentTimeMillis();
                            break;

                        /**
                         * Unsubscribe command
                         */
                        case "unsubscribe":
                            if (subList.isEmpty()) {
                                dataOutput.writeUTF("You are not currently subscribed to any hashtags.");
                            } else {
                                hashtag = split[1].split("#", 2);
                                if (hashtag[1].equals("ALL")) {
                                    subbedAll = false;
                                }
                                subList.remove(hashtag[1]);
                                trythis.remove(hashtag[1]);
                                timel.put(clientUsername,trythis);
                                dataOutput.writeUTF("operation success");

                            }
                            break;

                        case "getusers":
                            String msgRetur = "";
                            for(int i=0;i<usernames.size();i++){
                                msgRetur = msgRetur + usernames.get(i) + "\n";
                            }
                            dataOutput.writeUTF(msgRetur);
                            break;
                        case "gettweets":

                            if(!(usernames.contains(split[1].toLowerCase()))){
                                    dataOutput.writeUTF("No user " + split[1]+" in the system");
                                    break;
                            }
                            String llk = gett.get(split[1]);

                            dataOutput.writeUTF(llk);
                            break; 


                        /**
                         * Timeline command
                         */
                        case "timeline":
                        	if(diff.containsKey(clientUsername)==false){
                        		diff.put(clientUsername,"");
                        	}
                        	dataOutput.writeUTF(diff.get(clientUsername));
                            
                            break;



                        /**
                         * Handles all other inputs
                         */
                        default:
                            dataOutput.writeUTF("Invalid command please try again.");
                            break;
                    }

                } catch (Exception e) {
                    try {
                        socket.close();
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    }
                    e.printStackTrace();
                }
            }
        }

        /**
         * Helper function to add messages to hashmap of hashtags
         * @param hashtag the hashtag to be added to
         * @param tweetText the text of the tweet
         * @param user the original user who tweeted
         * @param originalHashes the original hashtag string
         */
        public void addMsgToHash(String hashtag, String tweetText, String user, String originalHashes) {
            String[] tweetArr = {user, tweetText, originalHashes, Long.toString(System.currentTimeMillis())};
            if (map.containsKey(hashtag)) {
                map.get(hashtag).add(tweetArr);
            } else {
                ArrayList<String[]> tweetList = new ArrayList<>();
                tweetList.add(tweetArr);
                map.put(hashtag, tweetList);
            }
        }
    }


    /**
     * Helper method to check if username is currently connected
     * @param username the username to check
     * @return true if username exists, false otherwise
     */
    public boolean userExists(String username) {
        if (usernames.contains(username.toLowerCase())) {
            return true;
        } else {
            usernames.add(username.toLowerCase());
            return false;
        }
    }


    public static void main(String args[]) throws IOException {
        //ttweetsrv server = new ttweetsrv(5000);
        ttweetser server = new ttweetser(Integer.parseInt(args[0]));
    }
} 