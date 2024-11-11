# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
import json


class MaterialMaterial(http.Controller):
    @http.route('/get/material', type='http', auth='public', methods=['GET'], csrf=False)
    def get_material(self, **kw):
        try:
            if all(key in kw for key in ['materialCode', 'materialType']):
                material_ids = request.env['material.material'].sudo().search([('material_code', '=', kw['materialCode']), ('material_type', 'ilike', kw['materialType'])])
            elif 'materialCode' in kw:
                material_ids = request.env['material.material'].sudo().search([('material_code', '=', kw['materialCode'])])
            elif 'materialType' in kw:
                material_ids = request.env['material.material'].sudo().search([('material_type', 'ilike', kw['materialType'])])
            else:
                material_ids = request.env['material.material'].sudo().search([])

            data_received = []
            if material_ids:
                statusCode = "200"
                message = "OK"
                for material in material_ids:
                    data_received.append({
                        "materialCode": material.material_code,
                        "materialName": material.material_name,
                        "materialType": dict(material._fields['material_type'].selection).get(material.material_type),
                        "materialBuyPrice": material.material_buy_price,
                        "supplierName": material.supplier_id.name,
                    })
            else:
                statusCode = "404"
                message = "No Data!"

            if data_received:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                    "data_received": data_received
                }
            else:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                }
            return json.dumps(response)
        except:
            return "<h3>Something went wrong!</h3>"

    @http.route('/post/material', type='http', auth='public', methods=['POST'], csrf=False)
    def post_material(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            data_received = False
            if 'materialCode' not in data:
                statusCode = "400"
                message = "materialCode must be Filled!"
            else:
                material_id = request.env['material.material'].sudo().search([('material_code', '=', data['materialCode'])])
                if material_id:
                    if 'materialType' in data:
                        if data['materialType'].lower() not in ["fabric", "jeans", "cotton"]:
                            statusCode = "404"
                            message = "materialType not Found!"
                            response = {
                                "statusCode": statusCode,
                                "message": message,
                            }
                            return json.dumps(response)

                    supplierName = False
                    if 'supplierName' in data:
                        partner_id = request.env['res.partner'].sudo().search([('name', 'ilike', data['supplierName'])])
                        if partner_id:
                            material_id.supplier_id = partner_id.id
                            supplierName = partner_id.name
                        else:
                            statusCode = "404"
                            message = "supplierName not Found!"
                            response = {
                                "statusCode": statusCode,
                                "message": message,
                            }
                            return json.dumps(response)

                    material_id.write({
                        'material_name': data['materialName'] if 'materialName' in data else material_id.material_name,
                        'material_type': data['materialType'].lower() if 'materialType' in data else material_id.material_type,
                        'material_buy_price': data['materialBuyPrice'] if 'materialBuyPrice' in data else material_id.material_buy_price
                    })

                    statusCode = "200"
                    message = "OK"
                    data_received = {
                        "materialCode": material_id.material_code,
                        "materialName": material_id.material_name,
                        "materialType": material_id.material_type,
                        "materialBuyPrice": material_id.material_buy_price,
                        "supplierName": supplierName if supplierName else material_id.supplier_id.name
                    }
                    material_id.sync_statusCode = statusCode
                    material_id.sync_message = message
                    material_id.sync_date = fields.Datetime.now()
                else:
                    statusCode = "404"
                    message = "materialCode not Found!"
                    data_received = {
                        "materialCode": data['materialCode']
                    }

            if data_received:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                    "data_received": data_received
                }
            else:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                }
            return json.dumps(response)
        except:
            return "<h3>Something went wrong!</h3>"

    @http.route('/delete/material', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, **kw):
        try:
            if 'materialCode' not in kw:
                response = {
                    "statusCode": 400,
                    "message": "materialCode must be Filled!"
                }
                return json.dumps(response)

            material_id = request.env['material.material'].sudo().search([('material_code', '=', kw['materialCode'])])

            if not material_id:
                response = {
                    "statusCode": 404,
                    "message": "Record not Found!",
                }
                return json.dumps(response)

            else:
                material_id.unlink()
                response = {
                    "statusCode": 200,
                    "message": "Record deleted successfully",
                }
                return json.dumps(response)
        except:
            return "<h3>Something went wrong!</h3>"
