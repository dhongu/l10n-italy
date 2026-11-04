# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
#
# Capturi de ecran pentru fișa consultant (readme/FISA_CONSULTANT.md, în RO, în
# static/description/) și pentru readme/USAGE.md (în EN, în static/description/en/).
#
# Localitățile sunt cele reale din data/res.city.csv (GeoNames); partenerii sunt de exemplu.
# Codul poștal se tastează în browser, ca operatorul.
#
# Rulare — RESTRÂNSĂ LA CLASĂ, altfel se rescriu capturile tuturor modulelor cu test de fișe:
#   ./odoo/odoo-bin -c odoo.conf -d <db> -i l10n_it_zip,deltatech_doc_screenshots \
#       --test-tags=/l10n_it_zip:TestItZipScreenshots --stop-after-init
import unittest

from odoo.tests import tagged

try:
    from odoo.addons.deltatech_doc_screenshots.tests.screenshot_case import ScreenshotCase
except ImportError:
    try:
        from odoo.addons.l10n_ro_doc_screenshots.tests.screenshot_case import ScreenshotCase
    except ImportError:
        ScreenshotCase = None


def wait(ms):
    return f"await new Promise((resolve) => setTimeout(resolve, {ms}));"


# caută în lista de localități după CAP (39100: Bolzano, Bozen și frazioni)
SEARCH_CAP = (
    """
async () => {
    const input = document.querySelector(".o_searchview_input");
    input.focus();
    input.value = "39100";
    input.dispatchEvent(new Event("input", { bubbles: true }));
    """
    + wait(800)
    + """
    input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
    """
    + wait(2000)
    + """
}
"""
)


def type_zip(zip_code, open_city=False):
    """Tastează CAP-ul în adresa partenerului; opțional îl caută apoi în lista de localități."""
    script = """
async () => {
    const style = document.createElement("style");
    style.textContent = ".o_form_view [data-fise-badge] { left: -30px !important; }";
    document.head.appendChild(style);
    const input = document.querySelector("div[name='zip'] input");
    input.focus();
    input.value = "ZIP_CODE";
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
    input.blur();
    """ + wait(2000)
    if open_city:
        script += (
            """
    const city = document.querySelector("div[name='city_id'] input");
    city.focus();
    city.value = "ZIP_CODE";
    city.dispatchEvent(new Event("input", { bubbles: true }));
    for (let i = 0; i < 50 && !document.querySelector(".o-autocomplete--dropdown-item"); i++) {
        """
            + wait(200)
            + """
    }
    """
        )
    return (script + "\n}\n").replace("ZIP_CODE", zip_code)


# selectează contactele italiene din listă și deschide meniul Acțiuni
OPEN_ACTIONS = (
    """
async () => {
    document.querySelector("thead .o_list_record_selector input").click();
    """
    + wait(800)
    + """
    document.querySelector(".o_cp_action_menus button").click();
    """
    + wait(1000)
    + """
}
"""
)

ADDRESS = ["div[name='zip']", "div[name='city_id']", "div[name='state_id']"]


@tagged("-at_install", "post_install", "fise_screenshots")
class TestItZipScreenshots(ScreenshotCase or object):
    screenshots_module = "l10n_it_zip"

    @classmethod
    def setUpClass(cls):
        if ScreenshotCase is None:
            raise unittest.SkipTest("deltatech_doc_screenshots indisponibil")
        super().setUpClass()
        cls.prepare_ro_company(name="RO Company")
        env = cls.env
        italy = env.ref("base.it")
        Partner = env["res.partner"]
        cls.partner_milano = Partner.create(
            {"name": "Esempio Milano SRL", "is_company": True, "country_id": italy.id, "street": "Via Dante 7"}
        )
        cls.partner_bolzano = Partner.create(
            {"name": "Esempio Bolzano SRL", "is_company": True, "country_id": italy.id, "street": "Via Museo 12"}
        )
        # contacte importate cu orașul scris liber, fără localitate din listă și fără provincie
        cls.imported = Partner.with_context(tracking_disable=True).create(
            [
                {"name": "Cliente Roma", "country_id": italy.id, "city": "Roma", "zip": "187"},
                {"name": "Cliente Firenze", "country_id": italy.id, "city": "Firenze", "zip": "50122"},
                {"name": "Cliente Napoli", "country_id": italy.id, "city": "Napoli", "zip": "80132"},
            ]
        )
        cls.city_action = env.ref("base_address_extended.action_res_city_tree")
        cls.contacts_action = env.ref("contacts.action_contacts")
        cls.menu = env.ref("contacts.menu_contacts")
        env.flush_all()

    def _form_url(self, partner):
        return f"id={partner.id}&model=res.partner&view_type=form&menu_id={self.menu.id}"

    def _shots(self):
        return [
            {
                "url": f"action={self.city_action.id}&view_type=list&menu_id={self.menu.id}",
                "name": "01_lista_localitati_cap.png",
                "wait": ".o_list_view .o_data_row",
                "eval": SEARCH_CAP,
                "eval_wait": 1000,
                "highlight": ".o_searchview",
            },
            {
                "url": self._form_url(self.partner_milano),
                "name": "02_partener_cap_unic.png",
                "wait": ".o_form_view div[name='zip'] input",
                "eval": type_zip("20121"),
                "eval_wait": 1000,
                "highlight": ADDRESS,
                "settle": 1500,
            },
            {
                "url": self._form_url(self.partner_bolzano),
                "name": "03_partener_cap_comun.png",
                "wait": ".o_form_view div[name='zip'] input",
                "eval": type_zip("39100", open_city=True),
                "eval_wait": 1000,
                "highlight": ADDRESS,
                "settle": 1500,
            },
            {
                "url": f"action={self.contacts_action.id}&view_type=list&menu_id={self.menu.id}",
                "name": "04_actiune_contacte_existente.png",
                "wait": ".o_list_view .o_data_row",
                "eval": OPEN_ACTIONS,
                "eval_wait": 1000,
                "settle": 1000,
            },
        ]

    def _shot_after_action(self):
        roma = self.imported.filtered(lambda p: p.name == "Cliente Roma")
        return {
            "url": self._form_url(roma),
            "name": "05_contact_dupa_actiune.png",
            "wait": ".o_form_view div[name='zip'] input",
            "highlight": ADDRESS,
        }

    def _capture(self, lang):
        self.capture_screenshots(self._shots(), lang=lang)
        # rezultatul acțiunii „Italia: completează localitatea din codul poștal”
        self.imported.l10n_it_fix_city_from_zip()
        self.env.flush_all()
        self.capture_screenshots([self._shot_after_action()], lang=lang)

    def test_capture_fise(self):
        self._capture("ro_RO")

    def test_capture_usage(self):
        self._capture("en_US")
