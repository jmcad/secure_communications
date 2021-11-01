from flask import Flask, render_template, redirect
from flask.globals import request
from flask.helpers import url_for
from diffie_hellman import DH
import sdes, csprng
import requests


app = Flask(__name__)

shared_base = 5     # g
shared_prime = 23   # p
alice_private = 6 
alice = DH(shared_base, shared_prime, alice_private) #randint, prime, private key

ct = []
KEY = []

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        binary_text = request.form["binarytext"]
        shared_key = request.form["key"]
        split_strings = []
        n = 8
        for i in range(0, len(binary_text), n):
            split_strings.append(binary_text[i : i + n])
        
        # encryption
        encrypted_text = []
        for x in split_strings:
            encrypted_text.append(sdes.encrypt(shared_key, x))
        ciphertext = ''.join(encrypted_text)
        ct.append(ciphertext)

        return redirect(url_for("success"))
    else:
        return render_template("index.html")

@app.route("/alicepub")
def genalicepub():  
    x_alice = alice.gen_pubkey()
    return f"{x_alice}"

@app.route("/success")
def success():
    return "<h1>Successfully sent!</h1>"

@app.route("/encmsg")
def encmsg():
    string = ""
    for i in ct:
        string += i
    return f'{string}'

@app.route("/getpub")
def getpub():
    rbob = requests.get("http://127.0.0.1:5000/bobpub")
    pub_bob = int(rbob.text)
    k_alice = alice.gen_secret(pub_bob)
    decimaltobinary = bin(k_alice).replace("0b", "")
    new_key = [ord(c) for c in decimaltobinary]
    keystream = csprng.rc4(new_key, 2)
    keystream = [bin(k).replace("0b", "") for k in keystream]
    K = ''.join(keystream)
    KEY.append(K)
    return f'Your Shared Key is {K}'

@app.route("/getmsg")
def getmsg():
    # gets the message and decrypt it
    renc = requests.get("http://127.0.0.1:5000/encmsg")
    encrypted_text = renc.text

    deciphered_text = []
    split_strings = []
    
    KEYSHARED = ""
    for i in KEY:
        KEYSHARED += i

    n = 8
    for i in range(0, len(encrypted_text), n):
        split_strings.append(encrypted_text[i : i + n])

    for x in split_strings:
        deciphered_text.append(sdes.decrypt(KEYSHARED, x))
    
    for i, x in enumerate(deciphered_text):
        deciphered_text[i] = chr(int(x, 2))
    
    originaltext = "".join(deciphered_text)
    return f"{originaltext}"

if __name__ == "__main__":
    app.run(debug=True, threaded=True)