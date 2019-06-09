# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import models, fields, api

class pos_order_line(models.Model):
    _inherit = 'pos.order.line'

    pack_lot_ids = fields.One2many('pos.pack.operation.lot', 'pos_order_line_id', string='Lot/serial Number')


class pos_order(osv.osv):
    _inherit = 'pos.order'

    def _force_picking_done(self, cr, uid, picking_id, context=None):
        context = context or {}
        picking_obj = self.pool.get('stock.picking')
        picking_obj.action_confirm(cr, uid, [picking_id], context=context)
        picking_obj.force_assign(cr, uid, [picking_id], context=context)
        #import pdb; pdb.set_trace()
        wrong_lots = self.set_pack_operation_lot(cr, uid, picking_id, context=context)
        #import pdb; pdb.set_trace()
        if not wrong_lots:
        # Mark pack operations as done
        #pick = picking_obj.browse(cr, uid, picking_id, context=context)
        #for pack in pick.pack_operation_ids.filtered(lambda x: x.product_id.tracking == 'none'):
            #self.pool['stock.pack.operation'].write(cr, uid, [pack.id], {'qty_done': pack.product_qty}, context=context)
        #if not any([(x.product_id.tracking != 'none') for x in pick.pack_operation_ids]):
            picking_obj.action_done(cr, uid, [picking_id], context=context)

    @api.multi
    def set_pack_operation_lot(self, picking=None):
        """Set Serial/Lot number in pack operations to mark the pack operation done."""

        StockProductionLot = self.env['stock.production.lot']
        PosPackOperationLot = self.env['pos.pack.operation.lot']
        has_wrong_lots = False
        #pic = self.env['stock.picking'].browse(picking)
        #import pdb; pdb.set_trace()
        for order in self:
            for pack_operation in order.picking_id.pack_operation_ids:
                qty = 0
                qty_done = 0
                pack_lots = []
                pos_pack_lots = PosPackOperationLot.search([('order_id', '=',  order.id), ('product_id', '=', pack_operation.product_id.id)])
                pack_lot_names = [pos_pack.lot_name for pos_pack in pos_pack_lots]

                if pack_lot_names:
                    for lot_name in list(set(pack_lot_names)):
                        stock_production_lot = StockProductionLot.search([('name', '=', lot_name), ('product_id', '=', pack_operation.product_id.id)])
                        if stock_production_lot:
                            if stock_production_lot.product_id.tracking == 'lot':
                                qty =  pos_pack_lots.pos_order_line_id.qty
                            else:
                                qty = 1.0
                            qty_done += qty
                            pack_lots.append({'lot_id': stock_production_lot.id, 'qty': qty})
                        else:
                            has_wrong_lots = True
                else:
                    qty_done = pack_operation.product_qty
                pack_operation.write({'pack_lot_ids': map(lambda x: (0, 0, x), pack_lots), 'qty_done': qty_done})


class PosOrderLineLot(models.Model):
    _name = "pos.pack.operation.lot"
    _description = "Specify product lot/serial number in pos order line"

    pos_order_line_id = fields.Many2one('pos.order.line')
    order_id = fields.Many2one('pos.order', related="pos_order_line_id.order_id")
    lot_name = fields.Char('Lot Name')
    product_id = fields.Many2one('product.product', related='pos_order_line_id.product_id')
