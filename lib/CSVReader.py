#!/usr/bin/env python3

import sys
import csv
import io
import requests
from .ResponsablesPublics import ResponsablesPublics
from .Report import Report

class CSVReader:
    _hatvp_list = 'https://www.hatvp.fr/livraison/opendata/liste.csv'

    def __init__(self, args):
        self._args = args

    def run(self):
        r = 0
        if self._args.input:
            r = self._open(self._args.input)
        else:
            r = self._fetch()
        return r

    def _fetch(self):
        r = requests.get(CSVReader._hatvp_list)
        return self._parser(io.StringIO(r.text))

    def _open(self, filename):
        with open(filename, 'r', encoding='utf-8-sig') as file_handle:
            return self._parser(file_handle)

    def _parser(self, file_handle):
        firstLine = True
        resps = ResponsablesPublics()
        csvreader = csv.reader(file_handle, delimiter=';', quotechar='"')
        for line in csvreader:
            if firstLine:
                resps.set_header(line)
                firstLine = False
                continue
            resps.new_entry(line)
        return self._report(resps)

    def _report(self, resps):
        try:
            handle = None
            if self._args.output:
                handle = open(self._args.output, 'w')
            else:
                handle = sys.stdout

            r = Report(handle, self._args.format)
            r.generate(resps)

            return 0

        finally:
            if self._args.output:
                handle.close()
