import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_on_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(10)
        self.assertEqual(str(self.maksukortti), "saldo: 0.2")

    def test_rahan_ottaminen_vahentaa_saldoa(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(str(self.maksukortti), "saldo: 0.05")

    def test_otto_ei_voi_ylittaa_saldoa(self):
        self.maksukortti.ota_rahaa(15)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_otto_palauttaa_tosi_rahojen_riitaessa(self):
        self.assertTrue(self.maksukortti.ota_rahaa(5))

    def test_otto_palauttaa_epatosi_kun_rahat_eivat_riita(self):
        self.assertFalse(self.maksukortti.ota_rahaa(15))
