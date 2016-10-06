import java.net.*;
import java.io.*;
import java.util.*;
public class ProxyThread extends Thread {
	private Socket clientSocket;
	private Socket serverSocket;
	public ProxyThread(Socket socket){
		super("proxythread");
		clientSocket = socket;
	}
	public void run(){
		try{
			//Gets response from client
			final InputStream inFromClient = clientSocket.getInputStream();
			final OutputStream outToClient = clientSocket.getOutputStream();
			
			byte[] clientinputBytes = new byte[10000];
			byte[] clientoutputBytes = new byte[10000];
			byte[] serverinputBytes = new byte[10000];
			byte[] serveroutputBytes = new byte[10000];

			int clientsize = inFromClient.read(clientinputBytes);
			System.out.println(clientsize);
			StringBuilder hostname = new StringBuilder();
			int slashcounter = 0;
			boolean thirdslashfound = false;
			int outputbytecounter = 4;
			serveroutputBytes[0]= 'G';
			serveroutputBytes[1]='E';
			serveroutputBytes[2]='T';
			serveroutputBytes[3]=' ';
			for (int i = 0; i < clientsize; i++){
				System.out.print((char)clientinputBytes[i]);
				if((char)clientinputBytes[i]== '/'){
					slashcounter++;
					if(slashcounter == 3)
						thirdslashfound=true;
				}					
				if(!thirdslashfound){
					if(i>10)
						hostname.append((char)clientinputBytes[i]);
				}	
				else{
					serveroutputBytes[outputbytecounter]=clientinputBytes[i];
					outputbytecounter++;
				}
			}
			
			/**for (int j = 0; j<outputbytecounter; j++)
				System.out.print((char)serveroutputBytes[j]);
			*/
			StringBuilder out = new StringBuilder();
			for(int i = 0; i< outputbytecounter; i++){
				out.append((char)serveroutputBytes[i]);
			}
			//System.out.println(outputbytecounter);
			//System.out.println(out.length());
			//System.out.println(out.toString());
			for(int i =0; i< outputbytecounter; i++){
				if(i+9 < outputbytecounter && 
						out.substring(i, i+10).equalsIgnoreCase("keep-alive")){
					out.replace(i, i+10, "closed");
					break;
				}
			}
			//System.out.println(out.toString());
			
			for(int i = 0; i< out.length(); i++){
				serveroutputBytes[i]=(byte) out.charAt(i);
				System.out.print((char)serveroutputBytes[i]);
			}
			
			System.out.println("\n\n\n\n"+hostname.toString());
			InetAddress address = InetAddress.getByName(hostname.toString()); 
			System.out.print(address.getHostAddress()+"\n\n\n"); 
			
			serverSocket = new Socket(address,80);
			
			InputStream inFromServer= serverSocket.getInputStream();
			OutputStream outToServer= serverSocket.getOutputStream();
			outToServer.write(serveroutputBytes);
			
			int serverbytes;
			
			while(	(serverbytes = inFromServer.read(serverinputBytes)) != -1){
				for(int i=0; i < serverbytes; i++)
					System.out.print((char)serverinputBytes[i]);
				outToClient.write(serverinputBytes,0, serverbytes);
				outToClient.flush();
			}
			

			outToClient.close();
			System.out.println(serverbytes);
			
			clientSocket.close();
			serverSocket.close();	
		}catch(Exception e){System.out.println(e);}
	}
}