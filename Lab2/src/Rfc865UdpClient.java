import java.io.Console;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;

public class Rfc865UdpClient {
    // Parameters
    static final int clientPortNumber = 8888;
    static final int serverPortNumber = 17;
    static final String serverIp = "192.168.1.17";

    // 1. Open UDP socket
    static DatagramSocket socket;

    public static void main(String[] argv) {
        // Initialise Datagram Socket
        try {
            socket = new DatagramSocket(clientPortNumber);
        }
        catch(SocketException e) {}

        try {
            String sendMessage = "Hello";

            // 2. Send UDP request to server
            byte[] sendMessageBuffer = sendMessage.getBytes();
            InetAddress addr = InetAddress.getByName(serverIp);
            DatagramPacket request = new DatagramPacket(sendMessageBuffer, sendMessageBuffer.length,addr,serverPortNumber);
            socket.send(request);
            System.out.println("Message Sent: " + sendMessage);

            // 3. Receive UDP reply from server
            byte[] replyMessageBuffer = new byte[1024];
            DatagramPacket response = new DatagramPacket(replyMessageBuffer,replyMessageBuffer.length);
            socket.receive(response);
            //Decode Reply
            String replyMessage = new String(response.getData(),response.getOffset(),response.getLength(), StandardCharsets.US_ASCII);
            System.out.print("Message Received: " + replyMessage);
        }
        catch (IOException e) {}
    }
}