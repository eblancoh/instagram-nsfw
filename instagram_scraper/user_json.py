#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import datetime as dt
import argparse
import configparser

class jsonProcessor(object):
    
    def __init__(self, user):
        self.info_dir = os.path.dirname(os.path.abspath(__file__))
        self.user = user
    
    def locations(self):
        # read file
        with open(os.path.join(self.info_dir, str(self.user), str(self.user) +'.json'),  encoding="utf8") as myfile:
            metadata = myfile.read()

        # Parseamos el fichero
        metadata = json.loads(metadata)

        # Extracción de las localizaciones disponibles y de sus timestamps
        minkowski_stalker = dict()
        minkowski_stalker["journey"] = []
        for obj in metadata["GraphImages"]:
            if obj["location"] is not None:
                media_loc = dict()
                media_loc["location"] = obj["location"]
                media_loc["timestamp_unix"] = obj["taken_at_timestamp"]
                media_loc["timestamp_human"] = dt.datetime.fromtimestamp(obj["taken_at_timestamp"]).strftime('%Y-%m-%dT%H:%M:%S%Z')
                minkowski_stalker["journey"].append(media_loc)
            else:
                continue

        for obj in minkowski_stalker["journey"]:
            obj["location"]["address_json"] = json.loads(str(obj["location"]["address_json"]))

        return minkowski_stalker
    
def main():
    parser = argparse.ArgumentParser(
        description="Provides json summary on location history of scarpped users.")
    parser.add_argument('--username', '-u', default=None, help='Username to obtain summary.')

    args = parser.parse_args()

    if not args.username :
        raise ValueError('Must provide username [!]')
    
    history = jsonProcessor(args.username).locations()
    print(history)

if __name__ == '__main__':
    main()