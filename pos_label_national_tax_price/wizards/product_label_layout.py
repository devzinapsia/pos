# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("national_tax_price", "National tax price (7.5 x 4 cm)")],
        ondelete={"national_tax_price": "set default"},
    )

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "national_tax_price":
            xml_id = "pos_label_national_tax_price.report_product_template_label_national_tax_price"
        return xml_id, data
