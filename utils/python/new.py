#!/usr/bin/env python

"""
for example:

> cat new.csv 
code,parent_id,qid,name
B38M,1159293593,Q139289,Boeing 737-MAX 8
B39M,1159293593,Q139289,Boeing 737-MAX 9
B773,1159293593,Q6425,Boeing 777-300
BA11,1159294331,Q6504,British Aerospace BAC-111
BCS1,1159293829,Q426074,Airbus A220-100
CRJ2,1159293567,Q891786,Bombardier CRJ200
CRJ7,1159293567,Q962677,Bombardier CRJ700 series
E550,1159294367,Q64361995,Embraer Legacy 500
"""

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.export

import os
import sys
import logging
import csv

if __name__ == "__main__":

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-a', '--aircraft', dest='aircraft', action='store', default='/usr/local/data/sfomuseum-data-aircraft', help='...')
    opt_parser.add_option('-e', '--enterprise', dest='enterprise', action='store', default='/usr/local/data/sfomuseum-data-enterprise', help='...')    
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    options, args = opt_parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    aircraft_repo = os.path.abspath(options.aircraft)
    aircraft_data = os.path.join(aircraft_repo, "data")
    
    enterprise_repo = os.path.abspath(options.enterprise)    
    enterprise_data = os.path.join(enterprise_repo, "data")    

    exporter = mapzen.whosonfirst.export.flatfile(aircraft_data)
    
    candidates = sys.argv[1]
    fh = open(candidates, "r")

    reader = csv.DictReader(fh)

    for row in reader:

        print row
        
        parent = mapzen.whosonfirst.utils.load(enterprise_data, row["parent_id"])
        parent_props = parent["properties"]

        props = {
            "wof:name": row["name"],
            "wof:country": parent_props["wof:country"],
            "wof:hierarchy": parent_props["wof:hierarchy"],        
            "wof:placetype":"instrument",
            "wof:repo":"sfomuseum-data-aircraft",
            "mz:is_current":-1,
            "mz:is_approximate":1,
            "sfomuseum:placetype":"aircraft",
            "sfomuseum:aircraft_id":-1,
            "wof:concordances":{
                "icao:designator":row["code"],
                "wd:id":row["qid"]
            },
            "wof:parent_id": parent_props["wof:id"]
        }

        geom = parent["geometry"]

        f = {
            "type":"Feature",
            "properties":props,
            "geometry":geom
            }
        
        print exporter.export_feature(f)
        
