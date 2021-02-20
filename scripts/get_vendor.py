# Credit to prot0man for the original
# https://gist.github.com/prot0man/457f90d80be49829552587f61a61788c

"""
    Locates the x and z coordinates of the Valheim vendor and prints them
    to console.
"""
import struct
import sys
import argparse

VENDOR_ID = b"Vendor_BlackForest"
VENDOR_FMT = "<fff"

def get_vendor_coordinates(db_data):
    # find where the vendor is defined
    offset = db_data.find(VENDOR_ID)
    if offset == -1:
        raise Exception("Invalid database provided")

    # After vendor occurs, the 4 byte x, y, and z coordinates occur. increment
    # past the vendor ID
    bidx = offset + len(VENDOR_ID)
    eidx = bidx + struct.calcsize(VENDOR_FMT)
    x,y,z = struct.unpack(VENDOR_FMT, db_data[bidx:eidx])
    return x, y, z

def load_db(db_path):
    with open(db_path, "rb") as hfile:
        data = hfile.read()
    return data

def parse_args():
    parser = argparse.ArgumentParser(description="Valheim Vendor finder")
    parser.add_argument("db_path", help="The path to the Valheim database to find the vendor for")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    db_data = load_db(args.db_path)
    x, y, z = get_vendor_coordinates(db_data)
    print("Type 'goto %d %d'" % (x, z))
