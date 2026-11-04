Loads the Italian localities with their postal code (CAP) and province, and fills in the
city and the province of Italian addresses from the CAP.

- Ships the list of Italian localities (comuni and frazioni) with their CAP, linked to the
  provinces already defined in Odoo. The data comes from [GeoNames](https://www.geonames.org)
  (Creative Commons Attribution 4.0).
- Italy is set to *enforce cities*: the city of an Italian address is chosen from the list.
- On the contact form, typing the CAP of an Italian address sets the city and the province.
  A CAP shared by several localities sets only the province; the city name, when it matches
  one of them (without accents and case), picks the locality. A leading zero lost in an
  import is put back ("187" is "00187").
- The action *Italy: set city from ZIP* on contacts links the Italian contacts to the city
  of their CAP and fills in the province.
- At install, the Italian contacts are linked: directly on a small database, by the scheduled
  action *Italy: link contacts to the city of their ZIP* in batches on a large one (it
  deactivates itself when done).
- Every form that runs the postal code rules of the contact (for example the delivery details
  of an AWB) gets the province filled in, so the shipment can be sent to Italy without
  looking up the province by hand.
