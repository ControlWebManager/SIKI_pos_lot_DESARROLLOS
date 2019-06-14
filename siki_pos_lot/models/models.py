# -*- coding: utf-8 -*-
#Código modificado controlwebmanger@gmail.com Ing. Henry VIvas

import logging
from openerp.osv import osv
from openerp import models, fields, api

_logger = logging.getLogger(__name__)

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
        picking_info = picking_obj.browse(cr, uid, picking_id, context=context)
        _logger.error('0 picking_info %s', picking_info.name)
        #import pdb; pdb.set_trace()
        _logger.error('1 picking_id %s', picking_id)
        wrong_lots = self.set_pack_operation_lot_HENRY(cr, uid, [picking_id], context=context)
        _logger.error('2 wrong_lots %s', wrong_lots)
        #import pdb; pdb.set_trace()


        if not wrong_lots:
            _logger.error('3 wrong_lots en el If not %s', wrong_lots)
        # Mark pack operations as done
        #pick = picking_obj.browse(cr, uid, picking_id, context=context)
        #for pack in pick.pack_operation_ids.filtered(lambda x: x.product_id.tracking == 'none'):
            #self.pool['stock.pack.operation'].write(cr, uid, [pack.id], {'qty_done': pack.product_qty}, context=context)
        #if not any([(x.product_id.tracking != 'none') for x in pick.pack_operation_ids]):
            picking_obj.action_done(cr, uid, [picking_id], context=context)

    @api.multi
    def set_pack_operation_lot_ALEJANDRO(self, picking=None):
        """Set Serial/Lot number in pack operations to mark the pack operation done."""
        _logger.error('4 set_pack_operation_lot picking %s', picking)
        StockProductionLot = self.env['stock.production.lot']
        PosPackOperationLot = self.env['pos.pack.operation.lot']
        has_wrong_lots = False
        # pic = self.env['stock.picking'].browse(picking)
        # import pdb; pdb.set_trace()
        for order in self:
            for pack_operation in order.picking_id.pack_operation_ids:
                qty = 0
                qty_done = 0
                pack_lots = []
                pos_pack_lots = PosPackOperationLot.search(
                    [('order_id', '=', order.id), ('product_id', '=', pack_operation.product_id.id)])
                pack_lot_names = [pos_pack.lot_name for pos_pack in pos_pack_lots]

                if pack_lot_names:
                    for lot_name in list(set(pack_lot_names)):
                        stock_production_lot = StockProductionLot.search(
                            [('name', '=', lot_name), ('product_id', '=', pack_operation.product_id.id)])
                        if stock_production_lot:
                            if stock_production_lot.product_id.tracking == 'lot':
                                qty = pos_pack_lots.pos_order_line_id.qty
                            else:
                                qty = 1.0
                            qty_done += qty
                            pack_lots.append({'lot_id': stock_production_lot.id, 'qty': qty})
                        else:
                            has_wrong_lots = True
                else:
                    qty_done = pack_operation.product_qty
                pack_operation.write({'pack_lot_ids': map(lambda x: (0, 0, x), pack_lots), 'qty_done': qty_done})

    def set_pack_operation_lot_HENRY(self, cr, uid, picking, context=None):
        """Set Serial/Lot number in pack operations to mark the pack operation done."""
        _logger.error('4 set_pack_operation_lot picking %s', picking)

        #Se debe obtener los modelos con la API old
        StockProductionLot = self.pool.get('stock.production.lot')
        PosPackOperationLot = self.pool.get('pos.pack.operation.lot')
        _logger.error('5 PosPackOperationLot picking %s', PosPackOperationLot)
        PosOrderModel = self.pool.get('pos.order')
        _logger.error('6 pos_order_env picking %s', PosOrderModel)

        #Buscar el id de la Orden generada por el POS de acuerdo al valor picking que llega en la funcion
        search_pos_id = PosOrderModel.search(cr, uid, [('picking_id', '=', picking)], context=context)
        _logger.error('7 search_pos_id picking %s', search_pos_id)

        #Objet de la Orden del POs, similiar al Self que se generaria en la API New
        pos_order = PosOrderModel.browse(cr, uid, search_pos_id, context=context)
        _logger.error('8 pos_order %s -> %s', pos_order, pos_order.name)

        has_wrong_lots = False
        # pic = self.env['stock.picking'].browse(picking)
        # import pdb; pdb.set_trace()
        for order in pos_order:
            for pack_operation in order.picking_id.pack_operation_ids:
                _logger.error('9 pack_operation %s', pack_operation)
                qty = 0
                qty_done = 0
                pack_lots = []
                #Se debe utilizar Api Old para search en pos_pack_lots
                pos_pack_lots_s = PosPackOperationLot.search(cr, uid,
                    [('order_id', '=', order.id), ('product_id', '=', pack_operation.product_id.id)], context=context)
                _logger.error('10 pos_pack_lots_s %s', pos_pack_lots_s)

                #pos_pack_lots de ser un objeto
                pos_pack_lots = PosPackOperationLot.browse(cr, uid, pos_pack_lots_s, context=context)
                _logger.error('11 pos.pack.operation.lot %s', pos_pack_lots)

                pack_lot_names = [pos_pack.lot_name for pos_pack in pos_pack_lots]
                _logger.error('12 pack_lot_names %s', pack_lot_names)

                if pack_lot_names:
                    #variable para recorrer las lineas de orden de lotes de manera individual
                    i = 0
                    for lot_name in list(set(pack_lot_names)):
                        _logger.error('13.1 lot_name %s', lot_name)
                        stock_production_lot_s = StockProductionLot.search(cr, uid,
                            [('name', '=', lot_name), ('product_id', '=', pack_operation.product_id.id)], context=context)
                        _logger.error('13 stock_production_lot_s %s', stock_production_lot_s)

                        # stock_production_lot debe ser un objeto
                        stock_production_lot = StockProductionLot.browse(cr, uid, stock_production_lot_s, context=context)

                        if stock_production_lot:
                            _logger.error('14 stock_production_lot %s', stock_production_lot)

                            _logger.error('15 pos_pack_lots_s %s', pos_pack_lots_s[i])
                            if stock_production_lot.product_id.tracking == 'lot':
                                #accedo a la linea de orde de manera individual para evitar el error de singleton
                                line_select = PosPackOperationLot.browse(cr, uid,[pos_pack_lots_s[i]], context=context)
                                _logger.error('15.1 line_select.pos_order_line_id.qty %s ', line_select.pos_order_line_id.qty)

                                qty = line_select.pos_order_line_id.qty
                            else:
                                qty = 1.0
                            i += 1
                            qty_done += qty
                            pack_lots.append({'lot_id': stock_production_lot.id, 'qty': qty})
                            _logger.error('16 pack_lots %s', pack_lots)

                        else:
                            has_wrong_lots = True

                _logger.error('18 pack_operation %s', pack_operation)

                pack_operation.write({'pack_lot_ids': map(lambda x: (0, 0, x), pack_lots), 'qty_done': qty_done})


class PosOrderLineLot(models.Model):
    _name = "pos.pack.operation.lot"
    _description = "Specify product lot/serial number in pos order line"

    pos_order_line_id = fields.Many2one('pos.order.line')
    order_id = fields.Many2one('pos.order', related="pos_order_line_id.order_id")
    lot_name = fields.Char('Lot Name')
    product_id = fields.Many2one('product.product', related='pos_order_line_id.product_id')
