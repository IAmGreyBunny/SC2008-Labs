import java.io.IOException;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Rfc865UdpServer {
    // Parameters
    static final int clientPortNumber = 8888;
    static final int serverPortNumber = 17;
    static final String serverIp = "192.168.1.17";

    // 1. Open UDP socket
    static DatagramSocket socket;

    public static void main(String[] argv) {

        // 1. Open UDP socket at well-known port
        try {
            socket = new DatagramSocket(serverPortNumber);
        }
        catch (SocketException e)
        {
        }

        while (true) {
            try {
                System.out.println("Listening...");

                // 2. Listen for UDP request from client
                byte[] messageBuffer = new byte[1024];
                DatagramPacket request = new DatagramPacket(messageBuffer, messageBuffer.length);
                socket.receive(request);
                String message = new String(request.getData(),request.getOffset(),request.getLength(), StandardCharsets.US_ASCII);
                System.out.println("Messaged Received: " + message);


                // 3. Send UDP reply to client
                DatagramPacket reply = new DatagramPacket(messageBuffer, messageBuffer.length, request.getAddress(), clientPortNumber);
                socket.send(reply);
                String replyMessage = new String(reply.getData(),reply.getOffset(),reply.getLength(), StandardCharsets.US_ASCII);
                System.out.print("Reply Sent: " + replyMessage);

            }
            catch (IOException e) {
            }
        }
    }
}