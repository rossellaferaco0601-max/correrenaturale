"""Contenuti di ESEMPIO per le anteprime dei modelli. Sono testi inventati che servono solo a vedere
l'impaginazione: non sono testimonianze reali e non vanno pubblicati."""

M = {"id": "es1", "firma": "Marta"}
P = {"id": "es2", "firma": "Paolo"}
E = {"id": "es3", "firma": "Elena"}


def _c(chi, testo):
    return dict(chi, testo=testo)


def carosello(unita=False, primadopo=False):
    if unita:
        el = [
            dict(ruolo="hook", titolo="«Ormai è *tardi* per imparare a correre bene.»", testo="Lo pensavano in tre. Poi hanno provato a cambiare una cosa sola."),
            dict(ruolo="problema", titolo="Stesso punto di partenza", testo="Età diverse, storie diverse. Ma la stessa frase in testa: «alla mia età il corpo non cambia più».",
                 citazioni=[_c(M, "Avevo 54 anni e mi sembrava di aver perso il treno"), _c(P, "Correvo da vent'anni sempre allo stesso modo, e sempre con lo stesso dolore")]),
            dict(ruolo="difficolta", titolo="Il momento più difficile", citazioni=[_c(E, "Le prime settimane mi sembrava di tornare indietro: più piano, più corto, più attenzione a ogni passo")],
                 testo="Ricominciare dalla tecnica vuol dire accettare di rallentare, per un po'."),
            dict(ruolo="soluzione", titolo="Cosa è cambiato davvero", testo="Un coach che guarda come corri *tu* e ti dà una cosa alla volta su cui lavorare. Niente tabelle uguali per tutti.",
                 citazioni=[_c(P, "Per la prima volta qualcuno guardava i miei video e mi diceva cosa cambiare")]),
            dict(ruolo="risultato", titolo="Dopo qualche mese", citazioni=[_c(M, "Ho chiuso la mia prima mezza senza fermarmi"), _c(E, "Corro tre volte a settimana e non ho più paura di farmi male")]),
            dict(ruolo="sintesi", titolo="Non era l'età. Era il *metodo*.", testo="Tre persone, tre età, lo stesso punto di svolta: smettere di correre «come viene» e farsi guidare passo dopo passo."),
            dict(ruolo="cta", titolo="Pensi anche tu che sia *tardi*?", testo="Commenta CORRO e ti scrivo io: capiamo insieme da dove puoi partire con il coaching personalizzato."),
        ]
    else:
        el = [
            dict(ruolo="hook", titolo="Correva da anni. E ogni volta tornava il *dolore*.", testo="La storia di Marta, e di cosa ha cambiato dopo l'ennesimo stop."),
            dict(ruolo="problema", titolo="Tre mesi di corsa, due di stop", testo="Marta correva tre volte a settimana. Ogni volta che aumentava i chilometri, il ginocchio la fermava.",
                 citazioni=[_c(M, "Pensavo di non essere fatta per correre")]),
            dict(ruolo="difficolta", titolo="Riposo, ripartenza, di nuovo fermo", testo="Aveva provato a cambiare scarpe, a correre meno, a fermarsi del tutto. Il dolore tornava sempre, e con lui la voglia di mollare."),
            dict(ruolo="soluzione", titolo="Ripartire dal *come*, non dal quanto", testo="Con il suo coach ha lavorato prima sulla tecnica: appoggio, cadenza, postura. Poi, una settimana alla volta, sui chilometri.",
                 citazioni=[_c(M, "Mi ha colpito che nessuno mi chiedesse di correre di più, ma di correre meglio")]),
            dict(ruolo="risultato", citazioni=[_c(M, "Sei mesi dopo ho corso la mia prima mezza maratona. Senza fermarmi e senza dolore.")]),
            dict(ruolo="sintesi", titolo="Non era il ginocchio. Era il *modo* di correre.", testo="Quando cambi il gesto, il corpo smette di difendersi. È un lavoro di pazienza, e si fa meglio con qualcuno che ti guarda."),
            dict(ruolo="cta", titolo="Ti rivedi nella storia di Marta?", testo="Commenta CORRO e ti scrivo io: capiamo insieme da dove partire con il coaching personalizzato."),
        ]
        if primadopo:
            el[4] = dict(ruolo="risultato", prima="Tre mesi di corsa, due di stop. Ogni aumento di chilometri finiva con il ginocchio fermo.",
                         dopo="Prima mezza maratona chiusa senza fermarsi. Tre uscite a settimana, da sei mesi.")
    return dict(elementi=el, cta=dict(parola="CORRO", tipo="dm"))


def stories(unita=False):
    if unita:
        el = [
            dict(ruolo="identificazione", titolo="Pensi che sia *tardi* per iniziare a correre?", testo="Lo pensavano anche loro."),
            dict(ruolo="difficolta", titolo="Da dove partivano", citazioni=[_c(M, "Avevo 54 anni e mi sembrava di aver perso il treno"), _c(P, "Vent'anni di corsa, sempre con lo stesso dolore")]),
            dict(ruolo="soluzione", titolo="Cosa hanno cambiato", testo="Una cosa alla volta, con un coach che guarda come corri tu.",
                 citazioni=[_c(E, "Per la prima volta qualcuno guardava i miei video e mi diceva cosa cambiare")]),
            dict(ruolo="risultato", titolo="E oggi", citazioni=[_c(M, "Ho chiuso la mia prima mezza senza fermarmi"), _c(E, "Corro tre volte a settimana senza paura di farmi male")]),
            dict(ruolo="cta", titolo="Pensi sia tardi per iniziare?", testo="Rispondi al sondaggio, oppure scrivimi in DM:"),
        ]
    else:
        el = [
            dict(ruolo="identificazione", titolo="Corri, ti fermi per il *dolore*, riparti. E poi di nuovo.", testo="Se ti suona familiare, leggi cosa mi ha scritto Marta."),
            dict(ruolo="difficolta", titolo="Tre mesi di corsa, due di stop", citazioni=[_c(M, "Pensavo di non essere fatta per correre")],
                 testo="È la frase che sentiamo più spesso. Quasi mai è vera."),
            dict(ruolo="soluzione", titolo="Ripartire dal *come*", citazioni=[_c(M, "Nessuno mi ha chiesto di correre di più, ma di correre meglio")],
                 testo="Prima la tecnica, poi i chilometri. Una settimana alla volta."),
            dict(ruolo="risultato", titolo="Sei mesi dopo", citazioni=[_c(M, "Ho corso la mia prima mezza maratona. Senza fermarmi e senza dolore.")]),
            dict(ruolo="cta", titolo="Anche tu hai dolori quando corri?", testo="Rispondi al sondaggio, oppure scrivimi in DM:"),
        ]
    return dict(elementi=el, cta=dict(parola="CORRO", tipo="sondaggio", sticker="Sondaggio «Anche tu hai dolori quando corri?»"))


def per_modello(modello: str) -> dict:
    if modello.startswith("C-"):
        return carosello(unita=modello == "C-voci", primadopo=modello == "C-primadopo")
    return stories(unita=modello == "S-voci")
