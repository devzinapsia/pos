# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    # TODO: remove the "test_tiny_label_delete_me" option and its handling
    # below once the SAM4S print diagnostic is done.
    print_format = fields.Selection(
        selection_add=[
            ("national_tax_price", "National tax price (7.2 x 4 cm)"),
            ("test_tiny_label_delete_me", "TEST DELETE ME - Tiny label (6x3 cm)"),
        ],
        ondelete={
            "national_tax_price": "set default",
            "test_tiny_label_delete_me": "set default",
        },
    )

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "national_tax_price":
            xml_id = "pos_label_national_tax_price.report_product_template_label_national_tax_price"
        elif self.print_format == "test_tiny_label_delete_me":
            xml_id = "pos_label_national_tax_price.report_product_template_label_test_tiny_delete_me"
        return xml_id, data
