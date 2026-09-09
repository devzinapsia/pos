=============================
POS Label National Tax Price
=============================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

This module adds a new product label format, **Etiqueta para comandera con
precio**, to the standard "Print Labels" wizard (Products > select
products > Print Labels).

It is intended for 80mm-wide thermal ticket printers ("comandera"). Rather
than one small PDF page per label (how the standard Dymo label works),
which some thermal printer drivers mishandle when several are printed in
one job, this format prints every requested label stacked on a single
continuous page, 7.2cm wide and as tall as needed for however many labels
are being printed.

The label prints:

* The product name, at a larger size than the Dymo label since there's no
  barcode to make room for.
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
   dialog — it does not go through an IoT Box or send ESC/POS commands.
   Because of that, **Odoo has no way to trigger an automatic cut after
   each label**: whether the printer cuts at all depends entirely on the
   thermal printer's own driver or on-device configuration. See the
   Configuration section below.

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

**Table of contents**

.. contents::
   :local:

Configuration
=============

No configuration is required. The label format is available to every
company as soon as the module is installed.

Automatic cutting
------------------

This label is printed as a PDF sent to the browser's print dialog. Odoo
does not talk to the printer directly (no IoT Box, no ESC/POS commands), so
it cannot issue a "cut" command after each label.

If the thermal printer has a physical cutter, check whether its own driver
or on-device settings expose a "cut" option (some receipt-printer Windows
drivers have a "Feed and Cut" settings tab with a cut-every-N-mm or
cut-after-page option) and enable it there. This is independent of Odoo and
must be configured on the printer/driver side.

Usage
=====

From Point of Sale > Products (or Inventory > Products), select one or more
products, open Actions > Print Labels, and choose the **Etiqueta para
comandera con precio** format, then click Print.

The generated PDF is one continuous 7.2cm-wide page holding every
requested label, one after another, and shows, per label:

* Product name (no barcode).
* "Importe sin impuestos nacionales" and the price with national taxes
  (VAT and national indirect taxes) excluded.
* The final price, as resolved by the wizard's pricelist (see the important
  note above about this not being verified as tax-included).

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/devzinapsia/pos/issues>`_.

Credits
=======

Authors
-------

* Zinapsia

Maintainers
-----------

This module is maintained by Zinapsia.
