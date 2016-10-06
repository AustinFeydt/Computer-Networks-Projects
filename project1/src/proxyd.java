	/**@author Austin Feydt
	 * 3/22/2016
	 * EECS 425
	 * Project 1
	 * This program emulates a simply HTTP proxy*/

import java.net.*;
import java.io.*;
public class proxyd {
	public static void main(String[] args) throws IOException {
		ServerSocket serverSocket = null;
	    boolean listening = true;
	    int counter = 0;

	    int port = 5506;	//default
	    try {
	        serverSocket = new ServerSocket(port);
	        System.out.println("Started on: " + port);
	    } catch (IOException e) {
	        System.out.println(e);
	        System.err.println("Could not listen on port: ");
	        System.exit(-1);
	    }

	        while (listening) {
	            new ProxyThread(serverSocket.accept()).start();
	        }
	        serverSocket.close();
	    }

}
