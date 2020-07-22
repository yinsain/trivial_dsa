#!/usr/bin/env python3

import sys
import math
import socket
import readline

import dsa
import messageUtils
import minilogger

MAX_SIZE = int(160)
MAX_LEN = int(1024)
PORT = int(9292)
HOST = ''
ml = minilogger.minilogger('client.log')

def getlocalip(h):
    # tries to retrieve local ip in respect to server
    try:
        global PORT, HOST
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((h, PORT))
        return s.getsockname()[0]
    except:
        return HOST

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('[!] Provide host to connect')
        exit()

    else:
        # Assigning a global HOST var
        HOST = sys.argv[1]
        LOCAL = getlocalip(HOST)
        ml.writer(("[!] Verifying Server : " + HOST + ", Signing Client : " + LOCAL), 0)

        # just a banner
        print('[!] Digital Signature Scheme ')
        while True:
            # single socket fd var needed for most work
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # single msg object, will manipulate this overall
            msgpkt = messageUtils.Message(HOST, LOCAL)

            # main choice op
            mch = input('[-] (S)end a msg | (E)xit : ')

            # this will allow login phase
            if mch in ['S','s']:
                print('[+] Enter message (max length : 1024, otherwise snipped)')
                msg = input('[-] Enter : ')[:MAX_LEN].strip()
                try:
                    # try for a connect to server
                    sock.connect((HOST, PORT))
                    # returns prime, key, g, y1, y2
                    q, key, g, y1, y2 = dsa.keyGeneration()
                    ml.writer("[!] Prime generated : " + str(q) + ", Key : " + str(key))
                    ml.writer("[!] Public Key elements generated : " + str(g) + ", y1 : " + str(y1) + ", y2 : " + str(y2))
                    # mould msg object for public element sharing
                    # and serialize for network op
                    msgpkt.createPubKeyMsg(q, g, y1, y2)
                    mpub = msgpkt.packMessage()
                    ml.writer("[!] PUBLIC ELEMENTS MSGPKT : " + str(mpub))
                    # trying to sign the msg
                    r, c, s = dsa.signatureGeneration(msg, g, key, q, y1, y2)
                    ml.writer("[!] Signature generated - Key r : " + str(r) + ", C : " + str(c) + ", S : " + str(s))
                    print("[!] Signature generated - C : " + str(c) + ", S : " + str(s))

                    ## tampering feature
                    tamper = input('[-] Tamper the msg (y/n) - ')
                    if tamper in ['Y', 'y']:
                        msg = msg + 'sdfsdfsdfsdfsdf'
                    else:
                        pass
                    # and construct a msgpacket for signed msg
                    msgpkt.createSignedMsg(q, g, y1, y2, msg, c, s)
                    msigned = msgpkt.packMessage()
                    ml.writer("[!] SIGNED MSG MSGPKT : " + str(msigned))
                    sock.sendall(mpub.encode())
                    sock.sendall(msigned.encode())
                    # unserialize the response
                    msgvr = sock.recv(2048).decode().strip()
                    ml.writer("[!] VERIFICATION STATUS : " + str(msgvr))
                    msgexp = msgpkt.unpackMessage(msgvr)
                    if msgexp[10] in [True, 'True']:
                        print('[!] Signature verification successful')
                        ml.writer('[!] Signature verification successful')
                    else:
                        print('[!] Signature verification failed')
                        ml.writer('[!] Signature verification failed')
                except socket.error:
                    print('[!] Verifying Server seems offline : ' + HOST)

                finally:
                    # ending registration session and socket
                    print('[+] Closing Session')
                    ml.writer('[+] Session closed')
                    sock.close()

            elif mch in ['E','e']:
                exit()

            else:
                print('[!] Wrong input try again')
