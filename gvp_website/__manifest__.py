# -*- coding: utf-8 -*-
{
    'name': "gvp_website",

    'summary': """
        Gujarat vidyapith""",

    'description': """
        Gujarat Vidyapith
    """,

    'author': "GVP",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website','portal','base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/profile_data.xml',
        'views/gvp_menu.xml',
        'views/basic_info.xml',
        'views/university_list.xml',
        'views/course_list.xml',
        'views/work_area_list.xml',
        'views/year_view.xml',
        'views/home_view.xml',
        'views/myprofile_view.xml',
        'views/memories_view.xml',
        'views/event_view.xml',
        'views/allmemories.xml',
        'views/allevents.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
