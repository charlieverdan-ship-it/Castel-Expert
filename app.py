import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Castel-Expert", layout="wide")

# Style CSS pour un rendu "Cabinet d'Expertise"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #1e3a8a; }
    h2 { color: #1e40af; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (PARAMÈTRES) ---
st.sidebar.header("⚙️ Paramètres du Projet")
tmi = st.sidebar.slider("Taux Marginal d'Imposition (TMI) associé", 0, 45, 30, step=5)
montant_travaux = st.sidebar.number_input("Budget total des travaux (€)", min_value=0, value=500000, step=50000)
duree_amortissement = st.sidebar.slider("Durée amortissement IS (Hôtellerie)", 10, 30, 20)

st.sidebar.markdown("---")
st.sidebar.info("💡 Basé sur l'Article 156 bis du CGI et les BOFiP mis à jour en 2024.")

# --- TITRE PRINCIPAL ---
st.title("🏰 Castel-Expert")
st.markdown("### Aide à la décision : Transformation de Monument Historique en Hôtel")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🛡️ Diagnostic de Sécurité", "📊 Arbitrage Fiscal", "🧱 Nature des Travaux"])

# --- TAB 1 : DIAGNOSTIC ---
with tab1:
    st.header("Diagnostic de conformité (Art. 156 bis CGI)")
    col1, col2 = st.columns(2)
    
    with col1:
        sci_familiale = st.radio("La SCI est-elle familiale ?", ["Oui", "Non"], help="Associés parents jusqu'au 4ème degré.")
        surface_hab = st.slider("% Surface conservée en habitation", 0, 100, 80)
        engagement_15 = st.checkbox("Engagement de conservation de 15 ans", value=True)

    with col2:
        # Logique de score basée sur tes fondements juridiques
        score = 0
        if engagement_15: score += 40
        if sci_familiale == "Oui": score += 60
        else:
            if surface_hab >= 75: score += 50
            else: score -= 20
        
        st.subheader("Indice de Sécurisation Fiscale")
        if score >= 90:
            st.success(f"Score : {score}/100 - Risque de requalification : FAIBLE")
            st.write("Le montage respecte les conditions dérogatoires du CGI.")
        elif score >= 50:
            st.warning(f"Score : {score}/100 - Risque de requalification : MODÉRÉ")
            st.write("Attention au seuil des 75% d'habitation pour les SCI non-familiales.")
        else:
            st.error(f"Score : {score}/100 - Risque de requalification : ÉLEVÉ")
            st.write("Le changement d'affectation commerciale totale menace la déduction MH.")

# --- TAB 2 : ARBITRAGE ---
with tab2:
    st.header("Simulation de l'avantage fiscal net")
    
    # Calculs simplifiés
    gain_mh = montant_travaux * (tmi / 100)
    economie_is_annuelle = (montant_travaux / duree_amortissement) * 0.25 # IS à 25%
    gain_is_total = economie_is_annuelle * 15 # Sur la durée d'engagement MH
    
    fig = go.Figure(data=[
        go.Bar(name='Régime MH (Déficit Global)', x=['Option IR'], y=[gain_mh], marker_color='#1e3a8a'),
        go.Bar(name='Régime IS (Amortissement)', x=['Option IS'], y=[gain_is_total], marker_color='#94a3b8')
    ])
    
    st.plotly_chart(fig, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Économie d'IR immédiate (MH)", f"{gain_mh:,.0f} €")
    col_b.metric("Économie d'IS cumulée (15 ans)", f"{gain_is_total:,.0f} €")
    
    st.info(f"👉 **Conseil Expert :** Le point de bascule se situe à un TMI de {((gain_is_total/montant_travaux)*100):.1f}%.")

# --- TAB 3 : NATURE DES TRAVAUX ---
with tab3:
    st.header("Classification des dépenses")
    st.write("Ventilation des travaux selon leur nature fiscale (Estimation)")
    
    p_restauration = st.slider("% Travaux de conservation (Toiture, Façade)", 0, 100, 60)
    p_transfo = 100 - p_restauration
    
    labels = ['Déductible MH (Conservation)', 'Amortissable IS (Transformation/Confort)']
    values = [p_restauration, p_transfo]
    
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig_pie)
    
    st.write("⚠️ **Rappel technique :** Les travaux de création de cuisines hôtelières ou de spas ne sont jamais déductibles au titre des MH, même si validés par l'ABF.")

st.markdown("---")
st.caption("Application développée pour le mémoire DEC - Session 2025. Sources : Article 156 bis CGI / Mémento Patrimoine Lefebvre.")
