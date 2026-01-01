import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Streamlit - Upload et Nettoyage de Données",
    page_icon="📊",
    layout="wide"
)

st.title("📂 Application de Visualisation et Nettoyage de Données")
st.write("Cette application permet d'uploader un fichier, visualiser les données, les nettoyer et les analyser.")

# =========================
# UPLOAD DU FICHIER
# =========================
st.subheader("📁 Upload du fichier CSV")
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:

    # Stockage du dataframe dans session_state
    if "df" not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)

    df = st.session_state.df

    # =========================
    # APERCU DES DONNÉES
    # =========================
    st.subheader("📊 Aperçu des données")
    st.dataframe(df, use_container_width=True)

    # =========================
    # NETTOYAGE
    # =========================
    st.subheader("🧹 Nettoyage des données")

    col1, col2 = st.columns(2)

    with col1:
        action = st.radio(
            "Choisissez une action de nettoyage",
            ["Aucune", "Supprimer les lignes vides", "Supprimer les doublons"]
        )

        if action == "Supprimer les lignes vides":
            df = df.dropna()
            st.session_state.df = df
            st.success("✔ Lignes vides supprimées.")

        elif action == "Supprimer les doublons":
            df = df.drop_duplicates()
            st.session_state.df = df
            st.success("✔ Doublons supprimés.")

    with col2:
        st.write(f"🔢 Nombre de lignes : **{df.shape[0]}**")
        st.write(f"📐 Nombre de colonnes : **{df.shape[1]}**")

    st.dataframe(df, use_container_width=True)

    # =========================
    # VISUALISATION
    # =========================
    st.subheader("📊 Visualisation des données")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
            "Choisissez une colonne numérique pour l'histogramme",
            numeric_cols
        )

        fig, ax = plt.subplots()
        ax.hist(df[selected_col], bins=20)
        ax.set_title(f"Histogramme de {selected_col}")
        ax.set_xlabel(selected_col)
        ax.set_ylabel("Fréquence")

        st.pyplot(fig)
    else:
        st.warning("⚠️ Aucune colonne numérique trouvée pour l'histogramme.")

    # =========================
    # STATISTIQUES
    # =========================
    st.subheader("📈 Statistiques descriptives")
    st.write(df.describe())

    # =========================
    # TELECHARGEMENT
    # =========================
    st.subheader("💾 Télécharger le dataset nettoyé")
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Télécharger le CSV nettoyé",
        data=csv,
        file_name="dataset_nettoye.csv",
        mime="text/csv"
    )

    # =========================
    # RESET
    # =========================
    if st.button("🔄 Réinitialiser le dataset"):
        del st.session_state.df
        st.success("Dataset réinitialisé. Rechargez le fichier.")
