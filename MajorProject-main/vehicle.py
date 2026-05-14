# vehicle.py

import csv
import random
import json
import hashlib
import requests
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


# -----------------------------------
# LOAD PRIVATE KEY
# -----------------------------------

with open("private.pem", "rb") as f:

    private_key = serialization.load_pem_private_key(

        f.read(),

        password=None
    )

# -----------------------------------
# LOAD DATASET USING CSV MODULE
# -----------------------------------

rows = []

with open("Veremi_final_dataset.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for i, row in enumerate(reader):

        rows.append(row)

        # Load only first 1000 rows
        if i >= 1000:
            break


# -----------------------------------
# CONTINUOUS BSM GENERATION
# -----------------------------------

while True:

    # Random row from dataset
    row = random.choice(rows)

    # Dynamic vehicle ID
    vehicle_id = f"CAR_{random.randint(100,999)}"

    # -----------------------------------
    # CREATE BSM
    # -----------------------------------

    bsm = {

        "vehicle_id": vehicle_id,

        "type": row["type"],

        "rcvTime": row["rcvTime"],

        "pos_0": row["pos_0"],
        "pos_1": row["pos_1"],

        "spd_0": row["spd_0"],
        "spd_1": row["spd_1"],

        "acl_0": row["acl_0"],
        "acl_1": row["acl_1"],

        "hed_0": row["hed_0"],
        "hed_1": row["hed_1"],

        "attack": row["attack"],

        "attack_type": row["attack_type"]
    }

    # -----------------------------------
    # CONVERT TO JSON
    # -----------------------------------

    bsm_json = json.dumps(bsm)

    # -----------------------------------
    # GENERATE SHA256 HASH
    # -----------------------------------

    packet_hash = hashlib.sha256(

        bsm_json.encode()

    ).hexdigest()

    # -----------------------------------
    # GENERATE DIGITAL SIGNATURE
    # -----------------------------------

    signature = private_key.sign(

        packet_hash.encode(),

        ec.ECDSA(hashes.SHA256())
    )

    # -----------------------------------
    # CREATE FINAL PACKET
    # -----------------------------------

    packet = {

        "bsm": bsm,

        "hash": packet_hash,

        "signature": signature.hex()
    }

    # -----------------------------------
    # ATTACK SIMULATION
    # -----------------------------------

    attack_mode = random.choices(

        ["normal", "tamper"],

        weights=[80, 20]

    )[0]

    # Tamper AFTER hash/signature generation
    if attack_mode == "tamper":

        tampered_bsm = packet["bsm"].copy()

        tampered_bsm["spd_0"] = "999"

        packet["bsm"] = tampered_bsm

        print("\nATTACK GENERATED : PACKET TAMPERED")

    else:

        print("\nNORMAL PACKET")

    # -----------------------------------
    # SEND PACKET TO SERVER
    # -----------------------------------

    response = requests.post(

        "http://127.0.0.1:5000/receive",

        json=packet
    )

    # -----------------------------------
    # PRINT RESPONSE
    # -----------------------------------

    print(response.json())

    print("--------------------------------------")

    # Wait
    time.sleep(2)