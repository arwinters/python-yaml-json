#!/usr/bin/python3
import json
import sys
import os
import collections
from collections import OrderedDict
import argparse
import ruamel.yaml
from ruamel.yaml.error import YAMLError
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scalarstring import PreservedScalarString, SingleQuotedScalarString
from ruamel.yaml.compat import string_types, MutableMapping, MutableSequence

yaml = ruamel.yaml.YAML()

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,
                    help="input file")
parser.add_argument("output", type=str,
                    help="output file")

args = parser.parse_args()


class OrderlyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, collections.abc.Mapping):
            return OrderedDict(o)
        elif isinstance(o, collections.abc.Sequence):
            return list(o)
        return json.JSONEncoder.default(self, o)


def preserve_literal(s):
    return PreservedScalarString(s.replace('\r\n', '\n').replace('\r', '\n'))


def walk_tree(base):
    if isinstance(base, MutableMapping):
        for k in base:
            v = base[k]  # type: Text
            if isinstance(v, string_types):
                if '\n' in v:
                    base[k] = preserve_literal(v)
                elif '${' in v or ':' in v:
                    base[k] = SingleQuotedScalarString(v)
            else:
                walk_tree(v)
    elif isinstance(base, MutableSequence):
        for idx, elem in enumerate(base):
            if isinstance(elem, string_types):
                if '\n' in elem:
                    base[idx] = preserve_literal(elem)
                elif '${' in elem or ':' in elem:
                    base[idx] = SingleQuotedScalarString(elem)
            else:
                walk_tree(elem)


def parseyaml(infile, outfile):

    with open(infile, 'r') as stream:
        try:
            datamap = yaml.load(stream)
            with open(outfile, 'w') as output:
                output.write(OrderlyJSONEncoder(indent=2).encode(datamap))
        except YAMLError as exc:
            print(exc)
            return False
    print('Your file has been converted.\n\n')


def parsejson(infile, outfile):

    with open(infile, 'r') as stream:
        try:
            datamap = json.load(stream, object_pairs_hook=CommentedMap)
            walk_tree(datamap)
            with open(outfile, 'w') as output:
                yaml.dump(datamap, output)
        except YAMLError as exc:
            print(exc)
            return False
    print('Your file has been converted.\n\n')


def main(infile, outfile):

    infile_type = os.path.splitext(infile)[1].replace('.', '').upper()
    outfile_type = os.path.splitext(outfile)[1].replace('.', '').upper()

    if str(infile_type) == str('YML') or str('YAML') and str(outfile_type) == str('JSON'):
        print("Convert YAML to JSON")
        parseyaml(infile, outfile)

    if str(infile_type) == str('JSON') and str(outfile_type) == str('YML') or str(outfile_type) == str('YAML'):
        print("Convert JSON to YAML")
        parsejson(infile, outfile)


if __name__ == '__main__':
    sys.exit(main(args.input, args.output))
