# Requerimiento SIKI pos lot

## Descripción: 

Desarrollo de funcionlidad de lotes a partir de la App Point_of_sale version 11 para la version 9

## Nombre de la Aplicacion Final: 

siki_pos_lot


## Lista de Modificaciones

* V.-1.0 Se verifica tipo de Funciones que se esta utilizando, Metodos del Core POS Version 11
    * V.-1.1 Se incorporan reglas de acceso para correcta funcionalidad en multiples cajas - Importante: en la asignacion de permiso al grupo, se debe colocar el module al que se hace referencia en nuestro caso point_of_sale
        * Permisos:
            * model_pos_pack_operation_lot
            * model_stock_production_lot
    * V.-2.0 Se corrige error de asignacion de cantidades de productos en la orden de entrega


### Fase de Prueba : 

#### White Box / Test de Caja Blanca 001 

* V.-2.0 Se corrige error de asignacion de cantidades de productos en la orden de entrega
* Se realizarón diferente pruebas de funcionalidad con diferentes variables, [Ver Pruebas](https://docs.google.com/spreadsheets/d/1fgJCBGUPm9i0FuufIGyPcttwbkDpb9LLXH0xId0Xz2I/edit?usp=sharing)


#### Desarrollo

Metodo involucrados
* _force_picking_done()
* set_pack_operation_lot()
* Ruta: /home/webmaster/odoo9/addons_custom/siki_pos_lot/models/models.py

Se detecta que desde el método _force_picking_done() se llama al método set_pack_operation_lot() con parámetros de la api.old (Api Vieja), y este método esta desarrollado con estructura y parámetros de la Api.New (api nueva), lo que hace incompatible la transferencia de data de entre estos dos métodos

Ej. wrong_lots = self.set_pack_operation_lot(cr, uid, [picking_id], context=context) -> llama al método set_pack_operation_lot, pero el método al ser llamado no recibe de manera correcta los argumentos cr, uid, context, ya que no esta preparado para hacerlo con la APi.Old, si no con la nueva: def set_pack_operation_lot(self, picking=None)

Al verificar la traza de la función, al entrar en el método set_pack_operation_lot, el parámetro picking no tiene ningún valor, el mismo es importante para la correcta continuidad de funciones dentre de este
![](./static/src/img/Selección_743.png)
     
#### Anexo Error que se desea corrergir

![](./static/src/img/Selección_735.png)

##### Corrección de error

Se utiliza funcionalidad de la Api.Old en el método set_pack_operation_lot, lo que hace variar drásticamente la estructura del mismo más no, su funcionalidad para lograr ejecutar todo el código que lo integra

Al verificar nuevamente la traza del código, podemos observar una traza más extensa que recorre todo el método set_pack_operation_lot hasta retornar un resultado satisfactorio para la variable wrond_lots
![](./static/src/img/Selección_740.png)

#### Anexos, Error Corregido

Se asigna de manera automática cantidad de inventario para los productos de tipo almacenable y consumible
![](./static/src/img/Selección_741.png)

Se asigna de manera automática Némero de Serie / Número de Lote y sus respectivas cantidades para los productos que dispone de ratreo
![](./static/src/img/Selección_742.png)

---------------------
---------------------
