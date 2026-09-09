# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("comandera_label", "Label for comandera with price")],
        ondelete={"comandera_label": "set default"},
    )

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "comandera_label":
            xml_id = "pos_label_national_tax_price.report_product_template_label_comandera"
        return xml_id, data
