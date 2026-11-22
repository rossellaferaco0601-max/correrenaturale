// Guida: controllo dell'impaginazione (nessun blocco oltre il piè di pagina), un'immagine per pagina e il PDF.
// Uso (da video-engine): node work/ytcn26/guida/export.js cartella_uscita   → guida_NN.png, Come-scaldarsi-quando-fa-freddo.pdf
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

(async () => {
  const out = path.resolve(process.argv[2] || "out/ytcn26/guida");
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto("file://" + path.resolve(__dirname, "guida.html"));
  await p.waitForTimeout(800);
  const over = await p.evaluate(() =>
    [...document.querySelectorAll("section.page")].map((s, i) => {
      const top = s.getBoundingClientRect().top;
      let max = 0;
      s.querySelectorAll(".pad > *, .txt > *").forEach((e) => {
        max = Math.max(max, e.getBoundingClientRect().bottom - top);
      });
      const cover = s.classList.contains("cover");
      return { pagina: i + 1, fondo: Math.round(max), ok: cover ? max <= 1300 : max <= 1282 };
    })
  );
  over.forEach((o) => console.log("pagina " + String(o.pagina).padStart(2) + ": contenuto fino a " + o.fondo + " px " + (o.ok ? "ok" : "ESCE (limite 1282)")));
  const secs = await p.$$("section.page");
  for (let i = 0; i < secs.length; i++) {
    await secs[i].screenshot({ path: out + "/guida_" + String(i + 1).padStart(2, "0") + ".png" });
  }
  await p.pdf({ path: out + "/Come-scaldarsi-quando-fa-freddo.pdf", width: "1080px", height: "1350px", printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await b.close();
  console.log(secs.length + " pagine in " + out);
})();
