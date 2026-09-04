No configuration is required. The label format is available to every
company as soon as the module is installed.

Automatic cutting
==================

This label is printed the same way the existing Dymo label is: as a PDF sent
to the browser's print dialog. Odoo does not talk to the printer directly
(no IoT Box, no ESC/POS commands), so it cannot issue a "cut" command after
each label.

If the thermal printer has a physical cutter, check whether its own driver
or on-device settings expose an "auto-cut" / "cut after each page" option
and enable it there. This is independent of Odoo and must be configured on
the printer/driver side.
