from odoo import api, fields, models, _
from logging import getLogger
_logger = getLogger(__name__)

class Product(models.Model):
    _inherit = ["product.template"]
    product_test = fields.Many2one(comodel_name='qc.test', string='Test', tracking=True)
    test_question = fields.One2many(related='product_test.test_lines')
    
    
class Question(models.Model):
    _inherit = ["qc.test.question"]
    valor_nominal = fields.Float(string='Valor Nominal', tracking=True)
    cota_min = fields.Float(string='Cota Mínima', tracking=True)
    cota_max = fields.Float(string='Cota Máxima', tracking=True)
    min_value = fields.Float(string="Min", digits="Quality Control", compute="_compute_test", store=True)    
    max_value = fields.Float(string="Max", digits="Quality Control", compute="_compute_test", store=True)    

    @api.depends('valor_nominal', 'cota_min', 'cota_max')
    def _compute_test(self):        
        for record in self:
            record.min_value = record.valor_nominal - record.cota_min
            record.max_value = record.valor_nominal + record.cota_max