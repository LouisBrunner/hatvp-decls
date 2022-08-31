#!/usr/bin/env python3

class ResponsablePublic:
    _hatvp_root = 'https://www.hatvp.fr/'
    _file_address = _hatvp_root + 'livraison/dossiers/'

    def __init__(self, resps, raw):
        self._resps = resps

        # Info
        # self.styles = set()
        # self.firstNames = set()
        # self.lastNames = set()
        self.style = self._resps._lookup(raw, 'civilite')
        self.mascPronoun = self.style == 'M.'
        self.firstName = self._resps._lookup(raw, 'prenom')
        self.lastName = self._resps._lookup(raw, 'nom')
        self.photos = set()

        # self.alphaIds = set()
        # self.folders = set()
        self.alphaId = self._resps._lookup(raw, 'classement')
        self.folder = ResponsablePublic._hatvp_root + self._resps._lookup(raw, 'url_dossier')

        # Mandates
        self.mandates = {}
        self.mandateTypes = set()
        self.departements = set()

        # Documents
        self.documents = []

    def _update_info(self, raw):
        # style = self._resps._lookup(raw, 'civilite')
        # self.styles.add(style)
        # firstName = self._resps._lookup(raw, 'prenom')
        # self.firstNames.add(firstName)
        # lastName = self._resps._lookup(raw, 'nom')
        # self.lastNames.add(lastName)

        photoUrl = self._resps._lookup(raw, 'url_photo')
        if photoUrl != '':
            self.photos.add(photoUrl)

        # alphaId = self._resps._lookup(raw, 'classement')
        # self.alphaIds.add(alphaId)
        # folder = self._resps._lookup(raw, 'url_dossier')
        # if folder != '':
        #     self.folders.add(ResponsablePublic._hatvp_root + folder)

    def _update_mandates(self, raw, document):
        mandateId = self._resps._lookup(raw, 'id_origine')
        mandateType = self._resps._lookup(raw, 'type_mandat')
        mandateTitle = self._resps._lookup(raw, 'qualite')
        departement = self._resps._lookup(raw, 'departement')

        mandate = None
        if mandateTitle in self.mandates:
            mandate = self.mandates[mandateTitle]
            mandate['documents'].append(document)
        else:
            mandate = {'id': mandateId, 'type': mandateType, 'departement': departement, 'title': mandateTitle, 'documents': [document]}
            self.mandates[mandateTitle] = mandate
        document['mandate'] = mandate

        self.mandateTypes.add(mandateType)
        if departement != '':
            self.departements.add(departement)

    def add_document(self, raw):
        mandateId = self._resps._lookup(raw, 'id_origine')
        mandateType = self._resps._lookup(raw, 'type_mandat')
        mandateTitle = self._resps._lookup(raw, 'qualite')
        departement = self._resps._lookup(raw, 'departement')

        type = self._resps._lookup(raw, 'type_document')
        published = self._resps._lookup(raw, 'date_publication')
        name = self._resps._lookup(raw, 'nom_fichier')

        url = None
        if name != '':
            if name == 'dispense':
                state = 'exempted'
            else:
                url = ResponsablePublic._file_address + name
                state = 'found'
        elif published == '':
            state = 'unpublished'
        else:
            state = 'not_found'

        document = {'state': state, 'published': published, 'type': type, 'url': url}
        self.documents.append(document)

        self._update_info(raw)
        self._update_mandates(raw, document)
