"""Prove delle regole sulle testimonianze. Si lanciano con:  python -m unittest discover prove"""
import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))
from ts import controlli, dati, selezione  # noqa: E402

CONFIG = json.loads((RADICE / "config.json").read_text(encoding="utf-8"))
OGGI = date(2026, 11, 24)
TESTO = ("Mario Rossi mario.rossi@example.com\nHo iniziato a correre a 52 anni, con dolori al ginocchio dopo ogni uscita. "
         "Pensavo di non essere fatto per correre :muscle: Con il coaching ho cambiato appoggio e cadenza, una settimana alla volta. "
         "Dopo sei mesi ho chiuso la mia prima mezza maratona in 2.05.30 senza fermarmi. Grazie @Luca, chiamami al 333 1234567.")


def riga(**k):
    r = {c: "" for c in dati.COLONNE}
    r.update({"ID": "1700000000", "Data": "2026-10-01", "Allievo": "Mario Rossi", "Stato": "Catalogato", "Testo completo": TESTO,
              "Forza (1-5)": "5", "Consenso": "Da verificare", "Obiezione che smonta": "Ho dolori / mi infortuno, Sono troppo vecchio/a",
              "Sticker / CTA": 'Sondaggio "Anche tu hai dolori quando corri?" + DM DOLORI', "Tipo": "Gara - Mezza",
              "Stagione / aggancio": "Maratone d'autunno (ottobre–dicembre)"})
    r.update(k)
    return dati.da_riga(r)


def contenuto(t, **k):
    c = {"storia": "singola", "ids": [t.id], "modello": "C-virgolette", "argomento": "dolori", "motivo_scelta": "x",
         "struttura": {}, "cta": {"parola": "CORRO", "tipo": "dm", "sticker": ""},
         "caption": "Parte dal problema. Commenta CORRO per il coaching personalizzato.",
         "elementi": [
             {"ruolo": "hook", "titolo": "Corri e ogni volta torna il *dolore*?", "testo": "La storia di Mario."},
             {"ruolo": "problema", "titolo": "Dolori dopo ogni uscita", "citazioni": [{"id": t.id, "testo": "Pensavo di non essere fatto per correre"}]},
             {"ruolo": "difficolta", "titolo": "A 52 anni", "testo": "Ripartire non era scontato."},
             {"ruolo": "soluzione", "titolo": "Una cosa alla volta", "citazioni": [{"id": t.id, "testo": "ho cambiato appoggio e cadenza… una settimana alla volta"}]},
             {"ruolo": "risultato", "citazioni": [{"id": t.id, "testo": "ho chiuso la mia prima mezza maratona in 2.05.30 senza fermarmi"}]},
             {"ruolo": "cta", "titolo": "Ti rivedi?", "testo": "Commenta CORRO e ti scriviamo noi."}]}
    c.update(k)
    return controlli.rifinisci(c)


def errori(t, c, formato="carosello", modelli=("C-virgolette", "C-primadopo")):
    return controlli.controlla(c, formato, {t.id: t}, list(modelli), CONFIG)[0]


