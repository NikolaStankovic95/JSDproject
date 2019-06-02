#!/usr/bin/env python
from os.path import join, dirname

from builtins import print
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


def main(debug=False):

    this_folder = dirname(__file__)

    # Get meta-model from language description
    meta_model = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=debug, skipws=False, ws='\s')

    # Optionally export meta-model to dot
    metamodel_export(meta_model, join(this_folder, 'hl7model.dot'))

    # Instantiate model
    model = meta_model.model_from_file(join(this_folder, 'example.txt'))

    # Optionally export model to dot
    model_export(model, join(this_folder, 'example.dot'))

    print('MSH segment:', end='\n')
    print(model.msh, end=' ')
    for pid in model.msh.fields:
        print(pid.value, end=' ')
        for sub in pid.values:
            print(sub.value.__str__(), end=' ')
    print('\n')

    print('PID segment:', end='\n')
    print(model.pid, end=' ')
    for field in model.pid.fields:
        print(field.__str__(), end=' ')
        for text in field.values:
            print(text.value.__str__(), end=' ')
    print('\n')


if __name__ == '__main__':
    main()

