odoo.define('account_child_parent_COA.account_reports', function (require) {
'use strict';

console.log("00000000000000000000000000000000000000000")
var core = require('web.core');
var Context = require('web.Context');
var AbstractAction = require('web.AbstractAction');
var Dialog = require('web.Dialog');
var datepicker = require('web.datepicker');
var session = require('web.session');
var field_utils = require('web.field_utils');
var RelationalFields = require('web.relational_fields');
var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');
var WarningDialog = require('web.CrashManager').WarningDialog;
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;
var account_report = require('account_reports.account_report');


account_report.include({

    fold: function(line) {
        var self = this;
        var line_id = line.data('id');
        line.find('.fa-caret-down').toggleClass('fa-caret-right fa-caret-down');
        line.toggleClass('folded');
        $(line).parent('tr').removeClass('o_js_account_report_parent_row_unfolded');
        var $lines_to_hide = this.$el.find('tr[data-parent-id="'+line_id+'"]');
        var index = self.report_options.unfolded_lines.indexOf(line_id);
        if (index > -1) {
            self.report_options.unfolded_lines.splice(index, 1);
        }
        if ($lines_to_hide.length > 0) {
            line.data('unfolded', 'False');
            $lines_to_hide.find('.js_account_report_line_footnote').addClass('folded');
            $lines_to_hide.hide();
            _.each($lines_to_hide, function(el){
                var child = $(el).find('[data-parent-id]:first');
                if (child) {
                    self.fold(child);
                }
            })
        }
        return false;
    },
});

});
