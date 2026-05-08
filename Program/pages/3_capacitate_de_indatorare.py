import streamlit as st
import pandas as pd

class CalculatorGradIndatorare:
    def __init__(self):
        self.PRAG_BNR = 0.40  # 40% limita standard
        self.PRAG_REFINANTARE = 0.60 # Excepție pentru anumite refinanțări

    def calculeaza_capacitate(self, venit_net, rate_existente, alte_cheltuieli, prag_ales):        
        # Venitul disponibil după cheltuieli de subzistență și alte cheltuieli
        venit_disponibil = venit_net - alte_cheltuieli

        # Rata maximă totală permisă (conform BNR)
        rata_maxima_totala = venit_disponibil * prag_ales
        
        # Cât mai poate suporta clientul pentru un credit nou
        capacitate_rata_noua = rata_maxima_totala - rate_existente
        
        # Gradul actual de îndatorare
        grad_actual = (rate_existente / venit_net) * 100 if venit_net > 0 else 0
        
        return {
            "grad_actual": round(grad_actual, 2),
            "rata_maxima_posibila": round(max(0, capacitate_rata_noua), 2),
            "este_eligibil": capacitate_rata_noua > 0,
            "venit_disponibil": venit_disponibil
        }

def render_pagina_capacitate():
    st.title("🏛️ Calculator Capacitate de Îndatorare")
    st.info("Acest calculator verifică încadrarea în limitele de creditare impuse de Banca Națională a României.")

    calc = CalculatorGradIndatorare()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Venituri și Cheltuieli")
        venit = st.number_input("Venit Net Lunar (familie/personal)", 0, 50000, 5000, step=100)
        cheltuieli_subzistenta = st.number_input("Cheltuieli de subzistență (estimat)", 0, 5000, 800, step=100)
        rate_actuale = st.number_input("Total rate credite existente", 0, 10000, 0, step=50)
        
    with col2:
        st.subheader("Parametri Reglementare")
        prag = st.selectbox("Grad Maxim Admis", 
                            options=[0.40, 0.60], 
                            format_func=lambda x: f"{int(x*100)}% (Standard BNR)" if x == 0.40 else f"{int(x*100)}% (Refinanțare/Excepții)")
        
        st.warning(f"Conform normelor, rata totală nu poate depăși {int(prag*100)}% din venitul net.")
        st.info("💡 Notă informativă: Calculul actual scade cheltuielile de subzistență din venitul tău înainte de a aplica limita de îndatorare, oferindu-ți o estimare mult mai realistă a siguranței tale financiare.")

    # Calcul Rezultate
    rezultat = calc.calculeaza_capacitate(venit, rate_actuale, cheltuieli_subzistenta, prag)

    st.divider()

    # Afișare Rezultate
    c1, c2, c3 = st.columns(3)
    c1.metric("Grad Îndatorare Actual", f"{rezultat['grad_actual']}%")
    c2.metric("Rată Maximă Nouă", f"{rezultat['rata_maxima_posibila']} RON")
    
    status = "ELIGIBIL" if rezultat['este_eligibil'] else "LIMITĂ DEPĂȘITĂ"
    c3.metric("Status Eligibilitate", status)

    # Vizualizare Grafică
    st.subheader("Analiza Venitului")
    
    # Date pentru grafic
    procent_rate = rezultat['grad_actual']
    procent_subzistenta = (cheltuieli_subzistenta/ venit) * 100 if venit > 0 else 0
    procent_disponibil_nou = (rezultat['rata_maxima_posibila'] / venit * 100) if venit > 0 else 0
    procent_liber = 100 - procent_rate - procent_disponibil_nou - procent_subzistenta
    
    chart_data = pd.DataFrame({
        "Categorie": ["Rate Existente", "Subzistență", "Capacitate Credit Nou", "Venit Liber"],
        "Procent": [procent_rate, procent_subzistenta, procent_disponibil_nou, procent_liber]
    })

    import plotly.express as px
    fig = px.pie(chart_data, 
                 values='Procent', 
                 names='Categorie', 
                 color_discrete_sequence=['#00CC96',  '#FECB52', '#636EFA', '#EF553B'],
                 hole=0.4)
    
    st.plotly_chart(fig)

    if not rezultat['este_eligibil']:
        st.error(f"⚠️ Atenție: Gradul de îndatorare depășește pragul de {int(prag*100)}%. Nu mai puteți accesa credite noi în acest moment.")
    else:
        st.success(f"✅ Clientul poate suporta o rată suplimentară de până la {rezultat['rata_maxima_posibila']} RON.")

if __name__ == "__main__":
    render_pagina_capacitate()