import streamlit as st
import pandas as pd
from fpdf import FPDF
import io
from datetime import date

st.set_page_config(
    page_title="Generatore Distinte di Pagamento",
    page_icon="🏦",
    layout="wide"
)

# --- CLASSE GENERAZIONE PDF ---
class DistintaPDF(FPDF):
    def __init__(self, ordinante_info):
        super().__init__()
        self.ordinante_info = ordinante_info

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "DISTINTA DI PAGAMENTO BONIFICI", ln=True, align="C")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, f"Data Creazione: {date.today().strftime('%d/%m/%Y')}", ln=True, align="C")
        self.ln(6)
        
        # Box Dati Ordinante
        self.set_fill_color(240, 240, 240)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, " DATI ORDINANTE / CONTO DI ADDEBITO", ln=True, fill=True)
        self.set_font("Helvetica", "", 9)
        self.cell(95, 5, f" Ragione Sociale: {self.ordinante_info['ragione_sociale']}", ln=False)
        self.cell(95, 5, f"Banca: {self.ordinante_info['banca']}", ln=True)
        self.cell(95, 5, f" IBAN: {self.ordinante_info['iban']}", ln=False)
        self.cell(95, 5, f"Data Esecuzione Richiesta: {self.ordinante_info['data_esecuzione']}", ln=True)
        self.ln(6)

    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 4, "Documento generato ad uso interno e per autorizzazione disposizioni bancarie.", align="C", ln=True)
        self.cell(0, 4, f"Pagina {self.page_no()}", align="C")

def genera_pdf_distinta(ordinante_info, df_disposizioni, totale_importo):
    pdf = DistintaPDF(ordinante_info)
    pdf.add_page()
    
    # Intestazione Tabella
    pdf.set_fill_color(30, 60, 90)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    
    # Larghezze colonne (totale = 190mm)
    col_w = [10, 45, 55, 55, 25]
    headers = ["N°", "Beneficiario", "IBAN", "Causale", "Importo (€)"]
    
    for w, header in zip(col_w, headers):
        pdf.cell(w, 7, header, border=1, align="C", fill=True)
    pdf.ln()
    
    # Righe Dati
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 8)
    fill = False
    
    for idx, row in df_disposizioni.iterrows():
        pdf.set_fill_color(248, 249, 250) if fill else pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(col_w[0], 6, str(idx + 1), border=1, align="C", fill=fill)
        pdf.cell(col_w[1], 6, str(row.get("Beneficiario", ""))[:25], border=1, fill=fill)
        pdf.cell(col_w[2], 6, str(row.get("IBAN", "")), border=1, fill=fill)
        pdf.cell(col_w[3], 6, str(row.get("Causale", ""))[:30], border=1, fill=fill)
        pdf.cell(col_w[4], 6, f"{float(row.get('Importo (€)', 0)):,.2f}", border=1, align="R", fill=fill)
        pdf.ln()
        fill = not fill

    # Totale
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(sum(col_w[:4]), 7, "TOTALE DISTINTA  ", border=1, align="R")
    pdf.cell(col_w[4], 7, f"{totale_importo:,.2f} €", border=1, align="R")
    pdf.ln(12)

    # Firma e Autorizzazione
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(95, 6, "Luogo e Data: ________________________", ln=False)
    pdf.cell(95, 6, "Firma del Legale Rappresentante / Ordinante", ln=True)
    pdf.ln(10)
    pdf.cell(95, 6, "", ln=False)
    pdf.cell(95, 6, "__________________________________________", ln=True)

    return bytes(pdf.output())


# --- INTERFACCIA UTENTE STREAMLIT ---
st.title("🏦 Generatore Distinte di Pagamento")
st.markdown("Crea, verifica ed esporta le distinte di bonifico per la banca.")

