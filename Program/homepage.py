import streamlit as st

st.set_page_config(
    page_title="CreditScore Pro",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
    <style>
    /* Fundalul general al paginii */
    .stApp {
        background-color: #F0F9F4 !important;
    }
    
    /* Se forteaza culoarea textului pentru TOATE elementele standard Streamlit */
    .stApp, .stMarkdown, p, li, span, label {
        color: #2D5A43 !important;
    }

    /* Se forteaza culoarea pentru Titluri și Subtitluri explicit */
    h1, h2, h3, h4, h5, h6 {
        color: #1B3C2B !important;
    }
    
    /* Stil special pentru containere (Carduri) */
    [data-testid="stVerticalBlock"] > div.stColumn > div {
        background-color: #FFFFFF !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border-left: 5px solid #4CAF50 !important;
        box-shadow: 2px 5px 15px rgba(0,0,0,0.08) !important;
    }

    /* Stil butoane */
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Se repara vizibilitatea textului în Info Boxes */
    .stAlert p {
        color: #155724 !important;
    }
    .logo-img {
        max-height: 50px !important; /* Ajustează înălțimea aici */
        width: auto;
    }
    .custom-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
        height: 250px; /* Optional: forces cards to be same height */
    }        
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
LOGO_URL_LARGE = 'resources/logo_correct.png'
LOGO_URL_SMALL = 'resources/logo_mini_correct.png'

st.logo(
    LOGO_URL_LARGE,
    icon_image=LOGO_URL_SMALL,
)

# --- SIDEBAR ---
with st.sidebar:
    st.success("Sunteți pe pagina principală")
    st.info("💡 **Eco-Sfat:** Creditele pentru case verzi au dobânzi cu până la 0.5% mai mici!")

# --- HERO SECTION ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.title("Descoperă-ți Potențialul Financiar 📈")
    st.markdown("""
    <p style='font-size: 1.2em; color: #4F7963;'>
    Verifică-ți eligibilitatea pentru credit rapid și ușor. Obține oferte personalizate și sfaturi pentru un viitor financiar sănătos.
    </p>
    """, unsafe_allow_html=True)
    
    if st.button("❔ Verifică Eligibilitatea"):
        st.switch_page("pages/1_verificare_credit.py")

with col2:
    st.image("resources/vecteezy_man-saves-money-from-business-investment-in-bank_4474434-1.jpg", use_container_width=True)

st.write("---")

# --- SECȚIUNE EDUCAȚIE FINANCIARĂ ---
st.header("🪙 Resurse pentru Tine")
ed_col1, ed_col2, ed_col3 = st.columns(3)

with ed_col1:
    st.markdown(f'''
        <div class="custom-card">
            <h3>💳 Ghid Credite</h3>
            <p>Este un credit într-adevăr necesar? Iată cum poți afla instant.</p>
        </div>
    ''', unsafe_allow_html=True)
    st.link_button("Deschide Ghid", "https://www.bcr.ro/ro/news-hub/blog/noutati/ghid-complet-pentru-obtinerea-unui-credit-de-nevoi-personale-in-romania", use_container_width=True)

with ed_col2:
    st.markdown(f'''
        <div class="custom-card" style="background-color: #e1f5fe;">
            <h3>💰 Economii Smart</h3>
            <p>Cum să îți gestionezi bugetul pentru a deveni eligibil mai repede.</p>
        </div>
    ''', unsafe_allow_html=True)
    st.link_button("Vezi Sfaturi", "https://www.economica.net/cum-te-ajuta-un-cont-online-sa-iti-gestionezi-eficient-un-credit-de-nevoi-personale_934461.html", use_container_width=True)

with ed_col3:
    st.markdown(f'''
        <div class="custom-card" style="background-color: #e8f5e9;">
            <h3>📈 Scorul FICO</h3>
            <p>Ce este și cum poți să îl îmbunătățești în doar 6 luni.</p>
        </div>
    ''', unsafe_allow_html=True)
    st.link_button("Află mai multe", "https://www.birouldecredit.ro/wps/portal/bcro/Home/servicii/", use_container_width=True)

st.write("")
st.header("📰 Noutăți din Piață")
c1, c2 = st.columns(2)

with c1:
    st.info("**Ziarul Financiar:** Dobânzile la creditele ipotecare înregistrează o ușoară scădere.")
with c2:
    st.info("**Profit.ro:** Noi reglementări BNR privind gradul de îndatorare maxim.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8em;'>
        CreditScore Pro © 2026 | Instrument de simulare informativ. Nu reprezintă un angajament contractual.
    </div>
    """, unsafe_allow_html=True)