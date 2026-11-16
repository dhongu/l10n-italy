## 20.0.1.0.1 (2026-11-16)

**Changed**

- Migration to Odoo 20 (the PostgreSQL codes to retry are defined in the module; `ir.config_parameter`
  `get_int` / `set_int`); `consultant_sheet` manifest key aligned with 19.0.

## 19.0.1.0.1 (2026-11-04)

**Added**

- Italian translation (`i18n/it.po`) of the actions.

## 19.0.1.0.0 (2026-11-04)

**Added**

- Italian localities with postal code (CAP) and province, from GeoNames.
- City and province filled in from the CAP on Italian addresses; action and scheduled
  action to link the existing contacts.
- Consultant sheet (readme/FISA_CONSULTANT.md) and screenshots, in Romanian and English.