# Sidebar - Dati Ordinante
with st.sidebar:
    st.header("⚙️ Dati Ordinante")
    ragione_sociale = st.text_input("Ragione Sociale / Nome", value="")
    banca_ordinante = st.text_input("Banca di Addebito", value="")
    iban_ordinante = st.text_input("IBAN Ordinante", value="")
    data_esecuzione = st.date_input("Data Esecuzione Richiesta", value=date.today())

st.subheader("1. Inserimento Disposizioni di Pagamento")

# Option Tabella Interattiva o Import File
tab_manual, tab_import = st.tabs(["✍️ Inserimento Manuale / Tabella", "📁 Importa da Excel/CSV"])

initial_data = pd.DataFrame({
    "Beneficiario": ["Mario Rossi", "Fornitore Alfa Srl"],
    "IBAN": ["IT60X0542811101000000123456", "IT99C0306902123000000987654"],
    "Importo (€)": [1500.00, 4350.50],
    "Causale": ["Avanzo competenze", "Fattura n. 102/2026"]
})

with tab_manual:
    df_edited = st.data_editor(
        initial_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Beneficiario": st.column_config.TextColumn("Beneficiario", required=True),
            "IBAN": st.column_config.TextColumn("IBAN Beneficiario", required=True),
            "Importo (€)": st.column_config.NumberColumn("Importo (€)", format="%.2f", min_value=0.01, required=True),
            "Causale": st.column_config.TextColumn("Causale Pagamento", required=True)
        }
    )

with tab_import:
    uploaded_file = st.file_uploader("Carica file Excel o CSV con le colonne (Beneficiario, IBAN, Importo (€), Causale)", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_imported = pd.read_csv(uploaded_file)
            else:
                df_imported = pd.read_excel(uploaded_file)
            st.success("File caricato con successo!")
            df_edited = df_imported
        except Exception as e:
            st.error(f"Errore nella lettura del file: {e}")

# Pulsante di Sincronizzazione / Validazione Dati
df_final = df_edited.dropna(subset=["Beneficiario", "Importo (€)"]).copy()
df_final["Importo (€)"] = pd.to_numeric(df_final["Importo (€)"], errors="coerce").fillna(0.0)

# --- RIEPILOGO METRICHE ---
st.divider()
st.subheader("2. Riepilogo Distinta")

col1, col2, col3 = st.columns(3)
totale_pagamenti = float(df_final["Importo (€)"].sum())
num_operazioni = len(df_final)

with col1:
    st.metric("Numero Bonifici", num_operazioni)
with col2:
    st.metric("Importo Totale Distinta", f"€ {totale_pagamenti:,.2f}")
with col3:
    st.metric("Data Esecuzione", data_esecuzione.strftime("%d/%m/%Y"))

# --- ESPORTAZIONE E DOWNLOAD ---
st.divider()
st.subheader("3. Esporta e Scarica Documenti")

if num_operazioni == 0:
    st.warning("Inserisci almeno una disposizione valida per generare i documenti.")
elif not ragione_sociale or not iban_ordinante:
    st.warning("Compila i dati dell'ordinante nella barra laterale a sinistra.")
else:
    col_pdf, col_csv = st.columns(2)
    
    # Payload dati ordinante
    ordinante_info = {
        "ragione_sociale": ragione_sociale,
        "banca": banca_ordinante,
        "iban": iban_ordinante,
        "data_esecuzione": data_esecuzione.strftime("%d/%m/%Y")
    }
    
    # 1. Generazione PDF
    pdf_data = genera_pdf_distinta(ordinante_info, df_final, totale_pagamenti)
    
    with col_pdf:
        st.download_button(
            label="📄 Scarica Distinta PDF (Firmabile)",
            data=pdf_data,
            file_name=f"distinta_pagamento_{data_esecuzione.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    # 2. Generazione CSV/Excel per la Banca
    csv_buffer = io.StringIO()
    df_final.to_csv(csv_buffer, index=False, sep=";")
    
    with col_csv:
        st.download_button(
            label="📊 Scarica Tracciato CSV / Excel per Banca",
            data=csv_buffer.getvalue(),
            file_name=f"export_bonifici_{data_esecuzione.strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
