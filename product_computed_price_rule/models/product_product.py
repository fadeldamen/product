# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
# import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    computed_list_price_rule_id = fields.Many2one(
        'product.computed_list_price.rule',
        string='Sale Price Rule',
        )
    computed_list_price_before = fields.Float(
        string='Sale Price Before',
        compute='_other_computed_rules',
        inverse='_set_prices',
        )
    computed_list_price = fields.Float(
        inverse=False,
        )

    @api.multi
    def _set_prices(self):
        # _logger.info('Set Prices from "computed_list_price"')
        # send coputed list price because it is lost
        for template in self:
            template.set_prices(self.computed_list_price_before)

    @api.multi
    @api.depends(
        'computed_list_price_rule_id.item_ids.sequence',
        'computed_list_price_rule_id.item_ids.percentage_amount',
        'computed_list_price_rule_id.item_ids.fixed_amount',
        )
    def _get_computed_list_price(self):
        """Only to update depends"""
        return super(ProductTemplate, self)._get_computed_list_price()

    @api.multi
    def _other_computed_rules(self, computed_list_price):
        computed_list_price = super(
            ProductTemplate, self)._other_computed_rules(computed_list_price)
        self.computed_list_price_before = computed_list_price
        if self.computed_list_price_rule_id and computed_list_price:
            for line in self.computed_list_price_rule_id.item_ids:
                computed_list_price = computed_list_price * \
                    (1 + line.percentage_amount / 100.0) + line.fixed_amount
        return computed_list_price
