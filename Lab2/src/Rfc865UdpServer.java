import java.io.IOException;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Rfc865UdpServer {
    static DatagramSocket socket;
    public static void main(String[] argv) {
        //
        // 1. Open UDP socket at well-known port
        //
        try {
            socket = new DatagramSocket(8888);
        }
        catch (SocketException e)
        {
        }

        while (true) {
            try {
                //
                // 2. Listen for UDP request from client
                //
                System.out.println("Listening...");
                byte[] messageBuffer = new byte[1024];
                DatagramPacket request = new DatagramPacket(messageBuffer, messageBuffer.length);
                socket.receive(request);

                //
                // 3. Send UDP reply to client
                //
                DatagramPacket reply = new DatagramPacket(messageBuffer, messageBuffer.length, request.getAddress(), 17);
                socket.send(reply);
                String replyMessage = new String(reply.getData(),reply.getOffset(),reply.getLength(), StandardCharsets.US_ASCII);
                System.out.print(replyMessage);

            }
            catch (IOException e) {
            }
        }
    }
}