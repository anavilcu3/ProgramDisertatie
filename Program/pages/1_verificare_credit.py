import streamlit as st
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Sistem Suport Decizie - Credit", layout="wide")

# Funcție pentru a lua cursul USD în timp real
@st.cache_data(ttl=3600) 
def get_official_bnr_usd():
    url = "https://www.bnr.ro/nbrfxrates.xml"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespace = {'bnr': 'http://www.bnr.ro/xsd'}
        
        rates = root.findall('.//bnr:Rate', namespace)
        for rate in rates:
            if rate.get('currency') == 'USD':
                return rate.text
                
        return "USD not found in feed"
    except Exception as e:
        return f"Error: {e}"

def get_live_usd_rate():
    usd_value = get_official_bnr_usd() 
    try:
        return float(usd_value)
    except (ValueError, TypeError):
        st.error(f"Nu s-a putut converti cursul valutar: {usd_value}")
        return 4.60  

usd_rate = get_live_usd_rate()

@st.cache_resource
def load_assets():
    try:
        with open('model_final.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("Eroare: Fișierul 'model_final.pkl' nu a fost găsit.")
        return None

assets = load_assets()

if assets:
    model = assets["model"]
    features_antrenare = assets.get("features", [])

    st.title("🏦 Sistem Inteligent de Evaluare a Riscului de Credit")
    
    with st.form("credit_form_complet"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Profil Personal")
            gender = st.selectbox("Gen", ["Masculin", "Feminin"])
            married = st.selectbox("Căsătorit", ["Da", "Nu"])
            dependents = st.selectbox("Persoane în întreținere", ["0", "1", "2", "3"])
            education = st.selectbox("Educație", ["Absolvent", "Fără Absolvire"])
            self_employed = st.selectbox("Independent (PFA/SRL)", ["Da", "Nu"])
            
        with col2:
            st.subheader("Date Financiare")
            income = st.number_input("Venit Lunar Solicitant (RON)", min_value=0, value=3000)
            co_income = st.number_input("Venit Lunar Co-solicitant (RON)", min_value=0, value=0)
            loan_amount = st.number_input("Suma Creditului (RON)", min_value=0, value=5000)
            term = st.selectbox("Termen Credit (Ani)", [30, 20, 15, 10, 7, 5, 3])
            st.caption(f"ℹ️ Curs utilizat: 1 USD = {usd_rate} RON")

        with col3:
            st.subheader("Istoric și Proprietate")
            credit_history = st.selectbox("Istoric Credit", ["Bun", "Rău"])
            property_area = st.selectbox("Zona Proprietății", ["Urban", "Semiurban", "Rural"])

        submit = st.form_submit_button("Analizează Cererea de Credit")

    if submit:

        try:

            # Se convertesc valorile în USD pentru a fi în același format ca datele de antrenare
            income_usd = income / usd_rate
            co_income_usd = co_income / usd_rate
            loan_usd = loan_amount / usd_rate/ 1000  # Modelul a fost antrenat pe mii de dolari

            term_months = term * 12  # Convertim ani în luni

            input_dict = {
                'Gender': float(0.0 if gender == 'Feminin' else 1.0),
                'Married': float(1.0 if married == 'Da' else 0.0),
                'Dependents': float({"0": 0.0, "1": 1.0, "2": 2.0, "3": 3.0}[dependents]),
                'Education': float(0.0 if education == 'Absolvent' else 1.0),
                'Self_Employed': float(1.0 if self_employed == 'Da' else 0.0),
                'ApplicantIncome': float(income_usd),
                'CoapplicantIncome': float(co_income_usd),
                'LoanAmount': float(loan_usd),
                'Loan_Amount_Term': float(term_months),
                'Credit_History': float(1.0 if "Bun" in credit_history else 0.0),
                'Property_Area': float({"Rural": 0.0, "Semiurban": 1.0, "Urban": 2.0}[property_area])
            }
            
            df_input = pd.DataFrame([input_dict])
            
            if features_antrenare:
                df_input = df_input[features_antrenare]
            else:
                column_order = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 
                                'Property_Area', 'Credit_History', 'ApplicantIncome', 
                                'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
                df_input = df_input[column_order]

            # Predicție
            proba = model.predict_proba(df_input)[0][1]
            
            # Afișare rezultate
            st.divider()
            c_res1, c_res2 = st.columns(2)
            with c_res1:
                st.metric("Probabilitate de Aprobare", f"{proba:.2%}")

                st.subheader("🔍 Analiza Factorilor de Risc")

                importances = model.feature_importances_
                feature_names = assets["features"]
                translations = {
                    'Gender': 'Gen',
                    'Married': 'Căsătorit',         
                    'Dependents': 'Dependenți',
                    'Education': 'Educație',
                    'Self_Employed': 'Angajat pe cont propriu',
                    'Property_Area': 'Zonă Imobil',
                    'Credit_History': 'Istoric Credit',
                    'ApplicantIncome': 'Venit Solicitant',
                    'CoapplicantIncome': 'Venit Co-solicitant',
                    'LoanAmount': 'Sumă Credit',
                    'Loan_Amount_Term': 'Termen Credit'
                }
                translated_names_list = [translations.get(name, name) for name in feature_names]
                feat_imp = pd.Series(importances, index=translated_names_list).sort_values(ascending=False)
                
                # Afișarea primilor 3 factori care au influențat rezultatul
                st.write("Principalii factori care au determinat acest rezultat:")
                for i in range(3):
                    st.write(f"{i+1}. **{feat_imp.index[i]}** (impact: {feat_imp.values[i]:.2%})")
            with c_res2:
                if proba > 0.7:
                    st.success("✅ RECOMANDARE: APROBARE")
                elif proba > 0.4:
                    st.warning("⚠️ RECOMANDARE: ANALIZĂ SUPLIMENTARĂ")
                else:
                    st.error("❌ RECOMANDARE: RESPINGERE")

        except Exception as e:
            st.error(f"Eroare la procesarea datelor: {e}")