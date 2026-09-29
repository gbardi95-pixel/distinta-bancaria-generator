# 🏦 Generatore Distinte di Pagamento

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un'applicazione web semplice, intuitiva e leggera sviluppata in **Python** e **Streamlit** per la gestione e la generazione delle distinte di pagamento bancarie per bonifici.

L'applicazione consente di compilare le disposizioni di pagamento sia manualmente tramite una tabella interattiva sia importandole da file Excel/CSV, calcolando automaticamente i totali e fornendo l'export pronto per la firma e l'invio alla banca.

---

## 🚀 Funzionalità Principali

- ✍️ **Inserimento Dati Flessibile**: Tabella dinamica per l'inserimento manuale rapido o caricamento massivo tramite file Excel/CSV.
- 🧮 **Calcolo in Tempo Reale**: Aggiornamento automatico del numero totale di disposizioni e dell'importo complessivo.
- 📄 **Generazione PDF Ufficiale**: Creazione di un documento PDF di sintesi pronto per la stampa, firma autografa o digitale del legale rappresentante.
- 📊 **Export dati per l'Home Banking**: Esportazione in formato CSV con separatore `;` pronta per l'importazione nei portali di Corporate Banking (CBI).
- 🎨 **Interfaccia Pulita**: Avvio con interfaccia neutra/vuota per la massima privacy e usabilità ad ogni riavvio.

---

## 🛠️ Stack Tecnologico

- **[Streamlit](https://streamlit.io/)**: Framework web frontend/backend per Python.
- **[Pandas](https://pandas.pydata.org/)**: Manipolazione ed elaborazione dati tabellari.
- **[FPDF2](https://pyfpdf.github.io/fpdf2/)**: Generazione programmabile di documenti PDF.
- **[OpenPyXL](https://openpyxl.readthedocs.io/)**: Gestione ed elaborazione dei file Excel (`.xlsx`).

---

## 💻 Installazione Locale

Se desideri eseguire l'applicazione sul tuo computer locale:

1. **Clona il repository:**
   ```bash
   git clone https://github.com/tuo-username/distinta-bancaria-generator.git
   cd distinta-bancaria-generator
   ```

2. **Crea ed attiva un ambiente virtuale (opzionale ma consigliato):**
   ```bash
   python -m venv venv
   # Su Windows:
   venv\Scripts\activate
   # Su macOS/Linux:
   source venv/bin/activate
   ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Avvia l'applicazione:**
   ```bash
   streamlit run app.py
   ```

L'applicazione sarà accessibile nel browser all'indirizzo `http://localhost:8501`.

---

## ☁️ Deployment su Streamlit Community Cloud

Per rendere l'applicazione accessibile online gratuitamente:

1. Esegui il fork o il push di questo repository sul tuo account GitHub.
2. Accedi a [share.streamlit.io](https://share.streamlit.io/) tramite il tuo account GitHub.
3. Clicca su **"New app"**.
4. Seleziona il repository, il branch (`main`) e specifica `app.py` come file principale.
5. Clicca su **"Deploy!"**.

---

## 📁 Struttura del Repository

```text
.
├── app.py              # Codice principale dell'applicazione Streamlit
├── requirements.txt    # Dipendenze Python del progetto
└── README.md           # Documentazione del progetto
```

---

## 📜 Licenza

Questo progetto è distribuito sotto licenza **MIT**. Consulta il file `LICENSE` per ulteriori dettagli.
