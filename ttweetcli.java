import java.net.*;
import java.io.*;
import java.util.Scanner;

/**
 * Client sided class that sends commands to server and receives server-sided results
 */
public class ttweetcli
{
    // initialize socket and input output streams
    private Socket socket;
    private DataInputStream  dataInput;
    private DataOutputStream out;
    String command;
    // constructor to put ip address and port

    /**
     * Constructor to create client
     * @param address IP address to connect to
     * @param port port number to connect to
     * @param username username of the client
     */
    public ttweetcli(String address, int port, String username) {
        // establish a connection
        try {
            Scanner scan = new Scanner(System.in);
            try {
                socket = new Socket(address, port);
            } catch (ConnectException ex) {
                System.out.println("Connection refused. Check input IP or port.");
            }
            // takes input from terminal
            dataInput = new DataInputStream(socket.getInputStream());

            // sends output to the socket
            out = new DataOutputStream(socket.getOutputStream());
            out.writeUTF(username);

            //reads and writes data
            while (true) {
                System.out.println(dataInput.readUTF());
                System.out.println(dataInput.readUTF());
                String tosend = scan.nextLine();
                out.writeUTF(tosend);


            }
        } catch (UnknownHostException u) {
            System.out.println(u);
        } catch (IOException i) {
            System.out.println(i);
        }
    }


    public static void main(String args[])
    {
        int port = Integer.parseInt(args[1]);
        ttweetcli client = new ttweetcli(args[0], port, args[2]);
        //ttweetcli client = new ttweetcli("127.0.0.1", 5000, "mseo31");
    }
}