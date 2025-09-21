import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;

public class Rfc865UdpClient {
    //
    // 1. Open UDP socket
    //
    static DatagramSocket socket;
    public static void main(String[] argv) {
        try {
            socket = new DatagramSocket(8888);
        } catch (SocketException e) {}
        try {
            //
            // 2. Send UDP request to server
            //
            //InetAddress addr = InetAddress.getByName("10.96.189.96");
            InetAddress addr = InetAddress.getByName("10.96.182.64");
            byte[] message = "Toh Kok Soon, SCSI, 10.91.194.183".getBytes();
            DatagramPacket request = new DatagramPacket(message, message.length,addr,17);
            socket.send(request);
            //
            // 3. Receive UDP reply from server
            //

            byte[] replyMessageBuffer = new byte[1024];
            //DatagramPacket reply = new DatagramPacket(replyMessageBuffer,replyMessageBuffer.length);
            DatagramPacket reply = new DatagramPacket(replyMessageBuffer,replyMessageBuffer.length);
            socket.receive(reply);
            String replyMessage = new String(reply.getData(),reply.getOffset(),reply.getLength(), StandardCharsets.US_ASCII);
            System.out.print(replyMessage);
        } catch (IOException e) {}
    }
}