import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(240)

    def test_kassa_alussa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edulliset_myynnit_alussa_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaat_myynnit_alussa_oikein(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_kasvattaa_kassan_rahamaaraa_oikein(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi + 240)

    def test_syo_edullisesti_kateisella_laskee_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)

    def test_syo_edullisesti_kateisella_kasvattaa_myyntilukua(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_kateisella_hylkays_ei_muuta_kassan_rahamaaraa(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi)

    def test_syo_edullisesti_kateisella_hylkays_palauttaa_rahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

    def test_syo_edullisesti_kateisella_hylkays_ei_kasvata_myyntilukua(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kateisella_kasvattaa_kassan_rahamaaraa_oikein(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi + 400)

    def test_syo_maukkaasti_kateisella_laskee_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(460), 60)

    def test_syo_maukkaasti_kateisella_kasvattaa_myyntilukua(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kateisella_hylkays_ei_muuta_kassan_rahamaaraa(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi)

    def test_syo_maukkaasti_kateisella_hylkays_palauttaa_rahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)

    def test_syo_maukkaasti_kateisella_hylkays_ei_kasvata_myyntilukua(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kortilla_veloittaa_kortilta_summan(self):
        saldo_aluksi = self.maksukortti.saldo
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, saldo_aluksi - 240)

    def test_syo_edullisesti_kortilla_palauttaa_tosi(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))

    def test_syo_edullisesti_kortilla_kasvattaa_myyntilukua(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_kortilla_hylkays_ei_muuta_kortin_rahamaaraa(self):
        self.maksukortti.saldo = 200
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 200)

    def test_syo_edullisesti_kortilla_hylkays_ei_kasvata_myyntilukua(self):
        self.maksukortti.saldo = 200
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_edullisesti_kortilla_hylkays_palauttaa_epatosi(self):
        self.maksukortti.saldo = 200
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))

    def test_syo_edullisesti_kortilla_ei_muuta_kassan_rahamaaraa(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi)

    def test_syo_maukkaasti_kortilla_veloittaa_kortilta_summan(self):
        self.maksukortti.saldo = 400
        saldo_aluksi = self.maksukortti.saldo
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, saldo_aluksi - 400)

    def test_syo_maukkaasti_kortilla_palauttaa_tosi(self):
        self.maksukortti.saldo = 400
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))

    def test_syo_maukkaasti_kortilla_kasvattaa_myyntilukua(self):
        self.maksukortti.saldo = 400
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kortilla_hylkays_ei_muuta_kortin_rahamaaraa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 240)

    def test_syo_maukkaasti_kortilla_hylkays_ei_kasvata_myyntilukua(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_maukkaasti_kortilla_hylkays_palauttaa_epatosi(self):
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))

    def test_syo_maukkaasti_kortilla_ei_muuta_kassan_rahamaaraa(self):
        self.maksukortti.saldo = 400
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi)

    def test_lataa_rahaa_kortille_kasvattaa_kortin_saldoa_oikein(self):
        saldo_aluksi = self.maksukortti.saldo
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
        self.assertEqual(self.maksukortti.saldo, saldo_aluksi + 1000)

    def test_lataa_rahaa_kortille_kasvattaa_kassan_rahamaaraa_oikein(self):
        rahaa_aluksi = self.kassapaate.kassassa_rahaa
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa_aluksi + 1000)

    def test_lataa_rahaa_kortille_ei_voi_ladata_negatiivista_summaa(self):
        saldo_aluksi = self.maksukortti.saldo
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
        self.assertEqual(self.maksukortti.saldo, saldo_aluksi)
