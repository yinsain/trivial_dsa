#!/usr/bin/env python3

import os
import threading
import socketserver

import dsa
import minilogger
import messageUtils

MAX_SIZE = int(160)
MAX_LEN = int(1024)
PORT = int(9292)
HOST = '127.0.0.1'
ml = minilogger.minilogger('server.log')

class LoginHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # this is a universal target function for our client
        global HOST
        # initialising a blank MSG structure
        msgpkt = messageUtils.Message(self.client_address[0], HOST)
        ml.writer(('[+] Signing Client request : ' + self.client_address[0]))
        self.data = self.request.recv(2048).strip()
        msgStringPub = str(self.data, 'ascii')
        ml.writer(('[+] VERIFICATION REQUEST MSG : ' + msgStringPub))
        msgexp = msgpkt.unpackMessage(msgStringPub)
        if msgexp[0] == '10':
            # extracting global elements and publoc key
            q, g, y1, y2 = msgexp[3:7]
            ml.writer("[!] Prime received : " + str(q))
            ml.writer("[!] Public Key elements received : " + str(g) + ", y1 : " + str(y1) + ", y2 : " + str(y2))
            self.data = self.request.recv(2048)
            msgStringSignedMsg = self.data.decode().strip()
            ml.writer(('[+] SIGNED MSG RECIEVED : ' + msgStringSignedMsg))
            msgexpSignedMsg = msgpkt.unpackMessage(msgStringSignedMsg)
            if msgexpSignedMsg[0] == '20':
                q, g, y1, y2, msg, c, s = msgexpSignedMsg[3:10]
                ml.writer("[!] Signed Msg received : " + str(msg) + ", c : " + str(c) + ", s : " + str(s))
                status, A, B, cnew = dsa.signatureVerification(s, q, g, y1, y2, c, msg)
                ml.writer("[!] Verification variables generated - A : " + str(A) + ", B : " + str(B) + ", C : " + str(cnew)+ ", Status : " + str(status))
                msgpkt.createVerstatus(q, g, y1, y2, c, s, status)
                msgverstat = msgpkt.packMessage()
                self.request.send(msgverstat.encode())
                return
            else:
                return
        else:
            pass

class LoginMultiThreadEnable(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    pass

if __name__ == '__main__':
    server = LoginMultiThreadEnable((HOST, PORT), LoginHandler)
    serving_at = server.server_address
    sThread = threading.Thread(target = server.serve_forever)
    sThread.start()
    print(sThread.name, ':', serving_at)
    ml.writer((sThread.name + ':' + str(serving_at)), 0)
    HOST = serving_at[0]
