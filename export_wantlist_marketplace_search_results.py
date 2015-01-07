# (c) 2015 by Jussi Jousimo <jvj@iki.fi>

import argparse
import csv
import urllib.request
import json
import time

parser = argparse.ArgumentParser(description='exports wantlist search results from Discogs Marketplace')
parser.add_argument('wantlist', help='exported CSV wantlist file from Discogs')
parser.add_argument('output', help='output CSV file')
args = parser.parse_args()

max_tries = 20
try_delay = 1
write_header = True

with open(args.wantlist) as wantlist_file:
    wantlist_reader = csv.reader(wantlist_file)
    next(wantlist_file)
    
    with open(args.output, "w", newline='') as output_file:
        output_writer = csv.writer(output_file)

        for record in wantlist_reader:
            artist = record[2]
            title = record[3]
            release_id = record[7]
            url = "http://api.discogs.com/marketplace/search?release_id=" + release_id
            print("Processing " + artist + " - " + title + "...") # There is some encoding problem here in Windows

            tries = 0
            while max_tries > tries:
                try:
                    with urllib.request.urlopen(url) as data:
                        result = data.read().decode()
                        items = json.loads(result)
                        
                        if write_header:
                            write_header = False
                            header = [list(items[0].keys())]
                            output_writer.writerows(header)
                            
                        for item in items:
                            row = [list(item.values())]
                            output_writer.writerows(row)
                                
                except:
                    print("Request failed. Retrying...")
                    tries += 1
                    time.sleep(try_delay)
                    continue
                else:
                    break
