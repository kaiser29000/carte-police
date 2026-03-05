import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuration de la page
st.set_page_config(page_title="Radar Sécurité", page_icon="🛡️", layout="wide")

# Dictionnaire des départements (Nom, Lat, Lon)
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

# Dictionnaire des populations de l'INSEE (~2023)
POP_DEP = {
    '01': 652432, '02': 531345, '03': 335975, '04': 164308, '05': 141220, '06': 1094283, '07': 328278, '08': 270582,
    '09': 153287, '10': 310242, '11': 374070, '12': 279649, '13': 2043110, '14': 694002, '15': 144226, '16': 350867,
    '17': 651358, '18': 302306, '19': 240073, '21': 533220, '22': 600582, '23': 116617, '24': 413223, '25': 543977,
    '26': 516762, '27': 599507, '28': 431277, '29': 915090, '2A': 158507, '2B': 181933, '30': 748437, '31': 1400039,
    '32': 191377, '33': 1623749, '34': 1175623, '35': 1079498, '36': 219316, '37': 610079, '38': 1271166, '39': 259199,
    '40': 413690, '41': 328503, '42': 766659, '43': 227339, '44': 1429272, '45': 680434, '46': 173751, '47': 331123,
    '48': 76520, '49': 818273, '50': 495045, '51': 565292, '52': 171042, '53': 305933, '54': 731004, '55': 184083,
    '56': 759224, '57': 1046873, '58': 204452, '59': 2608346, '60': 829419, '61': 279942, '62': 1461441, '63': 662152,
    '64': 682621, '65': 229567, '66': 479000, '67': 1140057, '68': 767086, '69': 1877046, '70': 235313, '71': 551063,
    '72': 566058, '73': 436434, '74': 823890, '75': 2165423, '76': 1255633, '77': 1421197, '78': 1448207, '79': 374587,
    '80': 569715, '81': 389844, '82': 260669, '83': 1076130, '84': 561941, '85': 685442, '86': 438435, '87': 372359,
    '88': 364499, '89': 335707, '90': 141318, '91': 1301659, '92': 1624357, '93': 1644903, '94': 1407124, '95': 1249674,
    '971': 382704, '972': 364508, '973': 281678, '974': 868846, '976': 299348
}

