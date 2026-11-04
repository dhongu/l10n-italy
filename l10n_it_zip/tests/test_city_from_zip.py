# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCityFromZip(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.italy = cls.env.ref("base.it")
        cls.Partner = cls.env["res.partner"]

    def _it_city(self, zip_code, name):
        return self.env["res.city"].search(
            [("country_id", "=", self.italy.id), ("zipcode", "=", zip_code), ("name", "=", name)]
        )

    def test_data_loaded(self):
        self.assertTrue(self.italy.enforce_cities)
        milano = self._it_city("20121", "Milano")
        self.assertEqual(len(milano), 1)
        self.assertEqual(milano.state_id, self.env.ref("base.state_it_mi"))

    def test_unique_zip(self):
        city, state = self.Partner._l10n_it_city_from_zip("20121")
        self.assertEqual(city, self._it_city("20121", "Milano"))
        self.assertEqual(state, self.env.ref("base.state_it_mi"))

    def test_leading_zero_restored(self):
        city, state = self.Partner._l10n_it_city_from_zip("187")
        self.assertEqual(city, self._it_city("00187", "Roma"))
        self.assertEqual(state, self.env.ref("base.state_it_rm"))

    def test_shared_zip_gives_province(self):
        # 39100 is Bolzano, Bozen and their frazioni: only the province is known
        bolzano = self.env.ref("base.state_it_bz")
        city, state = self.Partner._l10n_it_city_from_zip("39100")
        self.assertFalse(city)
        self.assertEqual(state, bolzano)
        # the city name picks the locality, without accents and case
        city, state = self.Partner._l10n_it_city_from_zip("39100", "bozen")
        self.assertEqual(city, self._it_city("39100", "Bozen"))
        city, state = self.Partner._l10n_it_city_from_zip("47121", "FORLI")
        self.assertEqual(city, self._it_city("47121", "Forlì"))

    def test_zip_in_two_provinces(self):
        # 08020 is shared by localities of Nuoro and Sassari: no province is guessed
        city, state = self.Partner._l10n_it_city_from_zip("08020")
        self.assertFalse(city)
        self.assertFalse(state)

    def test_onchange_zip(self):
        # not saved: other modules may make more fields required on the contact form
        partner_form = Form(self.Partner)
        partner_form.name = "Mario Rossi"
        partner_form.country_id = self.italy
        partner_form.zip = "20121"
        self.assertEqual(partner_form.city_id, self._it_city("20121", "Milano"))
        self.assertEqual(partner_form.city, "Milano")
        self.assertEqual(partner_form.state_id, self.env.ref("base.state_it_mi"))

    def test_fix_city_from_zip(self):
        partner = self.Partner.create(
            {"name": "Mario Rossi", "country_id": self.italy.id, "city": "Roma", "zip": "187"}
        )
        partner.l10n_it_fix_city_from_zip()
        self.assertRecordValues(
            partner,
            [
                {
                    "city_id": self._it_city("00187", "Roma").id,
                    "city": "Roma",
                    "zip": "00187",
                    "state_id": self.env.ref("base.state_it_rm").id,
                }
            ],
        )

    def test_other_country_untouched(self):
        partner = self.Partner.create(
            {"name": "Ion Popescu", "country_id": self.env.ref("base.ro").id, "city": "Milano", "zip": "20121"}
        )
        partner.l10n_it_fix_city_from_zip()
        self.assertFalse(partner.city_id)
        self.assertFalse(partner.state_id)

    def test_relink_batch(self):
        partner = self.Partner.create(
            {"name": "Mario Rossi", "country_id": self.italy.id, "city": "Milano", "zip": "20121"}
        )
        last_id, count = self.Partner._l10n_it_relink_batch(partner.id - 1)
        self.assertGreaterEqual(count, 1)
        self.assertEqual(partner.city_id, self._it_city("20121", "Milano"))
