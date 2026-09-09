# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

COMANDERA_REPORT_NAME = "pos_label_national_tax_price.comandera_label"
# Must match the label height (o_label_sheet, cut-guide row included) baked
# into report_simple_label_comandera's inline styles in
# product_label_national_tax_price_templates.xml.
LABEL_HEIGHT_MM = 40
PAGE_MARGIN_MM = 4


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        report = self._get_report(report_ref)
        if report.report_name == COMANDERA_REPORT_NAME and data:
            total_labels = sum(data.get("quantity_by_product", {}).values())
            self = self.with_context(pos_label_comandera_count=total_labels)
        return super(IrActionsReport, self)._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)

    def get_paperformat(self):
        count = self.env.context.get("pos_label_comandera_count")
        if count and self.report_name == COMANDERA_REPORT_NAME:
            height = count * LABEL_HEIGHT_MM + 2 * PAGE_MARGIN_MM
            return self.env["report.paperformat"].new({
                "format": "custom",
                "page_width": 72,
                "page_height": height,
                "orientation": "Portrait",
                "margin_top": 0,
                "margin_bottom": 0,
                "margin_left": 0,
                "margin_right": 0,
                "disable_shrinking": True,
                "dpi": 96,
            })
        return super().get_paperformat()
