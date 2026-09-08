# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.addons.product.report.product_label_report import _prepare_data


class ReportProductLabelNationalTaxPrice(models.AbstractModel):
    _name = "report.pos_label_national_tax_price.national_tax_price_label"
    _description = "Product Label Report - National Tax Price"

    def _get_report_values(self, docids, data):
        # Reuse the same product/quantity/pricelist resolution the core Dymo
        # label report uses, instead of re-implementing it.
        values = _prepare_data(self.env, docids, data)
        values["get_price_without_national_taxes"] = self._get_price_without_national_taxes
        # Built in Python (like account.move does for the RG 5614/2024 tax
        # summary) rather than left as inline QWeb text, so the label
        # actually picks up the report's language translation.
        values["national_tax_price_label"] = _("Amount without national taxes:")
        return values

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


# TEMPORARY diagnostic model, not for production use. Reuses the parent
# class's logic as-is, only under the "_name" that the continuous-roll test
# template (national_tax_price_label_continuous_delete_me) expects. Delete
# once the SAM4S print diagnostic is done.
class ReportProductLabelNationalTaxPriceContinuousDeleteMe(ReportProductLabelNationalTaxPrice):
    _name = "report.pos_label_national_tax_price.continuous_delete_me"
    _description = "TEST DELETE ME - Product Label Report - Continuous Roll"
