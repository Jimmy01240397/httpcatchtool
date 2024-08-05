import socket
import sys
import ssl
import io
import dpkt.http

buffer_size = 65535

if len(sys.argv) <= 1:
    print(f"usage: {sys.argv[0]} <port> <ssl> <cert> <key>")
    exit()


def readhttp(conn):
    conn.settimeout(1)
    data = conn.recv(8192)
    if len(data) == 0:
        raise Exception()
    buf = io.BytesIO(data)
    buf.readline()
    header = dpkt.http.parse_headers(buf)
    if 'content-length' in header:
        contentlen = int(header['content-length'])
        nowlen = len(buf.read())
        buf = io.BytesIO()
        buf.write(data)
        while contentlen - nowlen != 0:
            nowdata = conn.recv(contentlen - nowlen)
            tmplen = len(nowdata)
            if tmplen == 0:
                raise Exception()
            buf.write(nowdata)
            nowlen += tmplen
        data = buf.getvalue()
    conn.settimeout(None)
    try:
        print(data.decode())
        pass
    except:
        print(data)
        pass
    return data

port = int(sys.argv[1])
usessl = len(sys.argv) > 2 and sys.argv[2] == 'true'

lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if usessl:
    cert = sys.argv[3]
    key = sys.argv[4]
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, key)
    lis = context.wrap_socket(lis, server_side=True)
lis.bind(('', port))
lis.listen(0)

while True:
    try:
        with lis.accept()[0] as conn:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                init = False
                while True:
                    data = readhttp(conn)

                    if not init:
                        req = dpkt.http.Request()
                        req.unpack(data)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        if usessl:
                            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                            sock = context.wrap_socket(sock, server_hostname=req.headers['host'])
                        sock.connect((req.headers['host'], port))
                        init = True
                    sock.send(data)
                    data = readhttp(sock)
                    conn.send(data)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
        pass

