/* Copyright 2018 Tecnativa - David Vidal
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("siki_pos_lot.pos", function (require) {
    "use strict";
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var core = require('web.core');
    var models = require("point_of_sale.models");
    var Model = require("web.DataModel");
    var session = require("web.session");
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');
    var Backbone = window.Backbone;
    var _t = core._t;

    var exports = {};




var PosModelSuper = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
 
            load_server_data: function(){
            var self = this;
            var loaded = PosModelSuper.load_server_data.call(this);

            var set_prod_vals = function(vals) {
                _.each(vals, function(v){
                    _.extend(self.db.get_product_by_id(v.id), v);
                });
            };

            var prod_model = _.find(this.models, function(model){
                return model.model === 'product.product';
            });
             if (prod_model) {
                prod_model.fields.push('tracking');
                //var context_super = prod_model.context;
                //var loaded_super = prod_model.loaded;
                //prod_model.loaded = function(that, products){
                    //loaded_super(that, products);
                    //set_prod_vals(products);
               // };
                return loaded;
            }

     
        },
    

     

    });



var _super_order = models.Order.prototype;
 models.Order = models.Order.extend({
  display_lot_popup: function() {
        var order_line = this.get_selected_orderline();
        if (order_line){
            var pack_lot_lines =  order_line.compute_lot_lines();
            this.pos.gui.show_popup('packlotline', {
                'title': _t('Lot/Serial Number(s) Required'),
                'pack_lot_lines': pack_lot_lines,
                'order_line': order_line,
                'order': this,
            });
        }
    },

    //add_product: function(product, options){


   // var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
   // _super_order.add_product.apply(this,arguments);
    //if(line.has_product_lot){
           // this.display_lot_popup();
       // }

 //},

});



   var _super_orderline = models.Orderline.prototype;
   models.Orderline = models.Orderline.extend({

      initialize: function(attr,options){
        _super_orderline.initialize.call(this,attr,options);
        this.set_product_lot(this.product);
         
    },

     init_from_JSON: function(json) {
         _super_orderline.init_from_JSON.apply(this,arguments);
         this.set_product_lot(this.product);
         var pack_lot_lines = json.pack_lot_ids;
        for (var i = 0; i < pack_lot_lines.length; i++) {
            var packlotline = pack_lot_lines[i][2];
            var pack_lot_line = new exports.Packlotline({}, {'json': _.extend(packlotline, {'order_line':this})});
            this.pack_lot_lines.add(pack_lot_line);
        }
    },

        export_as_JSON: function() {
        var pack_lot_ids = [];
        if (this.has_product_lot){
            this.pack_lot_lines.each(_.bind( function(item) {
                return pack_lot_ids.push([0, 0, item.export_as_JSON()]);
            }, this));
        }
        return {
            qty: this.get_quantity(),
            price_unit: this.get_unit_price(),
            discount: this.get_discount(),
            product_id: this.get_product().id,
            tax_ids: [[6, false, _.map(this.get_applicable_taxes(), function(tax){ return tax.id; })]],
            id: this.id,
            pack_lot_ids: pack_lot_ids
        };
    },

     set_product_lot: function(product){
        this.has_product_lot = product.tracking !== 'none';
        this.pack_lot_lines  = this.has_product_lot && new PacklotlineCollection(null, {'order_line': this});
    },



     get_required_number_of_lots: function(){
        var lots_required = 1;

        if (this.product.tracking == 'serial') {
            lots_required = this.quantity;
        }

        return lots_required;
    },

    compute_lot_lines: function(){
        var pack_lot_lines = this.pack_lot_lines;
        var lines = pack_lot_lines.length;
        var lots_required = this.get_required_number_of_lots();

        if(lots_required > lines){
            for(var i=0; i<lots_required - lines; i++){
                pack_lot_lines.add(new exports.Packlotline({}, {'order_line': this}));
            }
        }
        if(lots_required < lines){
            var to_remove = lines - lots_required;
            var lot_lines = pack_lot_lines.sortBy('lot_name').slice(0, to_remove);
            pack_lot_lines.remove(lot_lines);
        }
        return this.pack_lot_lines;
    },

    has_valid_product_lot: function(){
        if(!this.has_product_lot){
            return true;
        }
        var valid_product_lot = this.pack_lot_lines.get_valid_lots();
        return this.get_required_number_of_lots() === valid_product_lot.length;
    },


});


exports.Packlotline = Backbone.Model.extend({
    defaults: {
        lot_name: null
    },
    initialize: function(attributes, options){
        this.order_line = options.order_line;
        if (options.json) {
            this.init_from_JSON(options.json);
            return;
        }
    },

    init_from_JSON: function(json) {
        this.order_line = json.order_line;
        this.set_lot_name(json.lot_name);
    },

    set_lot_name: function(name){
        this.set({lot_name : _.str.trim(name) || null});
    },

    get_lot_name: function(){
        return this.get('lot_name');
    },

    export_as_JSON: function(){
        return {
            lot_name: this.get_lot_name(),
        };
    },

    add: function(){
        var order_line = this.order_line,
            index = this.collection.indexOf(this);
        var new_lot_model = new exports.Packlotline({}, {'order_line': this.order_line});
        this.collection.add(new_lot_model, {at: index + 1});
        return new_lot_model;
    },

    remove: function(){
        this.collection.remove(this);
    }
});

var PacklotlineCollection = Backbone.Collection.extend({
    model: exports.Packlotline,
    initialize: function(models, options) {
        this.order_line = options.order_line;
    },

    get_empty_model: function(){
        return this.findWhere({'lot_name': null});
    },

    remove_empty_model: function(){
        this.remove(this.where({'lot_name': null}));
    },

    get_valid_lots: function(){
        return this.filter(function(model){
            return model.get('lot_name');
        });
    },

     set_quantity_by_lot: function() {
  if (this.order_line.product.tracking == 'serial') {
            var valid_lots_quantity = this.get_valid_lots().length;
            if (this.order_line.quantity < 0){
                valid_lots_quantity = -valid_lots_quantity;
            }
            this.order_line.set_quantity(valid_lots_quantity);
        }
    }
});


});
