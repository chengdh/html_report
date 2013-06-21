# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'html report',
    'description' : 
    """
    html 报表,特性如下:
    --针对html类型的报表，直接调用浏览器打印
    --支持以下类型的report: html html2html makohtml2html
    """,
    'version': '0.1',
    'depends': ['base','web'],
    'author': 'chengdh',
    'category': 'Reporting', # i.e a technical module, not shown in Application install menu
    'url': '',
    'data': [],
    'js': [
            'static/lib/jquery.jqprint/jquery.jqprint-0.3.js',
            'static/src/js/html_report.js',
            ],
    'css': [
      'static/src/css/print.css',
      ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
