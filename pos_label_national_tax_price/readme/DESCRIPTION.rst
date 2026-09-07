This module adds a new product label format, **National tax price (7.2 x 4
cm)**, to the standard "Print Labels" wizard (Products > select products >
Print Labels).

It is intended for 80mm-wide thermal ticket printers ("comandera"), and is
derived from the standard Odoo *Dymo* label report because that is the only
built-in format that already renders a single label per page instead of a
grid of several labels per sheet, and it already uses the full printable
width of an 80mm roll.

The label prints:

* The product name and barcode, same as the existing Dymo label.
* The final price, exactly as resolved by the wizard's pricelist — same
  value, same source, as the existing Dymo label.
* A new legend, "Importe sin impuestos nacionales", with the price with the
  AR *national* taxes (VAT and national indirect/internal taxes) excluded.
  This amount is computed reusing the exact same tax classification the
  Argentinian localization already applies to invoices/tickets for the AFIP
  RG 5614/2024 "Fiscal Transparency" breakdown
  (``account.move._l10n_ar_is_tax_group_vat`` /
  ``_l10n_ar_is_tax_group_other_national_ind_tax``), not a new tax
  computation.

The report format is available to every company in the database (it is not
restricted to a single company).

.. important::
   This label is generated as a PDF and printed through the browser's print
   dialog, exactly like the existing Dymo label — it does not go through an
   IoT Box or send ESC/POS commands. Because of that, **Odoo has no way to
   trigger an automatic cut after each label**: whether the printer cuts
   between labels depends entirely on the thermal printer's own driver or
   on-device configuration (many label printers with a built-in cutter have
   an "auto-cut" or "cut after each page" setting independent of the
   application sending the print job). See ``readme/CONFIGURE.rst``.

.. important::
   **This label does not verify that the price it prints is actually tax
   included.** It prints whatever price the wizard's pricelist resolves for
   the product (``pricelist._get_product_price()``) and treats it as the
   final price, without checking each tax's "Included in Price" setting or
   the company's default (Accounting > Settings > Taxes > "Default Sales
   Tax Included in Price"). This is not a limitation specific to this
   module: none of the core label formats (Dymo, 2x7, 4x7, 4x12) or
   ``product.pricelist`` itself do this check either — they all print/use
   the resolved price as-is.

   In a company where a product's tax is *not* marked as included in the
   price (directly on the tax, or via the company default), the price
   printed on every label format, including this one, will not match the
   tax-included amount the invoicer actually charges — and the "Importe sin
   impuestos nacionales" legend on this label is a breakdown *of that same
   printed price*, so it inherits the same gap. Fixing this would mean
   changing how ``product.pricelist``/the core label reports resolve
   "final price" everywhere, which is out of scope for this module.
