#!/usr/bin/env python
from os.path import join, dirname

from builtins import print
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


def main(debug=False):

    this_folder = dirname(__file__)

    # Get meta-model from language description
    meta_model = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=debug, skipws=True, ws='\s')

    # Optionally export meta-model to dot
    metamodel_export(meta_model, join(this_folder, 'hl7model.dot'))

    # Instantiate model
    model = meta_model.model_from_file(join(this_folder, 'example.txt'))

    # Optionally export model to dot
    model_export(model, join(this_folder, 'example.dot'))

    print(model.start)

if __name__ == '__main__':
    main()
