#!/usr/bin/env python3

import markdown
import unicodedata

class Report:
    def __init__(self, handle, format):
        self._handle = handle
        self._format = format
        if self._format == 'html':
            self._content = []

    def _print(self, content):
        if self._format == 'html':
            self._content.append(content)
        else:
            self._actual_print(content)

    def _actual_print(self, content):
        print(content, file=self._handle)

    def _newline(self):
        self._print('')

    def generate(self, resps):
        self._print("# Rapport sur les déclarations de responsables publics")
        self._newline()
        self._print("Ordonnés par ordre alphabétique")
        self._newline()

        for resp in resps:
            self._print_responsable(resp)

        if self._format == 'html':
            self._actual_print(markdown.markdown('\n'.join(self._content)))

    def _print_responsable(self, resp):
        fullName = '{} {} {}'.format(resp.style, resp.firstName, resp.lastName)
        self._print('## {}'.format(fullName))
        self._newline()
        for photo in resp.photos:
            self._print('![Photo de {}]({})'.format(fullName, photo))

        self._print('### Informations')
        mandateTypes = [self._generate_mandate(mandate) for mandate in resp.mandateTypes]
        self._print(' - **Mandats**: {}'.format(', '.join(mandateTypes)))
        departements = [self._generate_departement(dept) for dept in resp.departements]
        if len(departements) > 0:
            self._print(' - **Departements**: {}'.format(', '.join(departements)))
        if resp.folder != None:
            self._print(' - **HATVP**: [Dossier]({})'.format(resp.folder))
        self._newline()

        self._print('### Mandats')
        self._newline()
        for mandateTitle, mandate in resp.mandates.items():
            self._print('#### {}'.format(mandate['title']))
            self._newline()

            if mandate['type'] == 'senateur':
                self._print('_Sénat_:')
                self._newline()
                if mandate['id'] != '':
                    url_name = self._replace_accents('{}_{}{}'.format(resp.lastName, resp.firstName, mandate['id']).lower())
                    self._print(' - [Profil](http://www.senat.fr/senateur/{}.html)'.format(url_name))
                    self._print(' - [Calendrier d\'activité](https://www.senat.fr/calendrier_activite/?matricule={})'.format(mandate['id']))
                    self._print(' - [Vidéos](http://videos.senat.fr/intervenant.{})'.format(mandate['id']))
                else:
                    self._print(' - Aucune information')
            elif mandate['type'] == 'depute':
                self._print('_Assemblée nationale_:')
                self._newline()
                if mandate['id'] != '':
                    url_name = self._replace_accents('{}-{}'.format(resp.firstName, resp.lastName).lower())
                    self._print(' - [Profil](http://www2.assemblee-nationale.fr/deputes/fiche/OMC_PA{})'.format(mandate['id']))
                    # self._print(' - [Nomination](http://www.assemblee-nationale.fr/14/tribun/tnom/fnap/{})'.format(mandate['id']))
                self._print(' - [NosDeputes.fr](https://www.nosdeputes.fr/{})'.format(url_name))
            elif mandate['type'] == 'europe':
                self._print('_Parlement européen_:')
                self._newline()
                url_name = self._replace_accents('{}-{}'.format(resp.firstName, resp.lastName).lower())
                self._print(' - [VoteWatch](http://www.votewatch.eu/en/term8-{}.html)'.format(url_name))
            else:
                self._print('__Pas d\'informations complémentaires sur ce mandat__')
            self._newline()

            self._print('_Déclarations_:')
            self._newline()
            for document in mandate['documents']:
                documentType = self._generate_documentType(document['type'])
                if document['state'] == 'found':
                    documentDesc = '[{} publiée le {}]({})'.format(documentType, document['published'], document['url'])
                elif document['state'] == 'exempted':
                    documentDesc = 'Exempté' if resp.mascPronoun else 'Exemptée'
                elif document['state'] == 'unpublished':
                    documentDesc = 'Document indisponible pour le moment'
                else:
                    documentDesc = 'Document untrouvable'
                self._print(' - {}'.format(documentDesc))
        self._newline()

    def _generate_documentType(self, type):
        if type == 'dia':
            return 'Déclaration d’intérêts et d’activités'
        elif type == 'diam':
            return 'Déclaration de modification substantielle des intérêts et des activités'
        elif type == 'di':
            return 'Déclaration d’intérêts'
        elif type == 'dim':
            return 'Déclaration de modification substantielle des intérêts'
        elif type == 'dsp':
            return 'Déclaration de situation patrimoniale'
        elif type == 'dspm':
            return 'Déclaration de modification substantielle de situation patrimoniale'
        elif type == 'appreciation':
            return 'Appréciation de la HATVP'
        return 'Déclaration inconnue'

    def _generate_mandate(self, mandate):
        if mandate == 'senateur':
            return 'Sénateur'
        elif mandate == 'depute':
            return 'Député'
        elif mandate == 'gouvernement':
            return 'Membre du gouvernement'
        elif mandate == 'europe':
            return 'Représentant français au Parlement européen'
        elif mandate == 'region':
            return "Membre (dont président) d'un conseil régional"
        elif mandate == 'departement':
            return "Membre (dont président) d'un Conseil général ou équivalent" # / Assemblée et conseil exécutif de Corse / Assemblée de Guyane / Assemblée et conseil exécutif de Martinique / Assemblée territoriale et exécutif d’une collectivité d'outre-mer
        elif mandate == 'commune':
            return "Membre (dont maire) d'un conseil communal"
        elif mandate == 'epci':
            return "Membre (dont président) d'un établissement public de coopération intercommunale" # (dont Conseil de la métropole de Lyon)
        return 'Mandat inconnu'

    def _generate_departement(self, departement):
        name = None
        if departement == '099' or departement == '997' or departement == '998':
            name = 'Français Établis Hors de France'
        else:
            name = DEPARTMENTS[departement]
        return '{} ({})'.format(name, departement)

    def _replace_accents(self, string):
        return ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

