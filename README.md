## Assignment - 2 SNS
#### Author - yashdeep.saini@students.iiit.ac.in
#### Topic  - Digital Signature Scheme

* A simple client server model which performs a public key and elements transfer and then by using them and it performs the signature verification whenever a new signed messsage is provided with same elements.
* Code is written in Python

#### Main code

##### Server.py
> Multithreaded server which provides signature verification

##### Run Server
```
$ ./server.sh
```
##### Client.py
> Client which provides message input, key generation and Signature generation support.

##### Run Client
```
$ ./server.sh [ IP address of server ]
```

#### Extra files

* client.log - maintains a log session for client operations.
* server.log - maintains a log session for server operations.

#### Modules

##### Dsa
> Takes care of Public key, public elements generation, signing of the message and also verification.

* modinv - calculates inverse modulo
* extended_gcd - calculates extended gcd for two inputs
* keyGeneration - generates public key elements and key.
* signatureGeneration - generates signature over provided message
* signatureVerification - performs verification over message signature with provided old values.

##### messageUtils
> all forms of packet creation is done via this module

* createPubKeyMsg - Packet for public key elements
* createSignedMsg - Packet for message and signature details
* createVerstatus - Packet for response of signature verification.
* packMessage - Trivial serialization
* unpackMessage - Trivial unserialization

##### minilogger
> provides extremely basic logging capabilities

* minilogger.writer - append or fresh log file operations

##### prime
> module to perform all prime number calculcations

* is_prime - test if prime or not
* generate_prime_number - returns a prime number
* generate_prime_candidate - limits the bound for prime number
* prim_root - calculates primitive root of the prime number provided
