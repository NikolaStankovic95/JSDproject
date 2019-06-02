#!/usr/bin/env python
import os
import jinja2
import pdfkit
import textx
import sys
from os.path import join, dirname

from builtins import print

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


def get_element(segment, field=0, subfield=0):
    return segment.fields[field].values[subfield].value


def get_analysis_list(segment):
    tests = list()
    tests.append(get_element(segment.test1.obr, 3))
    for test in segment.tests:
        tests.append(get_element(test.obr, 3))
    return tests


def get_notes(segment):
    notes = list()
    for note in segment.nteSegments:
        notes.append((get_element(note, 1), get_element(note, 2)))
        return notes


def get_version_explanation(argument):
    message_type = {
        'ORM': 'Novi zahtev'
    }
    return message_type.get(argument, 'Tip poruke nije implementiran ili je pogrešan')


def check_patient_id(segment):
    pid = get_element(segment.test1.orc, 1)
    for test in segment.tests:
        if pid != get_element(test.orc, 1):
            return False
    return True


def print_model(model):
    print('Ustanova: ' + get_element(model.msh, 1) + ', verzija protokola: ' + get_element(model.msh, 9))
    print('Primnjena poruka od sistema: ' + get_element(model.msh))
    print('Tip poruke: ' + get_version_explanation(get_element(model.msh, 6, 0)) + ' : ' + get_element(model.msh, 6, 1))
    print('Prima sistem: ' + get_element(model.msh, 3, 1))
    print('PID pacijenta:' + get_element(model.pid, 1))
    print('Ime i prezime pacijenta: ' + get_element(model.pid, 4) + ' ' + get_element(model.pid, 4, 1))
    print('Pol: ' + get_element(model.pid, 7))
    print('Adresa:' + get_element(model.pid, 10))
    print('LBO:' + get_element(model.pid, 12, 0))
    print('BZK:' + get_element(model.pid, 17, 0))
    print('JMBG:' + get_element(model.pid, 2))
    print('Ime i prezime lekara: ' + get_element(model.pv1, 6, 1) + ' ' + get_element(model.pv1, 6, 2))
    print('Analize:', end='\n')
    for test in get_analysis_list(model):
        print(test, end='\n')
    print('Napomene:', end='\n')
    for note in get_notes(model):
        print(note[0] + ' : ' + note[1], end='\n')


def generate_pdf(model, this_folder, file):
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    template = jinja_env.get_template(join(this_folder, '/templates/result.html'))
    pdf_folder = join(this_folder, 'pdf')
    utils_folder = join(this_folder, 'utils')
    config = pdfkit.configuration(wkhtmltopdf=join(utils_folder, 'wkhtmltopdf.exe'))
    pdfkit.from_string(template.render(model=model), join(pdf_folder, file), configuration=config)


def main(debug=False):

    this_folder = dirname(__file__)

    # Get meta-model from language description
    meta_model = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=debug, skipws=False, ws='\s')

    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(meta_model, join(dot_folder, 'hl7meta_model.dot'))

    source = join(this_folder, 'sourcefiles')

    for file in os.listdir(source):
        if file.endswith(".txt"):
            try:
                model = meta_model.model_from_file(join(source, file))
            except textx.exceptions.TextXSyntaxError as e:
                print('Greška u fajlu:', file, '; opis greške', e.message, end='\n', file=sys.stderr)
                continue

            model_export(model, join(dot_folder, file.replace('.txt', '.dot')))

            if not check_patient_id(model):
                print('PID se ne slaže u svim testovima sa PID-om iz zaglavlja')
                continue
            else:
                print_model(model)
                generate_pdf(model, this_folder, file.replace('.txt', '.pdf'))


if __name__ == '__main__':
    main()




