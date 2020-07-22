#!/usr/bin/env python3

OP = {
    'PUBKEY'    :     10,
    'SIGNEDMSG' :     20,
    'VERSTATUS' :     30
}

class Message:
    def __init__(self, HOST, LOCAL):
        # empty msg structure with all None
        self.msgbody = [None] * 12
        self.msgbody[2] = str(HOST)
        self.msgbody[1] = str(LOCAL)

    def createPubKeyMsg(self, q, g, y1, y2):
        self.msgbody[0] = str(OP['PUBKEY'])
        self.msgbody[3] = str(q)
        self.msgbody[4] = str(g)
        self.msgbody[5] = str(y1)
        self.msgbody[6] = str(y2)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(None)
        self.msgbody[9] = str(None)
        self.msgbody[10] = str(None)
        self.msgbody[11] = str(None)

    def createSignedMsg(self, q, g, y1, y2, msg, c, s):
        self.msgbody[0] = str(OP['SIGNEDMSG'])
        self.msgbody[3] = str(q)
        self.msgbody[4] = str(g)
        self.msgbody[5] = str(y1)
        self.msgbody[6] = str(y2)
        self.msgbody[7] = str(msg)
        self.msgbody[8] = str(c)
        self.msgbody[9] = str(s)
        self.msgbody[10] = str(None)
        self.msgbody[11] = str(None)

    def createVerstatus(self, q, g, y1, y2, c, s, status):
        self.msgbody[0] = str(OP['VERSTATUS'])
        self.msgbody[3] = str(q)
        self.msgbody[4] = str(g)
        self.msgbody[5] = str(y1)
        self.msgbody[6] = str(y2)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(c)
        self.msgbody[9] = str(s)
        self.msgbody[10] = str(status)
        self.msgbody[11] = str(None)

    def packMessage(self):
        # does a string concat for data
        return '|'.join(self.msgbody)

    def unpackMessage(self, msg):
        # splits into list
        return msg.split('|')
