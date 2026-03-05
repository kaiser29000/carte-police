import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuration de la page (titre de l'onglet et mode plein écran)
st.set_page_config(page_title="Radar Sécurité", page_icon="🛡️", layout="wide")

# Le Super Dictionnaire avec 100% des départements
DEP_DATA = {
    '01': ('Ain', 46.1, 5.3), '02': ('Aisne', 49.6, 3.5), '03': ('Allier', 46.3, 3.2),
    '04': ('Alpes-de-Haute-Provence', 44.1, 6.2), '05': ('Hautes-Alpes', 44.7, 6.1),
    '06': ('Alpes-Maritimes', 43.9, 7.2), '07': ('Ardèche', 44.8, 4.4), '08': ('Ardennes', 49.6, 4.7),
    '09': ('Ariège', 42.9, 1.5), '10': ('Aube', 48.3, 4.2), '11': ('Aude', 43.1, 2.4),
    '12': ('Aveyron', 44.3, 2.7), '13': ('Bouches-du-Rhône', 43.5, 5.1), '14': ('Calvados', 49.0, -0.2),
    '15': ('Cantal', 45.1, 2.7), '16': ('Charente', 45.8, 0.2), '17': ('Charente-Maritime', 45.8, -0.7),
    '18': ('Cher', 47.1, 2.4), '19': ('Corrèze', 45.3, 1.8), '21': ('Côte-d\'Or', 47.3, 4.7),
    '22': ('Côtes-d\'Armor', 48.3, -2.8), '23': ('Creuse', 46.1, 2.0), '24': ('Dordogne', 45.2, 0.7),
    '25': ('Doubs', 47.2, 6.3), '26': ('Drôme', 44.8, 5.3), '27': ('Eure', 49.1, 1.0),
    '28': ('Eure-et-Loir', 48.3, 1.4), '29': ('Finistère', 48.3, -4.1), '2A': ('Corse-du-Sud', 41.9, 8.9),
    '2B': ('Haute-Corse', 42.3, 9.2), '30': ('Gard', 44.0, 4.2), '31': ('Haute-Garonne', 43.4, 1.3),
    '32': ('Gers', 43.7, 0.5), '33': ('Gironde', 44.8, -0.6), '34': ('Hérault', 43.6, 3.3),
    '35': ('Ille-et-Vilaine', 48.2, -1.7), '36': ('Indre', 46.8, 1.7), '37': ('Indre-et-Loire', 47.3, 0.7),
    '38': ('Isère', 45.3, 5.6), '39': ('Jura', 46.8, 5.6), '40': ('Landes', 43.9, -0.8),
    '41': ('Loir-et-Cher', 47.7, 1.3), '42': ('Loire', 45.8, 4.2), '43': ('Haute-Loire', 45.2, 3.8),
    '44': ('Loire-Atlantique', 47.3, -1.7), '45': ('Loiret', 47.9, 2.2), '46': ('Lot', 44.7, 1.7),
    '47': ('Lot-et-Garonne', 44.3, 0.4), '48': ('Lozère', 44.6, 3.5), '49': ('Maine-et-Loire', 47.4, -0.5),
    '50': ('Manche', 49.1, -1.3), '51': ('Marne', 48.9, 4.3), '52': ('Haute-Marne', 48.1, 5.2),
    '53': ('Mayenne', 48.2, -0.8), '54': ('Meurthe-et-Moselle', 48.7, 6.2), '55': ('Meuse', 49.0, 5.3),
    '56': ('Morbihan', 47.8, -2.8), '57': ('Moselle', 49.0, 6.7), '58': ('Nièvre', 47.2, 3.3),
    '59': ('Nord', 50.6, 3.1), '60': ('Oise', 49.4, 2.4), '61': ('Orne', 48.7, 0.2),
    '62': ('Pas-de-Calais', 50.5, 2.3), '63': ('Puy-de-Dôme', 45.7, 3.1),
    '64': ('Pyrénées-Atlantiques', 43.3, -0.8), '65': ('Hautes-Pyrénées', 43.1, 0.2),
    '66': ('Pyrénées-Orientales', 42.6, 2.5), '67': ('Bas-Rhin', 48.6, 7.6), '68': ('Haut-Rhin', 47.9, 7.2),
    '69': ('Rhône', 45.8, 4.6), '70': ('Haute-Saône', 47.7, 6.2), '71': ('Saône-et-Loire', 46.7, 4.5),
    '72': ('Sarthe', 48.0, 0.2), '73': ('Savoie', 45.5, 6.3), '74': ('Haute-Savoie', 46.0, 6.3),
    '75': ('Paris', 48.9, 2.4), '76': ('Seine-Maritime', 49.7, 1.1), '77': ('Seine-et-Marne', 48.6, 3.0),
    '78': ('Yvelines', 48.8, 1.8), '79': ('Deux-Sèvres', 46.5, -0.3), '80': ('Somme', 49.9, 2.3),
    '81': ('Tarn', 43.8, 2.2), '82': ('Tarn-et-Garonne', 44.1, 1.3), '83': ('Var', 43.4, 6.2),
    '84': ('Vaucluse', 44.0, 5.2), '85': ('Vendée', 46.7, -1.3), '86': ('Vienne', 46.6, 0.3),
    '87': ('Haute-Vienne', 45.8, 1.3), '88': ('Vosges', 48.2, 6.3), '89': ('Yonne', 47.8, 3.6),
    '90': ('Territoire de Belfort', 47.6, 6.9), '91': ('Essonne', 48.5, 2.3),
    '92': ('Hauts-de-Seine', 48.8, 2.2), '93': ('Seine-Saint-Denis', 48.9, 2.5),
    '94': ('Val-de-Marne', 48.8, 2.5), '95': ('Val-d\'Oise', 49.1, 2.2),
    '971': ('Guadeloupe', 16.3, -61.6), '972': ('Martinique', 14.7, -61.0),
    '973': ('Guyane', 3.9, -53.1), '974': ('La Réunion', -21.1, 55.5), '976': ('Mayotte', -12.8, 45.2)
}

@st.cache_data(ttl=86400)
def recuperer_donnees_securite():
    api_url = "https://www.data.gouv.fr/api/1/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/"
    res = requests.get(api_url).json()
    
    csv_url = None
    for resource in res.get('resources', []):
        titre = resource.get('title', '').upper()
        if 'DEP' in titre and resource.get('format', '').lower() == 'csv':
            csv_url = resource.get('url')
            break
            
    if not csv_url: return pd.DataFrame()
        
    df = pd.read_csv(csv_url, sep=';', low_memory=False)
    if len(df.columns) == 1:
        df = pd.read_csv(csv_url, sep=',', low_memory=False)
        
    df.columns = df.columns.str.strip()
    
    if 'annee' in df.columns: df.rename(columns={'annee': 'Annee'}, inplace=True)
    elif 'année' in df.columns: df.rename(columns={'année': 'Annee'}, inplace=True)
    elif 'Année' in df.columns: df.rename(columns={'Année': 'Annee'}, inplace=True)
        
    if 'Code_departement' in df.columns:
        df['Code_departement'] = df['Code_departement'].astype(str)
        df['Code_departement'] = df['Code_departement'].str.replace(r'\.0$', '', regex=True) 
        df['Code_departement'] = df['Code_departement'].str.strip().str.zfill(2)
    
    if 'nombre' in df.columns:
        df['nombre'] = df['nombre'].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.')
        df['nombre'] = pd.to_numeric(df['nombre'], errors='coerce') 
        
    return df

# EN-TÊTE PRINCIPAL
st.title("🛡️ Cartographie de la Délinquance en France")
st.markdown("##### *Analyse officielle des zones à risque pour sécuriser vos chantiers ou informer vos clients.*")
st.divider() # Une belle ligne de séparation

with st.spinner("Analyse des archives de la Police Nationale..."):
    df_brut = recuperer_donnees_securite()

if not df_brut.empty:
    
    # MENU LATÉRAL REVISITÉ
    st.sidebar.title("🎯 Vos Filtres")
    st.sidebar.markdown("Sélectionnez l'infraction et l'année à analyser :")
    
    if 'indicateur' in df_brut.columns and 'Annee' in df_brut.columns and 'nombre' in df_brut.columns:
        liste_delits = sorted(df_brut['indicateur'].dropna().unique())
        delit_choisi = st.sidebar.selectbox("Type d'infraction", liste_delits)
        
        liste_annees = sorted(df_brut['Annee'].dropna().unique(), reverse=True)
        annee_choisie = st.sidebar.selectbox("Année", liste_annees)
        
        # Filtrage
        df_filtre = df_brut[(df_brut['indicateur'] == delit_choisi) & (df_brut['Annee'] == annee_choisie)]
        liste_deps_parfaite = [{'Code_departement': k, 'Nom_Departement': v[0], 'Latitude': v[1], 'Longitude': v[2]} for k, v in DEP_DATA.items()]
        df_complet = pd.DataFrame(liste_deps_parfaite)
        df_complet = pd.merge(df_complet, df_filtre[['Code_departement', 'nombre']], on='Code_departement', how='left')
        df_complet['nombre'] = df_complet['nombre'].fillna(0)
        df_complet = df_complet.sort_values(by='nombre', ascending=False)
        
        # CALCUL DES INDICATEURS CLÉS (KPIs)
        total_france = int(df_complet['nombre'].sum())
        pire_dep = df_complet.iloc[0]['Nom_Departement']
        pire_chiffre = int(df_complet.iloc[0]['nombre'])
        
        # AFFICHAGE DES INDICATEURS CLÉS EN HAUT
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        col_kpi1.metric(label="🚨 Total des faits (France)", value=f"{total_france:,}".replace(',', ' '))
        col_kpi2.metric(label="🏆 Département le plus touché", value=f"{pire_dep}")
        col_kpi3.metric(label="📊 Faits dans ce département", value=f"{pire_chiffre:,}".replace(',', ' '))
        
        st.markdown("<br>", unsafe_allow_html=True) # Petit espace
        
        # CARTOGRAPHIE ET GRAPHIQUE
        col1, col2 = st.columns([2, 1]) 
        
        with col1:
            st.markdown(f"**📍 Carte de France : {delit_choisi} ({annee_choisie})**")
            fig_map = px.scatter_mapbox(
                df_complet, lat="Latitude", lon="Longitude", 
                color="nombre", size="nombre",
                color_continuous_scale=px.colors.sequential.YlOrRd,
                hover_name="Nom_Departement",
                hover_data={"Code_departement": True, "nombre": True, "Latitude": False, "Longitude": False},
                zoom=4.5, mapbox_style="carto-positron"
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        with col2:
            st.markdown("**📈 Top 15 des départements**")
            fig_bar = px.bar(
                df_complet.head(15), 
                x='nombre', y='Nom_Departement', 
                orientation='h',
                color='nombre', color_continuous_scale=px.colors.sequential.YlOrRd
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.divider()
        
        # TABLEAU RANGÉ DANS UN MENU DÉROULANT
        with st.expander("📂 Voir le classement complet des 101 départements"):
            st.markdown("*Cliquez sur l'en-tête d'une colonne pour trier, ou utilisez la loupe pour chercher un département.*")
            tableau_final = df_complet[['Nom_Departement', 'Code_departement', 'nombre']].copy()
            tableau_final.columns = ['Département', 'Code', 'Nombre de délits']
            st.dataframe(tableau_final, use_container_width=True)

    else:
        st.error("Erreur de lecture : Colonnes manquantes dans la base de données de l'État.")
else:
    st.error("Impossible de lire les données. L'API gouvernementale est peut-être hors-ligne.")
