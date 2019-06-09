odoo.define('siki_pos_lot.screens', function (require) {
"use strict";

var screens =  require('point_of_sale.screens');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var core = require('web.core');
var Model = require('web.DataModel');
var utils = require('web.utils');
var formats = require('web.formats');
var QWeb = core.qweb;
var _t = core._t;

screens.OrderWidget.include({
 render_orderline: function(orderline){
        var el_str  = QWeb.render('Orderline',{widget:this, line:orderline}); 
        var el_node = document.createElement('div');
            el_node.innerHTML = _.str.trim(el_str);
            el_node = el_node.childNodes[0];
            el_node.orderline = orderline;
            el_node.addEventListener('click',this.line_click_handler);
            var el_lot_icon = el_node.querySelector('.line-lot-icon');
        if(el_lot_icon){
            el_lot_icon.addEventListener('click', (function() {
                    this.show_product_lot(orderline);
            }.bind(this)));
        }
        

        orderline.node = el_node;
        return el_node;
    },

show_product_lot: function(orderline){
        this.pos.get_order().select_orderline(orderline);
        var order = this.pos.get_order();
        order.display_lot_popup();
    },
});


screens.ActionpadWidget.include({
    
  renderElement: function() {
        var self = this;
        this._super();
        this.$('.pay').click(function(){
               var order = self.pos.get_order();
            var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                return line.has_valid_product_lot();
            });
            if(!has_valid_product_lot){
                self.gui.show_popup('confirm',{
                    'title': _t('Empty Serial/Lot Number'),
                    'body':  _t('One or more product(s) required serial/lot number.'),
                    confirm: function(){
                        self.gui.show_screen('payment');
                    },
                });
            }else{
                self.gui.show_screen('payment');
            }
        });
        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    }
});




});
