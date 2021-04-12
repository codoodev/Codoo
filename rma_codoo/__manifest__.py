# -*- coding: utf-8 -*-
{
    'name': "RMA (Return Merchandise Authorization)",

    'summary': """
        Return Merchandise Authorization""",

    'description': """
        Return/Refund Orders in one Step.
    """,

    'author': "Codoo",
    'license' : 'LGPL-3',
    # for the full list
    'category': 'Sales',
    'version': '13.0',
    'support': 'codoo.dev@gmail.com',
    'live_test_url': 'https://www.youtube.com/watch?v=OSebQrQHDrg',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account','stock',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    "images": ['static/description/icon.png','static/images/desc1.png','static/images/desc.png'],
}