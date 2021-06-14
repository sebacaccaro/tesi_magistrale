#!/usr/bin/python3

import subprocess, sys

commands = [
    ['pdflatex', 'Metodologia_test' + '.tex'],
    ['bibtex', 'Metodologia_test' + '.aux'],
    ['pdflatex', 'Metodologia_test' + '.tex'],
    ['pdflatex', 'Metodologia_test' + '.tex']
]

for c in commands:
    subprocess.call(c)
