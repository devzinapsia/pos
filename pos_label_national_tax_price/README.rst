=============================
POS Label National Tax Price
=============================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

This module adds a new product label format, **National tax price (7.5 x 4
cm)**, to the standard "Print Labels" wizard (Products > select products >
Print Labels).

It is intended for 80mm-wide thermal ticket printers ("comandera"), and is
derived from the standard Odoo *Dymo* label report because that is the only
built-in format that already renders a single label per page instead of a
grid of several labels per sheet, and it already uses the full printable
width of an 80mm roll.

The label prints:

* The product name and barcode, same as the existing Dymo label.
* The final price (tax included), same as the existing Dymo label.
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
   application sending the print job). See the Configuration section below.

**Table of contents**

.. contents::
   :local:

Configuration
=============

No configuration is required. The label format is available to every
company as soon as the module is installed.

Automatic cutting
------------------

This label is printed the same way the existing Dymo label is: as a PDF sent
to the browser's print dialog. Odoo does not talk to the printer directly
(no IoT Box, no ESC/POS commands), so it cannot issue a "cut" command after
each label.

If the thermal printer has a physical cutter, check whether its own driver
or on-device settings expose an "auto-cut" / "cut after each page" option
and enable it there. This is independent of Odoo and must be configured on
the printer/driver side.

Usage
=====

From Point of Sale > Products (or Inventory > Products), select one or more
products, open Actions > Print Labels, and choose the **National tax price
(7.5 x 4 cm)** format, then click Print.

The generated PDF is sized for a 7.5 x 4 cm label on an 80mm-wide thermal
printer, and shows, per label:

* Product name and barcode.
* "Importe sin impuestos nacionales" and the price with national taxes
  (VAT and national indirect taxes) excluded.
* The final price, tax included.

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
