import csv
import os

FILE_NAME = "veremi_output_dataset.csv"


def save_to_dataset(bsm, decision):

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='') as file:

        writer = csv.writer(file)

        # Write headers once
        if not file_exists:

            writer.writerow([

                "vehicle_id",

                "type",

                "rcvTime",

                "pos_0",
                "pos_1",

                "spd_0",
                "spd_1",

                "attack",

                "attack_type",

                "decision"
            ])

        # Write data row
        writer.writerow([

            bsm["vehicle_id"],

            bsm["type"],

            bsm["rcvTime"],

            bsm["pos_0"],
            bsm["pos_1"],

            bsm["spd_0"],
            bsm["spd_1"],

            bsm["attack"],

            bsm["attack_type"],

            decision
        ])