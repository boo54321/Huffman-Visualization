import socket

if __name__ == '__main__':
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    Socket.bind(("127.0.0.1", 1236))
    A = ("127.0.0.1", 1215)
    Buffer = int()
    while True:
        Dict = dict()
        print("Waiting for message!!")
        Message = Socket.recvfrom(65535)[0]
        DictStr = Socket.recvfrom(65535)
        DictStr = DictStr[0].decode("utf-8")
        print("Size of the Compressed message: {}".format(len(Message)))
        print("Compressed Message : {}".format(Message))
        Dict.update(eval(DictStr))
        Dict = dict(sorted(Dict.items(), key=lambda a: int(a[1], 2), reverse=True))
        print(Dict)
        Dict = dict([(v, k) for k, v in Dict.items()])
        print(Dict)
        print("Raw Message---->>>> {}".format(Message))
        Message = str(bin(int().from_bytes(Message, "big")))[3:]
        print("Bit Message --->>>> {}".format(Message))
        Buffer = ""
        DecompressedMessage = ""
        for i in Message:
            Buffer += i
            if Dict.get(Buffer) is not None:
                DecompressedMessage += Dict.get(Buffer)
                # print(Buffer)
                Buffer = ""
        print("Size of the Decompressed Message -->>>> {}".format(len(DecompressedMessage)))
        print("Decompressed Message -->>>> {}".format(DecompressedMessage))
