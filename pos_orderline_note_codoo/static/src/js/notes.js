odoo.define('pos_orderline_note_codoo.notes', function (require) {
"use strict";

var models = require('point_of_sale.models');
var core = require('web.core');
var screens = require('point_of_sale.screens');

var _super_orderline = models.Orderline.prototype;
models.load_fields('pos.order.line','order_note');

models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
    _super_orderline.initialize.call(this,attr,options);
    this.order_note = this.order_note || "";
    },

    export_as_JSON: function(){
        var json = _super_orderline.export_as_JSON.call(this);
        json.order_note = this.order_note;
        return json;
    },

});

var OrderlineNoteButton = screens.ActionButtonWidget.extend({
    template: 'OrderlineNoteButton',
    button_click: function(){
        var line = this.pos.get_order().get_selected_orderline();
        line.order_note = line.node.getElementsByTagName('i')[0].innerHTML
    },
});

screens.define_action_button({
    'name': 'orderline_note',
    'widget': OrderlineNoteButton,
    'condition': function(){
        return this.pos.config.iface_orderline_order_notes;
    },
});
return {
    OrderlineNoteButton: OrderlineNoteButton,
}
});
