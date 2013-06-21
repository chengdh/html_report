#coding: utf-8
#修正使用make2html时的错误,
from lxml import etree

from openerp.report.render.makohtml2html.makohtml2html import makohtml2html
def format_body(self, html):
    '''
    重写makohtml2html.py的format_body方法
    不再添加修饰,直接返回html
    '''
    return etree.tostring(html)

makohtml2html.format_body = format_body



