#!/usr/bin/python
# -*- encoding:utf-8 -*-

# Required parameters:
#   data:    a list of dict
#   keys:    keys to export
#   file:    file to export to
#
# Optional parameters:
#   sep:     separator, default '|'

import ast
import csv
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', type=str, required=True, help='A list of dicts')
    parser.add_argument('-k', '--keys', type=str, required=True, help='Keys to export')
    parser.add_argument('-f', '--file', type=str, required=True, help='File to export to')
    parser.add_argument('-s', '--sep', type=str, required=False, default='|', help='Separator, default: |')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    keys = ast.literal_eval(args.keys)
    data = ast.literal_eval(args.data)

    csv_file = open(args.file, 'w') 
    csv_writer = csv.writer(csv_file,  delimiter = args.sep)
    
    csv_writer.writerow(keys)
    
    for dict in data:
        values = []
        for key in keys:
            if key in dict:
                values.append(dict[key])
            else:
                values.append('')
        csv_writer.writerow(values)
    csv_file.close()
# end if __main__