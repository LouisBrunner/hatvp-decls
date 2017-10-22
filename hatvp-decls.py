#!/usr/bin/env python3

import sys
import argparse
from lib.CSVReader import CSVReader

def main():
    parser = argparse.ArgumentParser(description='Génère un rapport concernant les déclarations de responsables publics')
    parser.add_argument('-e', '--entree', metavar='fichier', dest='input', help='le fichier CSV de la HATVP pour les déclarations de responsables publics')
    parser.add_argument('-s', '--sortie', metavar='fichier', dest='output', help='le fichier de sortie contenant le rapport')
    parser.add_argument('-f', '--format', metavar='md|html', default='md', dest='format', help='le format du fichier de sortie, Markdown (md) or HTML (html)')
    args = parser.parse_args()

    cr = CSVReader(args)
    return cr.run()

if __name__ == '__main__':
    sys.exit(main())
