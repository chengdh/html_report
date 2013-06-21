openerp.html_report = function(instance){
  _.extend(instance.web.ActionManager.prototype,{
    //重写report方法
    ir_actions_report_xml: function(action, options) {
      var self = this;
      instance.web.blockUI();
      return instance.web.pyeval.eval_domains_and_contexts({
        contexts: [action.context],
        domains: []
      }).then(function(res) {
        action = _.clone(action);
        action.context = res.context;
        var c = instance.webclient.crashmanager;

        //获取下载文件的请求
        var ajax_get_file = function(){
          return self.session.get_file({
            url: '/web/report',
            data: {action: JSON.stringify(action)},
            complete: instance.web.unblockUI,
            success: function(){
              if (!self.dialog) {
                options.on_close();
              }
              self.dialog_stop();
            },
            error: function () {
              c.rpc_error.apply(c, arguments);
            }
          })
        };

        var ajax_get_report = function(){
          var token = new Date().getTime();
          params = {};
          params['action'] = JSON.stringify(action);
          return self.session.rpc('web/report/html_report',params).pipe(function(data){
            var print_doc = $(data.result);
            print_doc.jqprint();

          }).fail(function(data){
            c.rpc_error.apply(c, arguments);
          }).then(function(){
            instance.web.unblockUI();
          });
        };
        if(action.report_type == 'html' || action.report_type == 'html2html' || action.report_type == 'mako2html')
          return ajax_get_report();
        else
          return ajax_get_file();
      });
    }
  });
};
