This HL7 parser is based on [textX](https://github.com/textX/textX) library.

Grammar is given in `grammar.tx` file.

All HL7 messages should be in folder `sourcefiles`.
Program will automatically try to parse all files with txt extension.

First, program will make meta model of grammar.

![HL7 message diagram](https://raw.githubusercontent.com/NikolaStankovic95/JSDproject/master/images/hl7meta_model.PNG)

After successful matching, you will get .dot file and .pdf file with same name. 