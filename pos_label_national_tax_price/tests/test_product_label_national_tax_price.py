# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductLabelNationalTaxPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vat_group = cls.env["account.tax.group"].create(
            {
                "name": "VAT 21% (test)",
                "l10n_ar_vat_afip_code": "5",
            }
        )
        cls.vat_tax = cls.env["account.tax"].create(
            {
                "name": "VAT 21% (test)",
                "amount": 21,
                "amount_type": "percent",
                "tax_group_id": cls.vat_group.id,
                "price_include_override": "tax_included",
            }
        )
        cls.iibb_group = cls.env["account.tax.group"].create(
            {
                "name": "IIBB perception (test)",
                "l10n_ar_tribute_afip_code": "07",
            }
        )
        cls.iibb_tax = cls.env["account.tax"].create(
            {
                "name": "IIBB perception 3% (test)",
                "amount": 3,
                "amount_type": "percent",
                "tax_group_id": cls.iibb_group.id,
                "price_include_override": "tax_included",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 121.0,
                "taxes_id": [(6, 0, (cls.vat_tax + cls.iibb_tax).ids)],
            }
        )
        cls.report_model = cls.env["report.pos_label_national_tax_price.comandera_label"]
        cls.report_action = cls.env.ref("pos_label_national_tax_price.report_product_template_label_comandera")

    def test_price_without_national_taxes_excludes_only_national_taxes(self):
        """Only the VAT (a national tax) is excluded; the provincial IIBB
        perception, even though price-included, must remain in the amount.

        Both taxes are price-included with the same sequence, so Odoo's tax
        engine back-solves them jointly: base * (1 + 0.21 + 0.03) = 121, i.e.
        base = 97.5806..., VAT = 20.4919..., IIBB = 2.9274...
        121 - VAT = 100.5081..., which rounds to 100.51.
        """
        price_without_national_taxes = self.report_model._get_price_without_national_taxes(
            self.product, self.product.list_price
        )
        self.assertAlmostEqual(price_without_national_taxes, 100.51, places=2)

    def test_price_without_national_taxes_no_taxes_returns_same_price(self):
        product_no_tax = self.env["product.product"].create(
            {"name": "Test Product No Tax", "list_price": 50.0, "taxes_id": [(5, 0, 0)]}
        )
        price = self.report_model._get_price_without_national_taxes(product_no_tax, product_no_tax.list_price)
        self.assertEqual(price, product_no_tax.list_price)

    def test_wizard_routes_to_comandera_report(self):
        wizard = self.env["product.label.layout"].create(
            {
                "print_format": "comandera_label",
                "product_ids": [(6, 0, self.product.ids)],
                "custom_quantity": 1,
            }
        )
        xml_id, data = wizard._prepare_report_data()
        self.assertEqual(
            xml_id,
            "pos_label_national_tax_price.report_product_template_label_comandera",
        )
        self.assertEqual(data["quantity_by_product"], {self.product.id: 1})

    def test_report_renders_without_error(self):
        wizard = self.env["product.label.layout"].create(
            {
                "print_format": "comandera_label",
                "product_ids": [(6, 0, self.product.ids)],
                "custom_quantity": 1,
            }
        )
        xml_id, data = wizard._prepare_report_data()
        # Mimic the JSON round-trip the report controller normally does on
        # `data` (which turns the int keys built by the wizard into strings)
        # before it reaches the report values method.
        data["quantity_by_product"] = {str(k): v for k, v in data["quantity_by_product"].items()}
        html, _report_type = (
            self.env["ir.actions.report"]
            .with_context(lang="en_US")
            ._render_qweb_html(xml_id, [self.product.id], data=data)
        )
        self.assertIn(b"Amount without national taxes", html)

    def test_paperformat_height_scales_with_label_count(self):
        """The continuous-roll page height must be computed from the actual
        number of labels being printed in that job (each label's own 40mm,
        cut-guide row included, plus a small page margin), not a fixed
        value - regression test for a bug where printing a single label
        used a leftover, much taller page.
        """
        paperformat_one = self.report_action.with_context(pos_label_comandera_count=1).get_paperformat()
        self.assertEqual(paperformat_one.page_width, 72)
        self.assertEqual(paperformat_one.page_height, 48)  # 1*40 + 2*4 margin

        paperformat_three = self.report_action.with_context(pos_label_comandera_count=3).get_paperformat()
        self.assertEqual(paperformat_three.page_height, 128)  # 3*40 + 2*4 margin

    def test_name_font_size_steps_down_for_long_names(self):
        short_name_product = self.env["product.product"].create(
            {"name": "Short Name Product", "list_price": 10.0}
        )
        long_name_product = self.env["product.product"].create(
            {
                "name": "A Very Long Product Name That Will Not Fit In Two Lines At The Normal Size",
                "list_price": 10.0,
            }
        )
        self.assertEqual(self.report_model._get_name_font_size_em(short_name_product), 1.3)
        self.assertEqual(self.report_model._get_name_font_size_em(long_name_product), 1.0)
