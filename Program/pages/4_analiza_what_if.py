import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class AnalizaSensibilitate:
    def calculate_totals(self, principal, dobanda_anuala, luni, extra_lunar=0):
        r = (dobanda_anuala / 100) / 12
        sold = principal
        total_dobanda = 0
        luni_reale = 0
        
        # Calcul rată standard (Anuitate)
        if r > 0:
            rata_fixa = principal * (r * (1 + r)**luni) / ((1 + r)**luni - 1)
        else:
            rata_fixa = principal / luni

        while sold > 0 and luni_reale < 600: # Limitare la 50 ani
            luni_reale += 1
            dobanda_luna = sold * r
            principal_luna = (rata_fixa - dobanda_luna) + extra_lunar
            
            if sold < principal_luna:
                total_dobanda += dobanda_luna
                sold = 0
            else:
                total_dobanda += dobanda_luna
                sold -= principal_luna
                
        return round(total_dobanda, 2), luni_reale

def render_what_if_page():
    st.title("🧪 Analiză de Sensibilitate What-If")
    st.markdown("Compară scenariul actual cu posibile schimbări ale pieței sau strategii de plată.")

    analiza = AnalizaSensibilitate()

    # --- INPUTURI SCENARIU DE BAZĂ ---
    with st.sidebar:
        st.header("📍 Scenariu de Bază")
        p = st.number_input("Suma Creditului", value=200000)
        d_baza = st.slider("Dobândă Anuală Bază (%)", 1.0, 20.0, 7.0)
        t_baza = st.slider("Durata Bază (Ani)", 5, 30, 20)
        
    # --- INPUTURI WHAT-IF ---
    st.subheader("Modifică variabilele pentru a vedea impactul")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📉 Scenariu: Creștere Dobândă (Risc de Piață)")
        d_nou = st.slider("Noua Dobândă (%)", 1.0, 20.0, d_baza + 2.0)
        
    with col2:
        st.success("💰 Scenariu: Plată Anticipată (Strategie)")
        extra = st.number_input("Plată extra lunară (RON)", 0, 5000, 500)

    # Calcule
    dobanda_baza, timp_baza = analiza.calculate_totals(p, d_baza, t_baza * 12)
    dobanda_what_if, timp_what_if = analiza.calculate_totals(p, d_nou, t_baza * 12, extra)

    # --- VIZUALIZARE METRICI COMPARATIVE ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    
    diff_dobanda = dobanda_what_if - dobanda_baza
    m1.metric("Total Dobândă Scenariu Nou", f"{dobanda_what_if} RON", delta=f"{diff_dobanda} RON", delta_color="inverse")
    
    diff_timp = timp_what_if - timp_baza
    m2.metric("Durată Nouă", f"{timp_what_if} Luni", delta=f"{diff_timp} Luni", delta_color="inverse")
    
    economie_potentiala = dobanda_baza - dobanda_what_if if dobanda_what_if < dobanda_baza else 0
    m3.metric("Economie Totală", f"{economie_potentiala} RON")

    # --- GRAFIC COMPARATIV ---
    st.subheader("Comparație Cost Total: Bază vs. What-If")
    
    fig = go.Figure(data=[
        go.Bar(name='Dobândă Bază', x=['Costuri'], y=[dobanda_baza], marker_color='#636EFA'),
        go.Bar(name='Dobândă What-If', x=['Costuri'], y=[dobanda_what_if], marker_color='#EF553B'),
        go.Bar(name='Capital Împrumutat', x=['Costuri'], y=[p], marker_color='#00CC96')
    ])
    fig.update_layout(barmode='stack', title="Compoziție Cost Total Credit")
    st.plotly_chart(fig, use_container_width=True)

    st.warning(f"💡 **Concluzie:** În scenariul 'What-If', vei plăti cu **{abs(diff_dobanda)} RON** {'mai mult' if diff_dobanda > 0 else 'mai puțin'} față de planul inițial.")

if __name__ == "__main__":
    render_what_if_page()