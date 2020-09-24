import socket
import GreedyHuffman


def To_Bytes(S):
    return int("1" + S, 2).to_bytes((len(S)+8)//8, byteorder="big")


if __name__ == '__main__':
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    Socket.bind(("127.0.0.1", 1215))
    B = ("127.0.0.1", 1236)
    while True:
        Input = input("Enter the Message to send : ")
        print("Size of the Original message: {}".format(len(Input)))
        Input = GreedyHuffman.HuffManTree(Input)
        print("Bit String --->>> {}".format(Input[0]))
        BitString = To_Bytes(Input[0])
        print("Size of the message after applying the Huffman Alg: {}".format(len(BitString)))
        print("Bytes ---->>> {}".format(BitString))
        Socket.sendto(BitString, B)
        Socket.sendto(bytes(str(Input[1]), "utf-8"), B)


