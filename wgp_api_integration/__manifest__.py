# -*- coding: utf-8 -*-
{
    'name': "WGP - API Integration",

    'summary': """
    Module for Integration
        """,

    'description': """
        
    """,

    'author': "Wisnu Galih Pradita",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/material_material.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "images": ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "sequence": 1
}
