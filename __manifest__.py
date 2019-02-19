# -*- coding: utf-8 -*-
{
    'name': "zh_mrp",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ZH",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'mrp',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','sale_mrp'],

    # always loaded
    'data': [
        #'security/zh_mrp_security.xml',
        'wizard/zh_mrp_wizard.xml',
        'views/zh_mrp_production.xml',
        'views/zh_mrp_menu.xml',
        'report/mrp_report_views_main.xml',
        'report/mrp_production_templates.xml',        
    ],
}