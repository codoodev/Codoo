# -*- coding: utf-8 -*-

{
    'name': 'Order Line Note In POS',
    'summary': """Add Note in order line from the pos interface. """,
    'version': '13',
    'description': """The module is used to add note per order line in POS""",
    'author': "Codoo",
    'license': 'LGPL-3',
    'support': 'codoo.dev@gmail.com',
    'live_test_url': 'https://youtu.be/dvzL39MTja8',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_templates.xml',
        'views/pos_order_views.xml',
        'views/pos_config_views.xml',
    ],
    'qweb': [
        'static/src/xml/notes.xml',
            ],
    "images": ['static/description/icon.png'],


}