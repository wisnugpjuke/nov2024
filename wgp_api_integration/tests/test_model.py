from odoo.tests.common import TransactionCase


class TestMyCustomModel(TransactionCase):
    def setUp(self):
        super(TestMyCustomModel, self).setUp()

        # success
        self.example1 = self.env['material.material'].create({
            'material_code': 'mtr2',
            'material_name': 'Material 2',
            'material_type': 'cotton',
            'material_buy_price': 1000,
            'supplier_id': 14,
        })

        # failed, cause of material_buy_price < 100
        self.example2 = self.env['material.material'].create({
            'material_code': 'mtr2',
            'material_name': 'Material 2',
            'material_type': 'cotton',
            'material_buy_price': 80,
            'supplier_id': 14,
        })

        # failed, cause of material_code already exist
        self.example3 = self.example1.copy()


    def test_create1(self):
        result = self.example1
        self.assertEqual(result, 'Example 1')

    def test_create2(self):
        result = self.example2
        self.assertEqual(result, 'Example 2')

    def test_create3(self):
        result = self.example3
        self.assertEqual(result, 'Example 3')
