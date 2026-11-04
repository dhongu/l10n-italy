# l10n-italy

Localizare Odoo pentru Italia (Terrabit).

## Module

- `l10n_it_zip` — localitățile Italiei (comune și frazioni) cu codul poștal (CAP), legate de
  provinciile din Odoo standard; completează localitatea și provincia din CAP și leagă
  contactele existente de localitatea codului lor poștal: la instalare, direct pe o bază mică
  sau printr-o acțiune programată, pe loturi, pe una mare.

## Date

Lista de localități vine din [GeoNames](https://www.geonames.org) (licență Creative Commons
Attribution 4.0). Pentru reîmprospătare:

```bash
curl -sSfLO https://download.geonames.org/export/zip/IT.zip && unzip IT.zip IT.txt
python3 scripts/generate_city_data.py IT.txt
```
