#!/usr/bin/python
# -*- encoding:utf-8 -*-

# Required parameters:
#   csv:    CSV file to read in
#   xml:    XML file to export to
#
# Optional parameters:
#   sep:    separator, default ','
#   keys:   keys to export, default '' (all)
#   root:   root node name, default 'rows'
#   item:   item node name, default 'row'

import ast
import csv
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv', type=str, required=True, help='CSV file to read')
    parser.add_argument('-x', '--xml', type=str, required=True, help='XML file to export to')
    parser.add_argument('-s', '--sep', type=str, required=False, default=',', help='Separator, default: ","')
    parser.add_argument('-k', '--keys', type=str, required=False, default='', help='Keys to export, comma separate, default: "" (all)')
    parser.add_argument('-r', '--root', type=str, required=False, default='rows', help='root node name, default: "rows"')
    parser.add_argument('-i', '--item', type=str, required=False, default='row', help='item node name, default: "row"')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    xml_file = open(args.xml, mode='w')
    csv_file = open(args.csv, mode='r')
    csv_reader = csv.DictReader(csv_file,  delimiter = args.sep)

    if args.keys == '':
        keys = csv_reader.fieldnames
    else:
        keys = args.keys.split(',')

    xml_file.write('<?xml version="1.0"?>' + "\n")
    xml_file.write("<{}>\n".format(args.root))
    for row in csv_reader:
        item = '<{}'.format(args.item)
        for key in keys:
            if key in row:
                item += ' {}="{}"'.format(key, row[key])
        item += "/>\n"
        xml_file.write(item)
    xml_file.write("</{}>".format(args.root))

    xml_file.close()