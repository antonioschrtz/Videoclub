# -*- coding: utf-8 -*-
{
    'name': "Video Club",

    'summary': """
        Short summary of the module's purpose.
    """,

    'description': """
        A simple module to manage a video club.
    """,

    'author': "Antonio",
    'website': "http://www.aserti.es",
    'license': 'LGPL-3',

    'category': 'Sales',
    'version': '0.1',
    'application': True,

    'depends': ['base'],

    'data': [
        'security/videoclub_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,

    'demo': [
        'demo/demo.xml',
    ],
}
