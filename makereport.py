''' ,o888888o.       d888888o.   8 888888888o
 . 8888     `88.   .`8888:' `88. 8 8888    `88.
,8 8888       `8b  8.`8888.   Y8 8 8888     `88
88 8888        `8b `8.`8888.     8 8888     ,88
88 8888         88  `8.`8888.    8 8888.   ,88'
88 8888         88   `8.`8888.   8 888888888P'
88 8888        ,8P    `8.`8888.  8 8888
`8 8888       ,8P 8b   `8.`8888. 8 8888
 ` 8888     ,88'  `8b.  ;8.`8888 8 8888
    `8888888P'     `Y8888P ,88P' 8 8888

8888888b.                                    888
888   Y88b                                   888
888    888                                   888
888   d88P .d88b.  88888b.   .d88b.  888d888 888888
8888888P" d8P  Y8b 888 "88b d88""88b 888P"   888
888 T88b  88888888 888  888 888  888 888     888
888  T88b Y8b.     888 d88P Y88..88P 888     Y88b.
888   T88b "Y8888  88888P"   "Y88P"  888      "Y888
                   888
 .d8888b.          888                                888
d88P  Y88b         888                                888
888    888                                            888
888         .d88b.  88888b.   .d88b.  888d888 8888b.  888888 .d88b.  888d888
888  88888 d8P  Y8b 888 "88b d8P  Y8b 888P"      "88b 888   d88""88b 888P"
888    888 88888888 888  888 88888888 888    .d888888 888   888  888 888
Y88b  d88P Y8b.     888  888 Y8b.     888    888  888 Y88b. Y88..88P 888
 "Y8888P88  "Y8888  888  888  "Y8888  888    "Y888888  "Y888 "Y88P"  888

## AUTHOR AND PROGRAM INFO ####################################################

Author:  Alex Jansons <u5183898@anu.edu.au>
Version: 1.0 (MVP)
Created: 28/07/2014

This is just a simple program to render the mako template,
using: #python makereport.py
then just open report.html.

Please see the report.mako header for more information.

'''

from mako.template import Template

def renderTemplate(file):
    template = Template(filename = file, input_encoding = 'utf-8')
    return template.render()

def gen_report():
    ## TODO: Allow user to specify output file name, add prompt if file already
    ## exists. This would probably be contained in the config file
    f = open('report.html', 'w+')
    template = Template(filename = 'report.mako')
    ## Convert the rendered report from a bytes object to a string, so we can
    ## write it to the file.
    output = str(template.render())
    f.write(output)
    f.close()


if __name__ == '__main__':
    gen_report();

    