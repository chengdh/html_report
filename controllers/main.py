#coding: utf-8
#重写web/controller/main
from web.controllers.main import Reports,content_disposition

import simplejson
import time
import logging
import ast
import base64
import csv
import glob
import itertools
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import time
import urllib
import urllib2
import urlparse
import xmlrpclib
import zlib
from lxml import etree
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

from web import http
openerpweb = http
import openerp
import openerp.modules.registry
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

@openerpweb.httprequest
def report_index(self, req, action, token):
  '''
  重写报表的方法
  '''
  action = simplejson.loads(action)

  report_srv = req.session.proxy("report")
  context = dict(req.context)
  context.update(action["context"])

  report_data = {}
  report_ids = context["active_ids"]
  if 'report_type' in action:
      report_data['report_type'] = action['report_type']
  if 'datas' in action:
      if 'ids' in action['datas']:
          report_ids = action['datas'].pop('ids')
      report_data.update(action['datas'])

  report_id = report_srv.report(
      req.session._db, req.session._uid, req.session._password,
      action["report_name"], report_ids,
      report_data, context)

  report_struct = None
  while True:
      report_struct = report_srv.report_get(
          req.session._db, req.session._uid, req.session._password, report_id)
      if report_struct["state"]:
          break

      time.sleep(self.POLLING_DELAY)

  report = base64.b64decode(report_struct['result'])
  if report_struct.get('code') == 'zlib':
      report = zlib.decompress(report)
  report_mimetype = self.TYPES_MAPPING.get(
      report_struct['format'], 'octet-stream')


  file_name = action.get('name', 'report')
  #判断是否是导出到excel
  if file_name.endswith('xls') and action['report_type'] in ['html','mako2html','html2html']:
    file_name = action.get('report_name', 'report')
    _logger.debug("report = %s" % report)
    etree_obj = etree.HTML(report)
    #获取要导出的table
    export_excels = [etree.tostring(t) for t in etree_obj.xpath(u"//table")]
    _logger.debug("export excels = %s" % export_excels)
    report = "".join(export_excels)
  else:
    if 'name' not in action:
      reports = req.session.model('ir.actions.report.xml')
      res_id = reports.search([('report_name', '=', action['report_name']),],
                              0, False, False, context)
      if len(res_id) > 0:
          file_name = reports.read(res_id[0], ['name'], context)['name']
      else:
          file_name = action['report_name']

    file_name = '%s.%s' % (file_name, report_struct['format'])



  return req.make_response(report,
       headers=[
           ('Content-Disposition', content_disposition(file_name, req)),
           ('Content-Type', report_mimetype),
           ('Content-Length', len(report))],
       cookies={'fileToken': int(token)})


@openerpweb.jsonrequest
def html_report(self,req,action,mods = None):
    action = simplejson.loads(action)

    report_srv = req.session.proxy("report")
    context = dict(req.context)
    context.update(action["context"])

    report_data = {}
    report_ids = context["active_ids"]
    if 'report_type' in action:
        report_data['report_type'] = action['report_type']
    if 'datas' in action:
        if 'ids' in action['datas']:
            report_ids = action['datas'].pop('ids')
        report_data.update(action['datas'])

    report_id = report_srv.report(
        req.session._db, req.session._uid, req.session._password,
        action["report_name"], report_ids,
        report_data, context)

    report_struct = None
    while True:
        report_struct = report_srv.report_get(
            req.session._db, req.session._uid, req.session._password, report_id)
        if report_struct["state"]:
            break

        time.sleep(self.POLLING_DELAY)

    report = base64.b64decode(report_struct['result'])
    if report_struct.get('code') == 'zlib':
        report = zlib.decompress(report)

    return {'result' : report}

Reports.html_report = html_report
Reports.index = report_index