@st.cache_data(ttl=86400)
def recuperer_donnees_securite():
    api_url = "https://www.data.gouv.fr/api/1/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/"
    res = requests.get(api_url).json()
    csv_url = None
    for resource in res.get('resources', []):
        if 'DEP' in resource.get('title', '').upper() and resource.get('format', '').lower() == 'csv':
            csv_url = resource.get('url')
            break
    if not csv_url: return pd.DataFrame()
    df = pd.read_csv(csv_url, sep=';', low_memory=False)
    if len(df.columns) == 1: df = pd.read_csv(csv_url, sep=',', low_memory=False)
    df.columns = df.columns.str.strip()
    if 'annee' in df.columns: df.rename(columns={'annee': 'Annee'}, inplace=True)
    elif 'année' in df.columns: df.rename(columns={'année': 'Annee'}, inplace=True)
    elif 'Année' in df.columns: df.rename(columns={'Année': 'Annee'}, inplace=True)
    if 'Code_departement' in df.columns:
        df['Code_departement'] = df['Code_departement'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.zfill(2)
    if 'nombre' in df.columns:
        df['nombre'] = df['nombre'].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.')
        df['nombre'] = pd.to_numeric(df['nombre'], errors='coerce') 
    return df

@st.cache_data(ttl=86400)
def recuperer_donnees_auteurs():
    # URL du nouveau jeu de données du SSMSI (Janvier 2026) concernant les caractéristiques des mis en cause
    api_url = "https://www.data.gouv.fr/api/1/datasets/principales-caracteristiques-des-victimes-enregistrees-et-des-mis-en-cause-pour-des-infractions-elucidees-par-la-police-et-la-gendarmerie-nationales"
    try:
        res = requests.get(api_url).json()
        csv_url = None
        for resource in res.get('resources', []):
            # On cherche le fichier CSV officiel
            if resource.get('format', '').lower() == 'csv':
                csv_url = resource.get('url')
                break
        if not csv_url: return pd.DataFrame()
        df = pd.read_csv(csv_url, sep=';', low_memory=False)
        if len(df.columns) == 1: df = pd.read_csv(csv_url, sep=',', low_memory=False)
        return df
    except Exception as e:
        return pd.DataFrame()

# EN-TÊTE PRINCIPAL
st.title("🛡️ Tableau de Bord Sécurité & Délinquance")
st.markdown("##### *Analyse de la criminalité en France pour sécuriser vos projets et informer vos clients.*")
st.divider()

with st.spinner("Analyse des bases de la Police Nationale..."):
    df_brut = recuperer_donnees_securite()

if not df_brut.empty:
    
    # MENU LATÉRAL
    st.sidebar.title("🎯 Vos Filtres")
    
    liste_delits = sorted(df_brut['indicateur'].dropna().unique())
    delit_choisi = st.sidebar.selectbox("Type d'infraction", liste_delits)
    
    liste_annees = sorted(df_brut['Annee'].dropna().unique(), reverse=True)
    annee_choisie = st.sidebar.selectbox("Année à analyser", liste_annees)
    
    st.sidebar.markdown("---")
    taux_actif = st.sidebar.checkbox("⚖️ Afficher le vrai taux de dangerosité", value=True, help="Divise le nombre de délits par la population.")

    # CRÉATION DES 3 ONGLETS !
    tab1, tab2, tab3 = st.tabs(["🌍 Analyse Nationale", "📍 Profil Local", "👤 Profil des Auteurs (NOUVEAU)"])
    
    # --- ONGLET 1 ---
    with tab1:
        df_filtre = df_brut[(df_brut['indicateur'] == delit_choisi) & (df_brut['Annee'] == annee_choisie)]
        liste_deps = [{'Code_departement': k, 'Nom_Departement': v[0], 'Latitude': v[1], 'Longitude': v[2]} for k, v in DEP_DATA.items()]
        df_complet = pd.DataFrame(liste_deps)
        df_complet = pd.merge(df_complet, df_filtre[['Code_departement', 'nombre']], on='Code_departement', how='left')
        df_complet['nombre'] = df_complet['nombre'].fillna(0)
        
        if taux_actif:
            df_complet['Valeur_Affichee'] = df_complet.apply(lambda row: round((row['nombre'] / POP_DEP.get(row['Code_departement'], 1)) * 1000, 2), axis=1)
            unite = "Faits pour 1000 hab."
        else:
            df_complet['Valeur_Affichee'] = df_complet['nombre']
            unite = "Nombre total de faits"
            
        df_complet = df_complet.sort_values(by='Valeur_Affichee', ascending=False)
        
        col1, col2 = st.columns([2, 1]) 
        with col1:
            st.markdown(f"**📍 Carte de France : {delit_choisi}**")
            fig_map = px.scatter_mapbox(
                df_complet, lat="Latitude", lon="Longitude", color="Valeur_Affichee", size="Valeur_Affichee",
                color_continuous_scale=px.colors.sequential.YlOrRd, hover_name="Nom_Departement",
                zoom=4.5, mapbox_style="carto-positron"
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        with col2:
            st.markdown("**📈 Top 15 des départements**")
            fig_bar = px.bar(
                df_complet.head(15), x='Valeur_Affichee', y='Nom_Departement', orientation='h',
                color='Valeur_Affichee', color_continuous_scale=px.colors.sequential.YlOrRd
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("---")
        st.markdown(f"**📉 Évolution de la délinquance en France : {delit_choisi} (2016 à aujourd'hui)**")
        df_tendance = df_brut[df_brut['indicateur'] == delit_choisi].groupby('Annee')['nombre'].sum().reset_index()
        fig_line = px.line(df_tendance, x="Annee", y="nombre", markers=True, color_discrete_sequence=['#ff4b4b'])
        fig_line.update_layout(xaxis_title="Année", yaxis_title="Nombre total de délits (France)", margin={"r":0,"t":10,"l":0,"b":0})
        st.plotly_chart(fig_line, use_container_width=True)

        with st.expander("📂 Voir le classement complet des 101 départements"):
            tableau_final = df_complet[['Nom_Departement', 'Code_departement', 'Valeur_Affichee']].copy()
            tableau_final.columns = ['Département', 'Code', unite]
            st.dataframe(
                tableau_final, hide_index=True, use_container_width=True, height=320,
                column_config={"Département": st.column_config.TextColumn("Département 📍"),
                               "Code": st.column_config.TextColumn("Code 🔢"),
                               unite: st.column_config.ProgressColumn(unite, format="%.2f", min_value=0, max_value=float(tableau_final[unite].max()))}
            )

    # --- ONGLET 2 ---
    with tab2:
        st.markdown("### 🔍 Profil de Délinquance Départemental")
        liste_noms_deps = [f"{k} - {v[0]}" for k, v in DEP_DATA.items()]
        dep_choisi = st.selectbox("Choisissez le département de votre client/chantier :", liste_noms_deps, index=liste_noms_deps.index("75 - Paris"))
        code_dep_choisi = dep_choisi.split(" - ")[0]
        nom_dep_choisi = dep_choisi.split(" - ")[1]
        
        st.markdown(f"#### Rapport de sécurité pour : **{nom_dep_choisi} ({code_dep_choisi})** en {annee_choisie}")
        df_dep = df_brut[(df_brut['Code_departement'] == code_dep_choisi) & (df_brut['Annee'] == annee_choisie)]
        
        if not df_dep.empty:
            col_pie, col_empty = st.columns([2, 1])
            with col_pie:
                st.markdown("**Quels sont les délits les plus fréquents ici ?**")
                df_dep_top = df_dep.sort_values(by='nombre', ascending=False).head(10)
                fig_pie = px.pie(df_dep_top, values='nombre', names='indicateur', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                fig_pie.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"Aucune donnée enregistrée pour le {code_dep_choisi} en {annee_choisie}.")

    # --- ONGLET 3 : DEMOGRAPHIE ---
    with tab3:
        st.markdown("### 👤 Qui sont les auteurs présumés ? (Données Nationales)")
        st.info("💡 Ces données proviennent du tout nouveau fichier du SSMSI recensant les caractéristiques des personnes mises en cause.")
        
        with st.spinner("Téléchargement de la base de données démographique depuis data.gouv.fr..."):
            df_auteurs = recuperer_donnees_auteurs()
            
        if not df_auteurs.empty:
            st.success("Fichier démographique téléchargé avec succès !")
            st.markdown("Pour l'instant, regardons ensemble les données brutes fournies par la police. **Cherchez la colonne qui parle de la nationalité ou de l'âge dans ce tableau :**")
            
            # On affiche les 5 premières lignes pour que le développeur (vous) puisse inspecter les colonnes
            st.dataframe(df_auteurs.head(10), use_container_width=True)
            
            st.markdown("---")
            st.markdown("🛠️ **Message pour vous (le développeur) :** Regardez attentivement les en-têtes des colonnes dans le tableau noir ci-dessus. Dites-moi exactement comment s'appellent les colonnes qui concernent la **Nationalité**, le **Sexe**, ou le **nombre de faits**, et je vous coderai immédiatement les superbes graphiques en anneau ! (Exemple: *'nationalite'*, *'tranche_age'*, *'victimes_ou_mis_en_cause'*...).")
        else:
            st.warning("⚠️ Impossible de télécharger le fichier. L'API est peut-être temporairement indisponible.")

else:
    st.error("Impossible de lire les données de la Police.")
