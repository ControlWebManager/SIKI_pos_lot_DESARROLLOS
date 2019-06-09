# -*- coding: utf-8 -*-
{
    'name': "siki_pos_lot",

    'summary': """
        Lotes en pos""",

    'description': """
        Agrega funcionalidad de core 10 punto de venta para lotes
    """,

    'author': "SIKI SAS, Developer Alejandro Maitan",
    'website': "www.sikisoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'point of sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
 'qweb': [
        'static/src/xml/pos.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
