# -*- coding: utf-8 -*-
{
    'name': "siki_pos_lot",

    'summary': """
        Lotes en pos""",

    'description': """
        Agrega funcionalidad de core 10 punto de venta para lotes     

List of modifications:
----------------------
    * V.-1.0 Se verifica tipo de Funciones que se esta utilizando, Metodos del Core POS Version 11
    * V.-1.1 Se incorporan reglas de acceso para correcta funcionalidad en multiples cajas - Importante: en la asignacion de permiso al grupo, se debe colocar el module al que se hace referencia en nuestro caso point_of_sale
        * Permisos:
            * model_pos_pack_operation_lot
            * model_stock_production_lot
    * V.-2.0 Se corrige error no se asignaba cantidad de producto en la Orden de Entrega Generada en el procesode ventas del POS
    * V.-3.0 Se corrige error productos lotes, al seleccionar este tipo de producto la selección se sumaba en una sola linea de orden, su tratamiento normal es: cada producto lote seleccionado se crea una nueva línea de orden 
    * V.-4.0 Se corrige error en orden de entrega, cuando se selecciona diferentes lotes en POS, la orden de entrega generada no asignaba las cantidades de productos a los lotes correspondiente
    """,

    'author': "SIKI SAS, Developer Alejandro Maitan - Colaborador: Ing Henry Vivas controlwebmanager@gmail.com",
    'website': "www.sikisoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'point of sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','sale_stock', 'barcodes'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
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
