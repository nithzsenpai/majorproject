from flask import Flask, request

from database import save_to_dataset

import hashlib
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# -----------------------------------
# LOAD PUBLIC KEY
# -----------------------------------

with open("public.pem", "rb") as f:

    public_key = serialization.load_pem_public_key(

        f.read()
    )

# -----------------------------------
# RECEIVE PACKETS
# -----------------------------------

@app.route('/receive', methods=['POST'])

def receive():

    data = request.json

    bsm = data["bsm"]

    received_hash = data["hash"]

    signature = bytes.fromhex(data["signature"])

    vehicle_id = bsm["vehicle_id"]

    # -----------------------------------
    # RECALCULATE HASH
    # -----------------------------------

    recalculated_hash = hashlib.sha256(

        json.dumps(bsm).encode()

    ).hexdigest()

    # -----------------------------------
    # HASH VERIFICATION
    # -----------------------------------

    if recalculated_hash != received_hash:

        save_to_dataset(bsm, "REJECT")

        return {

            "vehicle_id": vehicle_id,

            "status": "REJECT",

            "reason": "Hash mismatch (Tampered Packet)"
        }

    # -----------------------------------
    # SIGNATURE VERIFICATION
    # -----------------------------------

    try:

        public_key.verify(

            signature,

            received_hash.encode(),

            ec.ECDSA(hashes.SHA256())
        )

    except:

        save_to_dataset(bsm, "REJECT")

        return {

            "vehicle_id": vehicle_id,

            "status": "REJECT",

            "reason": "Invalid Signature"
        }

    # -----------------------------------
    # TRUSTED PACKET
    # -----------------------------------

    save_to_dataset(bsm, "ACCEPT")

    return {

        "vehicle_id": vehicle_id,

        "status": "ACCEPT",

        
    }

# -----------------------------------
# START SERVER
# -----------------------------------

if __name__ == '__main__':

    app.run(

        host='0.0.0.0',

        port=5000
    )