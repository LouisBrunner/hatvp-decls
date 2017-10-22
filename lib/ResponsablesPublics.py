#!/usr/bin/env python3

from .ResponsablePublic import ResponsablePublic

class ResponsablesPublics:
    def __init__(self):
        self._header = None
        self._resps = []

    def __iter__(self):
        return self._resps.__iter__()

    def set_header(self, header):
        self._header = header

    def _lookup(self, line, name):
        return line[self._header.index(name)]

    def new_entry(self, entry):
        if self._header == None:
            raise RuntimeError("le programme n'a pas trouvé d'en-tête pour décoder les informations du fichier de la HATVP")

        previousResp = self._find_resp(entry)
        if previousResp != None:
            previousResp.add_document(entry)
        else:
            self._insert_resp(entry)

    def _find_resp(self, entry):
        alphaId = self._lookup(entry, 'classement')
        for resp in self._resps:
            if alphaId == resp.alphaId:
                return resp
        return None

    def _insert_resp(self, entry):
        resp = ResponsablePublic(self, entry)
        resp.add_document(entry)
        self._resps.append(resp)
