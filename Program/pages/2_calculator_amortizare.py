import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

class CalculatorAmortizare:
    def __init__(self, principal, dobanda_anuala, ani, tip_rata, plata_extra=0):
        self.principal = principal
        self.dobanda_anuala = dobanda_anuala
        self.luni = ani * 12
        self.tip_rata = tip_rata
        self.plata_extra = plata_extra

    def genereaza_scadentar(self):
        r_lunara = (self.dobanda_anuala / 100) / 12
        sold_ramas = self.principal
        date_tabel = []
        
        # Calcul Anuitate (Rată Egală) pe baza formulei standard
        if r_lunara > 0:
            rata_anuitate = self.principal * (r_lunara * (1 + r_lunara)**self.luni) / ((1 + r_lunara)**self.luni - 1)
        else:
            rata_anuitate = self.principal / self.luni

        for luna in range(1, self.luni + 1):
            if sold_ramas <= 0:
                break
                
            dobanda_luna = sold_ramas * r_lunara
            
            if self.tip_rata == "Anuități (Rate Egale)":
                princ_luna = rata_anuitate - dobanda_luna
            else: 
                # Rate Descrescătoare
                princ_luna = self.principal / self.luni
            
            # Plata antiticipată se adaugă la principalul lunar
            plata_totala_luna = princ_luna + dobanda_luna + self.plata_extra
            princ_total_luna = princ_luna + self.plata_extra
            
            # Se verifica dacă plata totală depășește soldul rămas
            if princ_total_luna > sold_ramas:
                princ_total_luna = sold_ramas
                plata_totala_luna = princ_total_luna + dobanda_luna
                sold_ramas = 0
            else:
                sold_ramas -= princ_total_luna

            date_tabel.append({
                "Luna": luna,
                "Rată Totală": round(plata_totala_luna, 2),
                "Principal": round(princ_total_luna, 2),
                "Dobândă": round(dobanda_luna, 2),
                "Sold Rămas": round(sold_ramas, 2)
            })
            
        return pd.DataFrame(date_tabel)

st.set_page_config(page_title="Calculator Amortizare Avansat", layout="wide")

st.title("📊 Calculator Amortizare Credit")
st.markdown("Acest modul permite simularea detaliată a unui credit, inclusiv impactul **plăților anticipate**.")

# Sidebar pentru Input
with st.sidebar:
    st.header("⚙️ Parametri Credit")
    suma = st.number_input("Suma Împrumutată (RON)", 5000, 2000000, 150000, step=5000)
    ani = st.slider("Durata Creditului (Ani)", 1, 35, 15)
    dobanda = st.number_input("Rata Dobânzii Anuale (%)", 0.1, 25.0, 7.2, step=0.1)
    tip = st.selectbox("Metoda de Rambursare", ["Anuități (Rate Egale)", "Rate Descrescătoare"])
    
    st.divider()
    st.header("🚀 Strategie de Economisire")
    plata_extra = st.number_input("Plată Anticipată Lunară (RON)", 0, 10000, 0, step=100)

# Procesare Date
calc = CalculatorAmortizare(suma, dobanda, ani, tip, plata_extra)
df = calc.genereaza_scadentar()

# Metrici Principale
total_plata = df["Rată Totală"].sum()
total_dobanda = df["Dobândă"].sum()
economie_timp = (ani * 12) - len(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rată Lunară Medie", f"{round(df['Rată Totală'].mean(), 2)} RON")
col2.metric("Total Dobândă", f"{round(total_dobanda, 2)} RON")
col3.metric("Total de Plată", f"{round(total_plata, 2)} RON")
col4.metric("Timp Economisit", f"{economie_timp} Luni", delta=f"{economie_timp // 12} Ani")

# Vizualizare Grafică
st.subheader("📈 Analiza Evoluției Creditului")
fig = px.area(df, x="Luna", y=["Principal", "Dobândă"], 
              labels={"value": "Suma (RON)", "variable": "Componentă"},
              color_discrete_map={"Principal": "#00CC96", "Dobândă": "#EF553B"},
              title="Raportul Principal vs Dobândă pe parcursul creditului")
st.plotly_chart(fig, use_container_width=True)

# Tabel și Export
with st.expander("📄 Vezi Scadențarul Detaliat"):
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-16')
    st.download_button("📥 Descarcă Tabelul (CSV)", data=csv, file_name="scadentar_credit.csv", mime="text/csv")