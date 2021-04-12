# -*- coding: utf-8 -*-

{
    'name': "Traccar Integration",

    'summary': """
        Odoo Fleet Tracking Using Traccar""",

    'description': """
        This module is used to Integrate Traccar with odoo through Traccar documentation
    """,

    'author': "Codoo",
    'license': 'LGPL-3',
    # for the full list
    'category': 'Tools',
    'version': '14.0',
    'support': 'codoo.dev@gmail.com',
    'live_test_url': 'https://www.youtube.com/watch?v=J5SXLUUni9o',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/report.xml',
        'views/configurations.xml',
        'data/data.xml',
    ],
    "images": ['static/description/icon.png'],

}
