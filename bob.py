from flask import Flask, render_template, redirect, url_for, request
from diffie_hellman import DH
import sdes, csprng
import requests


app = Flask(__name__)

shared_base = 5     # g
shared_prime = 23   # p
bob_private = 190 
bob = DH(shared_base, shared_prime, bob_private) #randint, prime, private key

ct = []
KEY = dict()

def list2string(lst):
    string = ""
    for i in lst:
        string += i
    return string

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
        # clear the encrypted message array list
        # everytime the /getmsg is invoked
        ct.clear()   
        return render_template("index.html")

# generates bob's public key
@app.route("/bobpub")
def genbobpub():
    x_bob = bob.gen_pubkey()
    return f"{x_bob}"

@app.route("/success")
def success():
    return "<h1>Successfully sent!</h1>"

@app.route("/encmsg")
def encmsg():
    msg = list2string(ct)
    # clear the encrypted message array list
    ct.clear()
    return f'{msg}'

# gets the public key of the opposite side
@app.route("/getpub")
def getpub():
    try:
        ralice = requests.get("http://127.0.0.1:8000/alicepub")
        pub_alice = int(ralice.text)
        k_bob = bob.gen_secret(pub_alice)
        decimaltobinary = bin(k_bob).replace("0b", "")
        new_key = [ord(c) for c in decimaltobinary]
        keystream = csprng.rc4(new_key, 2)
        keystream = [bin(k).replace("0b", "") for k in keystream]
        K = ''.join(keystream)
        KEY["alice"] = K
    except:
        print("Something went wrong!")
    return f'Your Shared Key is {KEY["alice"]}'

@app.route("/getmsg")
def getmsg():
    # gets the message and decrypt it
    r = requests.get("http://127.0.0.1:8000/encmsg")
    encrypted_text = r.text

    deciphered_text = []
    split_strings = []

    KEYSHARED = ""
    for i in KEY["alice"]:
        KEYSHARED += i

    n = 8
    for i in range(0, len(encrypted_text), n):
        split_strings.append(encrypted_text[i : i + n])

    for x in split_strings:
        deciphered_text.append(sdes.decrypt(KEYSHARED, x))

    for i, x in enumerate(deciphered_text):
        deciphered_text[i] = chr(int(x, 2))
    
    originaltext = "".join(deciphered_text)
    return f"<h2>{originaltext}</h2>"

if __name__ == "__main__":
    app.run(debug=True, threaded=True)