class Dati(unittest.TestCase):
    def test_date_due_formati(self):
        self.assertEqual(dati.leggi_data("2026-11-05"), date(2026, 11, 5))
        self.assertEqual(dati.leggi_data("05/11/2026"), date(2026, 11, 5))
        self.assertEqual(dati.leggi_data("", "1700000000"), date(2023, 11, 14))

    def test_valori_multipli(self):
        self.assertEqual(dati.dividi("Post, Ads (ha dato l'ok, non ha social), Storia IG"), ["Post", "Ads (ha dato l'ok, non ha social)", "Storia IG"])

    def test_pulizia_dati_personali(self):
        t = riga()
        for vietato in ("Rossi", "@", "example.com", "333", ":muscle:", "Luca"):
            self.assertNotIn(vietato, t.testo_pulito)
        self.assertEqual(t.firma, "Mario")

    def test_consenso(self):
        self.assertEqual(riga(Consenso="Sì").firma, "Mario Rossi")
        self.assertEqual(riga(Consenso="Da verificare").firma, "Mario")
        self.assertEqual(riga(**{"Da oscurare": "Sì: nomi, cognomi e numeri visibili"}).firma, "")
        self.assertTrue(riga(Consenso="Minorenne – serve ok genitori").minorenne)

    def test_csv_righe_monche(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.csv"
            dati.scrivi_csv([dati.COLONNE, ["1700000001", "01/10/2026", "10:00", "Anna Bianchi"]], p)
            self.assertEqual(dati.carica(p)[0].data, date(2026, 10, 1))


class Selezione(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.reg = selezione.Registro(Path(self.tmp.name) / "registro.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def motivo(self, t):
        return selezione.motivo_esclusione(t, OGGI, self.reg, CONFIG)

    def test_solo_catalogato_e_niente_minorenni(self):
        self.assertIsNone(self.motivo(riga()))
        self.assertIn("Catalogato", self.motivo(riga(Stato="Da catalogare")))
        self.assertEqual(self.motivo(riga(Consenso="Minorenne – serve ok genitori")), "minorenne")
        self.assertEqual(self.motivo(riga(Consenso="No")), "consenso negato")

    def test_novanta_giorni(self):
        t = riga()
        self.reg.registra(OGGI - timedelta(days=89), [t], "stories", "S-tappe", "Fiducia", "singola", "x")
        self.assertIn("90", self.motivo(t))
        self.reg.registra(OGGI - timedelta(days=89), [], "stories", "S-tappe", "Fiducia", "singola", "x")
        self.reg.registra(OGGI - timedelta(days=91), [t], "stories", "S-tappe", "Fiducia", "singola", "x")
        self.assertIsNone(self.motivo(t))
        self.assertIn("90", self.motivo(riga(**{"Ultimo utilizzo": "01/11/2026"})))  # anche la colonna del foglio conta

    def test_rifare_lo_stesso_giorno_non_blocca(self):
        t = riga()
        self.reg.registra(OGGI, [t], "carosello", "C-voci", "Educativo", "singola", "x")
        self.assertIsNone(self.motivo(t))

    def test_rotazione_modelli(self):
        t = riga()
        self.reg.registra(OGGI - timedelta(days=1), [t], "stories", "S-tappe", "Fiducia", "singola", "x")
        self.reg.registra(OGGI - timedelta(days=2), [riga(ID="1700000009")], "carosello", "C-voci", "Pratico", "unita", "x")
        ordine = selezione.ordine_modelli("carosello", OGGI, self.reg)
        self.assertNotIn("C-voci", ordine)      # ultimo carosello uscito
        self.assertNotIn("C-percorso", ordine)  # stessa famiglia grafica di ieri (Tappe)

    def test_stagione(self):
        self.assertEqual(selezione.punti_stagione(riga(), OGGI, CONFIG), 3)
        self.assertEqual(selezione.punti_stagione(riga(), date(2026, 9, 10), CONFIG), 2)
        self.assertEqual(selezione.punti_stagione(riga(), date(2026, 6, 1), CONFIG), 0)


class Controlli(unittest.TestCase):
    def test_contenuto_valido(self):
        t = riga()
        self.assertEqual(errori(t, contenuto(t)), [])

    def test_citazione_riscritta(self):
        t = riga()
        c = contenuto(t)
        c["elementi"][1]["citazioni"][0]["testo"] = "Credevo di non essere portato per la corsa"
        self.assertTrue(any("non è fedele" in e for e in errori(t, c)))
        self.assertTrue(controlli.citazione_fedele("Pensavo di non essere fatto… ho cambiato appoggio", t.testo_pulito))
        self.assertFalse(controlli.citazione_fedele("ho cambiato appoggio… Pensavo di non essere fatto", t.testo_pulito))  # ordine invertito

    def test_cognome_e_contatti(self):
        t = riga()
        c = contenuto(t)
        c["elementi"][2]["testo"] = "Mario Rossi non mollava."
        self.assertTrue(any("Rossi" in e for e in errori(t, c)))
        c = contenuto(t)
        c["caption"] += " Scrivi a info@example.com CORRO"
        self.assertTrue(any("email" in e for e in errori(t, c)))

    def test_da_oscurare_niente_nome(self):
        t = riga(**{"Da oscurare": "Sì: nomi, cognomi e numeri visibili"})
        c = contenuto(t)
        self.assertTrue(any("Mario" in e for e in errori(t, c)))

    def test_parole_salute(self):
        t = riga()
        for frase in ("Il metodo guarisce il ginocchio.", "Una cura per i dolori.", "Così si risolve il problema."):
            c = contenuto(t)
            c["elementi"][2]["testo"] = frase
            self.assertTrue(any("guarisce/cura/risolve" in e for e in errori(t, c)), frase)

    def test_storytelling_e_cta(self):
        t = riga()
        c = contenuto(t)
        c["elementi"][0]["testo"] = "Commenta CORRO subito."
        self.assertTrue(any("primo elemento" in e.lower() for e in errori(t, c)))
        c = contenuto(t)
        c["cta"]["parola"] = "VINCI"
        self.assertTrue(any("cta.parola" in e for e in errori(t, c)))
        c = contenuto(t)
        del c["elementi"][3]
        self.assertTrue(any("soluzione" in e for e in errori(t, c)))
        c = contenuto(t)
        c["elementi"] = c["elementi"][:1] + c["elementi"][1:5] * 3 + c["elementi"][5:]
        self.assertTrue(any("da 6 a 9" in e for e in errori(t, c)))

    def test_stories_massimo_sei(self):
        t = riga()
        c = contenuto(t, modello="S-tappe")
        c["elementi"][0]["ruolo"] = "identificazione"
        c["elementi"][1]["ruolo"] = "difficolta"
        c["elementi"] = c["elementi"][:5] + [dict(c["elementi"][4]), dict(c["elementi"][4])] + c["elementi"][5:]
        self.assertTrue(any("da 4 a 6" in e for e in errori(t, c, "stories", ["S-tappe"])))


if __name__ == "__main__":
    unittest.main()