DEPARTMENTS = {
    '01': 'Ain',
    '02': 'Aisne',
    '03': 'Allier',
    '04': 'Alpes-de-Haute-Provence',
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes',
    '07': 'Ardèche',
    '08': 'Ardennes',
    '09': 'Ariège',
    '10': 'Aube',
    '11': 'Aude',
    '12': 'Aveyron',
    '13': 'Bouches-du-Rhône',
    '14': 'Calvados',
    '15': 'Cantal',
    '16': 'Charente',
    '17': 'Charente-Maritime',
    '18': 'Cher',
    '19': 'Corrèze',
    '2A': 'Corse-du-Sud',
    '2B': 'Haute-Corse',
    '21': 'Côte-d\'Or',
    '22': 'Côtes-d\'Armor',
    '23': 'Creuse',
    '24': 'Dordogne',
    '25': 'Doubs',
    '26': 'Drôme',
    '27': 'Eure',
    '28': 'Eure-et-Loir',
    '29': 'Finistère',
    '30': 'Gard',
    '31': 'Haute-Garonne',
    '32': 'Gers',
    '33': 'Gironde',
    '34': 'Hérault',
    '35': 'Ille-et-Vilaine',
    '36': 'Indre',
    '37': 'Indre-et-Loire',
    '38': 'Isère',
    '39': 'Jura',
    '40': 'Landes',
    '41': 'Loir-et-Cher',
    '42': 'Loire',
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique',
    '45': 'Loiret',
    '46': 'Lot',
    '47': 'Lot-et-Garonne',
    '48': 'Lozère',
    '49': 'Maine-et-Loire',
    '50': 'Manche',
    '51': 'Marne',
    '52': 'Haute-Marne',
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle',
    '55': 'Meuse',
    '56': 'Morbihan',
    '57': 'Moselle',
    '58': 'Nièvre',
    '59': 'Nord',
    '60': 'Oise',
    '61': 'Orne',
    '62': 'Pas-de-Calais',
    '63': 'Puy-de-Dôme',
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées',
    '66': 'Pyrénées-Orientales',
    '67': 'Bas-Rhin',
    '68': 'Haut-Rhin',
    '69': 'Rhône',
    '70': 'Haute-Saône',
    '71': 'Saône-et-Loire',
    '72': 'Sarthe',
    '73': 'Savoie',
    '74': 'Haute-Savoie',
    '75': 'Paris',
    '76': 'Seine-Maritime',
    '77': 'Seine-et-Marne',
    '78': 'Yvelines',
    '79': 'Deux-Sèvres',
    '80': 'Somme',
    '81': 'Tarn',
    '82': 'Tarn-et-Garonne',
    '83': 'Var',
    '84': 'Vaucluse',
    '85': 'Vendée',
    '86': 'Vienne',
    '87': 'Haute-Vienne',
    '88': 'Vosges',
    '89': 'Yonne',
    '90': 'Territoire de Belfort',
    '91': 'Essonne',
    '92': 'Hauts-de-Seine',
    '93': 'Seine-Saint-Denis',
    '94': 'Val-de-Marne',
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe',
    '972': 'Martinique',
    '973': 'Guyane',
    '974': 'La Réunion',
    '975': 'Saint-Pierre-et-Miquelon',
    '976': 'Mayotte',
    '977': 'Saint-Barthélémy',
    '978': 'Saint-Martin',
    '986': 'Wallis-et-Futuna',
    '987': 'Polynésie française',
    '988': 'Nouvelle-Calédonie',
}
