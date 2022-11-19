import time
import socket
import struct


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def take_photo(cl):
    # Get header with number of bytes
    header = cl.recv(4)
    nBytes = struct.unpack('!i', header)[0]

    # Receive actual image
    img = recvall(cl, nBytes)
    return img


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 24999))
s.listen(1)

while True:
    cl_image, addr = s.accept()
    break

while True:
    try:
        # Request image by sending a single byte
        cl_image.sendall(b'1')
        photo = take_photo(cl_image)
        time.sleep(1)
        print(f'SERVER: photo received, {len(photo)} bytes')

    except KeyboardInterrupt:
        print("error")
        s.close()
