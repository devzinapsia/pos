# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.addons.product.report.product_label_report import _prepare_data

# Empirically, ~38 characters is about the longest product name that still
# wraps into 2 lines at the label's normal 1.3em name font size, within its
# ~68mm printable width - longer names wrap to a cramped 3rd line instead
# (confirmed with real reported names: 44 and 50 characters both needed a
# 3rd line at 1.3em; 34 characters comfortably fit in 2). Stepping the font
# size down for those gives them more room to comfortably wrap into 2 (or
# an uncramped 3) lines, instead of a fixed label height tall enough for
# the rare 3-line case at full size (which would make every other, shorter
# label unnecessarily taller too).
NAME_FONT_SIZE_THRESHOLD_CHARS = 38
NAME_FONT_SIZE_NORMAL_EM = 1.3
NAME_FONT_SIZE_LONG_EM = 1.0


class ReportProductLabelComandera(models.AbstractModel):
    _name = "report.pos_label_national_tax_price.comandera_label"
    _description = "Product Label Report - Comandera"

    def _get_report_values(self, docids, data):
        # Reuse the same product/quantity/pricelist resolution the core Dymo
        # label report uses, instead of re-implementing it.
        values = _prepare_data(self.env, docids, data)
        values["get_price_without_national_taxes"] = self._get_price_without_national_taxes
        values["get_name_font_size_em"] = self._get_name_font_size_em
        # Built in Python (like account.move does for the RG 5614/2024 tax
        # summary) rather than left as inline QWeb text, so the label
        # actually picks up the report's language translation.
        values["national_tax_price_label"] = _("Amount without national taxes:")
        return values

    @staticmethod
    def _get_name_font_size_em(product):
        name = product.display_name if product.is_product_variant else product.name
        if name and len(name) > NAME_FONT_SIZE_THRESHOLD_CHARS:
            return NAME_FONT_SIZE_LONG_EM
        return NAME_FONT_SIZE_NORMAL_EM

    def _get_price_without_national_taxes(self, product, price):
        """Amount left of the tax-included `price` after excluding the taxes
        that the AR localization classifies as national (VAT + national
        indirect taxes), reusing the exact classification account.move
        already applies for the RG 5614/2024 "Fiscal Transparency" summary
        printed on invoices (see account.move._l10n_ar_get_invoice_custom_tax_summary_for_report).
        """
        AccountMove = self.env["account.move"]
        taxes = product.taxes_id.filtered(lambda t: t.company_id == self.env.company)
        if not taxes:
            return price
        currency = self.env.company.currency_id
        computed_taxes = taxes.compute_all(price, currency=currency, product=product)
        national_tax_amount = sum(
            tax_vals["amount"]
            for tax_vals in computed_taxes["taxes"]
            if self._is_national_tax(AccountMove, self.env["account.tax"].browse(tax_vals["id"]).tax_group_id)
        )
        return price - national_tax_amount

    @staticmethod
    def _is_national_tax(AccountMove, tax_group):
        return AccountMove._l10n_ar_is_tax_group_vat(tax_group) or AccountMove._l10n_ar_is_tax_group_other_national_ind_tax(tax_group)
