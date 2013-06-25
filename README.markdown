# openerp html report 模块,用于将openerp中的报表以html的形式呈现
=========================================================================
## 具备以下功能
1. 支持mako模板
2. 支持rml模版

## 如何使用
- 按照通常做法,安装该module
- 定义report
定义openerp report的方式,参考[openerp report doc](https://doc.openerp.com/6.1/developer/05_reports/)

## 定义导出到excel类型的报表
- 将report.xml中定义的report_name的名字最后加上.xls 就这么简单,可以了 :)
- 例如
`
      <report id="report_purchase_order_excel" model="purchase.order"
        name="purchase.order.new.xls" file="custom_purchase/report/purchase_order.mako"
        usage="default" string="export purchase order to excel" report_type='mako2html' header='0' />
 `

## **注意**
- 如果需要使用mako模版的报表,注意在定义 `report_type`时,需要将其值设为`mako2html`
- 如果需要使用rml模版的报表,注意在定义 `report_type`时,需要将其值设为`html`
- 如果你想把原系统中所有的pdf报表转换为html形式的报表,请执行以下sql：
`UPDATE ir_act_report_xml SET report_type='html' WHERE report_type='pdf'`

## TODOS
- 增加导出到excel功能
- 不同报表的css样式如何处理
