#coding: utf-8
#重写rml2html方法
import logging
from openerp.report.render.rml2pdf import utils
from openerp.report.render.rml2html.rml2html import _flowable as flowable

_logger = logging.getLogger(__name__)

def _tag_ignore(self,node):
  result = ""
  for n in utils._child_get(node, self):
    _logger.debug("tag = %s" % n.tag)
    if n.tag in self._tags:
      result += self._tags[n.tag](n)
    else:
      pass

  return result

flowable._tag_ignore = _tag_ignore

def render(self, node):
  result = self.template.start()
  result += self.template.frame_start()
  for n in utils._child_get(node, self):
    if n.tag in self._tags:
      result += self._tags[n.tag](n)
    else:
      result += self._tag_ignore(n)

  result += self.template.frame_stop()
  result += self.template.end()
  return result.encode('utf-8').replace('"',"\'").replace('°','&deg;')

flowable.render = render
