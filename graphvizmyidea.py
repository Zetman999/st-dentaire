import streamlit as st
import graphviz
#from MembreFamille import MembreFamille
import base64
import numpy as np
from csv import reader
import pandas as pd
from io import BytesIO
import openpyxl as xl
import xlsxwriter

from Famille import Famille

class MembreFamille: #Do default values
    def __init__(self, id, nom, maladie, generation, conjoint_id, parents_id, enfants, colour, colourstyle, sexe, image):
        self.id = id
        self.nom = nom
        self.maladie = maladie
        self.generation = generation #0 est la plus vieille
        self.conjoint_id = conjoint_id
        self.parents_id = parents_id #liste ou tuple c'est mieux
        self.enfants = enfants
        self.colour = colour
        self.colourstyle = colourstyle
        self.sexe = sexe
        self.image = image

file = 'data_copy.csv'
nombre_attribut_objet_MembreFamille = 11

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
#df_xlsx = to_excel(df)
# st.download_button(label='📥 Download Current Result',
#                                 data=df_xlsx ,
#                                 file_name= 'df_test.xlsx')

def traitement_donnees_listes(value): #parents_id et enfants
    if value == 'None':
        value = None
    if value != None:
        if isinstance(value, int):
            return [value]
        else:
            L = []
            listRes = list(value.split(";"))
            for item in listRes:
                L.append(int(item))
            return L
    else:
        return None

def int_les_nombres_donnees_listes(value):
    if value != None:
        return int(value)
    else:
        return None

#print(traitement_donnees_listes("1;2;3"))

#id, nom, maladie, generation, conjoint_id, parents_id, enfants, colour, colourstyle, sexe, image
#parents_id doit être ordonné
#de préférence enfants aussi mais je crois pas que ce soit nécessaire (àvérifmaisblc)
#patient0 = MembreFamille(0, 'GrandUncle','Gingivite', 0, None, None, None)
# patient1 = MembreFamille(1, 'GP','Gingivite', 0, 2, None, [3,5,7], None, None, 'Homme', None)
# patient2 = MembreFamille(2, 'GrandMother','Parodontite', 0, 1, None, [3,5,7], None, None, 'Femme', None)
# patient3 = MembreFamille(3, 'Charlie le pd',None, 1, 4, [1,2], [13,15,16], None, None, 'Homme', None)
# patient4 = MembreFamille(4, 'Mother','Santé Gingivale', 1, 3, None, [13,15,16], None, None, 'Femme', None)
# patient5 = MembreFamille(5, 'Uncle','Suce picion', 1, 6, [1,2], None, None, None, 'Homme', None)
# patient6 = MembreFamille(6, 'His Wife','Parodontite', 1, 5, None, None, None, None, 'Femme', None)
# patient7 = MembreFamille(7, 'WTF','Parodontite', 1, 8, [1,2], [9,10,11,12], None, None, 'Homme', None)
# patient8 = MembreFamille(8, 'Her Husband','Parodontite', 1, 7, None, [9,10,11,12], None, None, 'Femme', None)
# patient9 = MembreFamille(9, 'Hriu','Parodontite', 2, None, [7,8], None, None, None, 'Homme', None)
# patient10 = MembreFamille(10, 'Eric','Parodontite', 2, None, [7,8], None, None, None, 'Homme', None)
# patient11 = MembreFamille(11, 'UNgama','Parodontite', 2, None, [7,8], None, None, None, 'Homme', None)
# patient12 = MembreFamille(12, 'Toma','Parodontite', 2, None, [7,8], None, None, None, 'Homme', None)
# patient13 = MembreFamille(13, 'Me','Parodontite', 2, 14, [3,4], [17], None, None, 'Homme', None)
# patient14 = MembreFamille(14, 'My Wife','Parodontite', 2, 13, None, [17], None, None, 'Femme', None)
# patient15 = MembreFamille(15, 'Brother','Parodontite', 2, None, [3,4], None, None, None, 'Homme', None)
# patient16 = MembreFamille(16, 'Sister','Parodontite', 2, None, [3,4], None, None, None, 'Femme', None)
# patient17 = MembreFamille(17, 'My Son','Parodontite', 3, None, [13,14], None, None, None, 'Homme', None)

# liste_patients_dune_famille = [patient1, patient2, patient3, patient4, patient5, patient6, patient7, patient8, patient9, patient10, patient11, patient12, patient13, patient14, patient15, patient16, patient17]
# #print(liste_patients_dune_famille[0].conjoint_id)
#st.write(df)

st.write("""  
# Projet dentaire

Fiches famille et données.

""")

file = st.file_uploader("Veuillez upload un fichier .csv (UTF-8)")#, type="csv", encoding='ansi')

if file is None:
    if 'donnees' in st.session_state:
        st.session_state.pop('donnees')
    st.text("Exemple:")
    st.code("""id,nom,maladie,generation,conjoint_id,parents_id,enfants,colour,colourstyle,sexe,image
    1,Papy,Gingivite,0,2,None,3;5;7,None,None,Homme,None
    2,Mamie,Santé Gingivale,0,1,None,3;5;7,None,None,Femme,None
    3,Charlie,None,1,4,1;2,13;15;16,None,None,Homme,None
    4,Mother,Santé Gingivale,1,3,None,13;15;16,None,None,Femme,None
    5,Raphaël,Suspicion,1,6,1;2,None,None,None,Homme,None
    6,His Wife,Parodontite,1,5,None,None,None,None,Femme,None
    7,Aunt,Parodontite,1,8,1;2,9;10;11;12,None,None,Femme,None
    8,Her Husband,Parodontite,1,7,None,9;10;11;12,None,None,Homme,None
    9,Pierrick,Parodontite,2,None,7;8,None,None,None,Homme,None
    10,Eric,Parodontite,2,None,7;8,None,None,None,Homme,None
    11,Adam,Parodontite,2,None,7;8,None,None,None,Homme,None
    12,Toma,Parodontite,2,None,7;8,None,None,None,Homme,None
    13,Me,Parodontite,2,14,3;4,17;18;19,None,None,Homme,None
    14,My Wife,Parodontite,2,13,None,17;18;19,None,None,Femme,None
    15,Brother,Parodontite,2,None,3;4,None,None,None,Homme,None
    16,Sister,Parodontite,2,None,3;4,None,None,None,Femme,None
    17,My Son,Parodontite,3,None,13;14,None,None,None,Homme,None
    18,Jean-Christophe,Santé Gingivale,3,None,13;14,None,None,None,None,None
    19,Gwendal,Santé Gingivale,3,None,13;14,None,None,None,None,None
    """)
if file is not None:
    df = pd.read_csv(file, low_memory=False, encoding='ansi')
    file.seek(0)
    if 'donnees' not in st.session_state:
        st.session_state['donnees'] = df
    #df = donnees.copy()
    #file.seek(0)
    #st.dataframe(donnees)


    #df = pd.read_csv(file, sep=',')
    liste_patients_dune_famille = dict()
    #ICI EST l'IMPORTATION DES DONNEES SOUS FORME D'OBJETS
    #id, nom, maladie, generation, conjoint_id, parents_id, enfants, colour, colourstyle, sexe, image
    for index, row in st.session_state['donnees'].iterrows():
        if st.session_state['donnees'].loc[index,"id"] == 'None' or st.session_state['donnees'].loc[index,"id"] == '':
            st.session_state['donnees'].loc[index,"id"] = None
        if st.session_state['donnees'].loc[index,"nom"] == 'None' or st.session_state['donnees'].loc[index,"nom"] == '':
            st.session_state['donnees'].loc[index,"nom"] = None
        if st.session_state['donnees'].loc[index,"maladie"] == 'None' or st.session_state['donnees'].loc[index,"maladie"] == '':
            st.session_state['donnees'].loc[index,"maladie"] = None
        if st.session_state['donnees'].loc[index,"generation"] == 'None' or st.session_state['donnees'].loc[index,"generation"] == '':
            st.session_state['donnees'].loc[index,"generation"] = None
        if st.session_state['donnees'].loc[index,"conjoint_id"] == 'None' or st.session_state['donnees'].loc[index,"conjoint_id"] == '':
            st.session_state['donnees'].loc[index,"conjoint_id"] = None
        if st.session_state['donnees'].loc[index,"parents_id"] == 'None' or st.session_state['donnees'].loc[index,"parents_id"] == '':
            st.session_state['donnees'].loc[index,"parents_id"] = None
        if st.session_state['donnees'].loc[index,"enfants"] == 'None' or st.session_state['donnees'].loc[index,"enfants"] == '':
            st.session_state['donnees'].loc[index,"enfants"] = None
        if st.session_state['donnees'].loc[index,"colour"] == 'None' or st.session_state['donnees'].loc[index,"colour"] == '':
            st.session_state['donnees'].loc[index,"colour"] = None
        if st.session_state['donnees'].loc[index,"colourstyle"] == 'None' or st.session_state['donnees'].loc[index,"colourstyle"] == '':
            st.session_state['donnees'].loc[index,"colourstyle"] = None
        if st.session_state['donnees'].loc[index,"sexe"] == 'None' or st.session_state['donnees'].loc[index,"sexe"] == '':
            st.session_state['donnees'].loc[index,"sexe"] = None
        if st.session_state['donnees'].loc[index,"image"] == 'None' or st.session_state['donnees'].loc[index,"image"] == '':
            st.session_state['donnees'].loc[index,"image"] = None
        if st.session_state['donnees'].loc[index,"image"] == None:
            st.session_state['donnees'].loc[index,"image"] = ""
        liste_patients_dune_famille[int_les_nombres_donnees_listes(st.session_state['donnees'].loc[index,"id"])] = MembreFamille(int_les_nombres_donnees_listes(st.session_state['donnees'].loc[index,"id"]), st.session_state['donnees'].loc[index,"nom"], st.session_state['donnees'].loc[index,"maladie"],
        int_les_nombres_donnees_listes(st.session_state['donnees'].loc[index,"generation"]), int_les_nombres_donnees_listes(st.session_state['donnees'].loc[index,"conjoint_id"]), traitement_donnees_listes(st.session_state['donnees'].loc[index,"parents_id"]),
        traitement_donnees_listes(st.session_state['donnees'].loc[index,"enfants"]), st.session_state['donnees'].loc[index,"colour"], st.session_state['donnees'].loc[index,"colourstyle"], st.session_state['donnees'].loc[index,"sexe"], st.session_state['donnees'].loc[index,"image"])
    #df = donnees.copy()
        # liste_patients_dune_famille.append(MembreFamille(int_les_nombres_donnees_listes(donnees.loc[index,"id"]), donnees.loc[index,"nom"], donnees.loc[index,"maladie"],
        # int_les_nombres_donnees_listes(donnees.loc[index,"generation"]), int_les_nombres_donnees_listes(donnees.loc[index,"conjoint_id"]), traitement_donnees_listes(donnees.loc[index,"parents_id"]),
        # traitement_donnees_listes(donnees.loc[index,"enfants"]), donnees.loc[index,"colour"], donnees.loc[index,"colourstyle"], donnees.loc[index,"sexe"], donnees.loc[index,"image"]))

    #FONCTION POUR TROUVER COUPLES (UTILE DANS les listes de parents possibles)////////////////////
    def trouver_couples(liste_patients_dune_famille):
        
        liste_couples = []
        liste_ajout_par_round = []
        for key in liste_patients_dune_famille.keys():
            if liste_patients_dune_famille[key].conjoint_id != '' and liste_patients_dune_famille[key].conjoint_id != 'None' and liste_patients_dune_famille[key].conjoint_id != None:
                liste_ajout_par_round = [liste_patients_dune_famille[key].id, liste_patients_dune_famille[key].conjoint_id]
                liste_ajout_par_round.sort()
                liste_couples.append(liste_ajout_par_round)
        return liste_couples #liste de listes de couples (les id couples sont ordonnés)


    #FONCTIONS POUR AJOUTER UN INDIVIDU /////////////////////////////////////////////////////////////////////////////////////////////////
    def update_enfant_parents(id_enfant, id_parents, liste_patients_dune_famille): #update l'objet MembreFamille du parent ainsi que les données dans le csv
        
        #print("ID PARENTS: ", id_parents)
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        if id_parents == None:
            return 0
        for i in range(len(id_parents)):
            if liste_patients_dune_famille[id_parents[i]].enfants == None:
                liste_patients_dune_famille[id_parents[i]].enfants = []
            if id_enfant not in liste_patients_dune_famille[id_parents[i]].enfants:
                #print("HERE: ", id_parents[i])
                liste_patients_dune_famille[id_parents[i]].enfants.append(id_enfant)
                #print("HERE 2: ", liste_patients_dune_famille[id_parents[i]].enfants)
                liste_patients_dune_famille[id_parents[i]].enfants.sort()
                valeur_a_mettre_dans_le_csv = ''
                for j in range(len(liste_patients_dune_famille[id_parents[i]].enfants)):
                    valeur_a_mettre_dans_le_csv = valeur_a_mettre_dans_le_csv + str(liste_patients_dune_famille[id_parents[i]].enfants[j])
                    if j != len(liste_patients_dune_famille[id_parents[i]].enfants)-1:
                        valeur_a_mettre_dans_le_csv = valeur_a_mettre_dans_le_csv + ';'
                #print("HERE 3: ", valeur_a_mettre_dans_le_csv)
                for index, row in st.session_state['donnees'].iterrows():
                    if st.session_state['donnees'].loc[index, "id"] == id_parents[i]:
                        st.session_state['donnees'].loc[index, "enfants"] = valeur_a_mettre_dans_le_csv
        #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')

    def update_mariage(id_individu, id_conjoint, liste_patients_dune_famille): #update l'objet MembreFamille du conjoint ainsi que les données dans le csv
        
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        #L'objet
        liste_patients_dune_famille[id_conjoint].conjoint_id = id_individu
        for index, row in st.session_state['donnees'].iterrows():
            if st.session_state['donnees'].loc[index, "id"] == id_conjoint:
                st.session_state['donnees'].loc[index, "conjoint_id"] = id_individu
        #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    #FONCTIONS POUR SUPPRIMER UN INDIVIDU /////////////////////////////////////////////////////////////////////////////////////////////////       
    def supprimer_enfant_parents(id_enfant, id_parents, liste_patients_dune_famille): #update l'objet MembreFamille du parent ainsi que les données dans le csv (SUPPRESSION ENFANT DU PARENT)
        
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        if id_parents == None:
            return 0
        for i in range(len(id_parents)):
            valeur_a_mettre_dans_le_csv = ''
            if len(liste_patients_dune_famille[id_parents[i]].enfants) == 1:
                liste_patients_dune_famille[id_parents[i]].enfants.remove(id_enfant)
                valeur_a_mettre_dans_le_csv = 'None'
            else:
                liste_patients_dune_famille[id_parents[i]].enfants.remove(id_enfant)
                for j in range(len(liste_patients_dune_famille[id_parents[i]].enfants)):
                    valeur_a_mettre_dans_le_csv = valeur_a_mettre_dans_le_csv + str(liste_patients_dune_famille[id_parents[i]].enfants[j])
                    if j != len(liste_patients_dune_famille[id_parents[i]].enfants)-1:
                        valeur_a_mettre_dans_le_csv = valeur_a_mettre_dans_le_csv + ';'
            for index, row in st.session_state['donnees'].iterrows():
                if st.session_state['donnees'].loc[index, "id"] == id_parents[i]:
                    st.session_state['donnees'].loc[index, "enfants"] = valeur_a_mettre_dans_le_csv
        #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')

    def supprimer_mariage(id_conjoint, liste_patients_dune_famille): #update l'objet MembreFamille du conjoint ainsi que les données dans le csv (SUPPRESSION CONJOINT DU CONJOINT)
        
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        #L'objet
        liste_patients_dune_famille[id_conjoint].conjoint_id = None
        for index, row in st.session_state['donnees'].iterrows():
            if st.session_state['donnees'].loc[index, "id"] == id_conjoint:
                st.session_state['donnees'].loc[index, "conjoint_id"] = 'None'
        #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    #FONCTION POUR SET LA GENERATION AUTOMATIQUEMENT /////////////////////////////////////////////////////////////////////////////////////////////////  
    def autogen(parents_id, conjoint_id, liste_patients_dune_famille): #retourne la génération | parents_id liste, conjoint_id str ('1' ou '' par exemple), liste_patients dict d'objets MembreFamille
        
        if conjoint_id != None and conjoint_id != '' and conjoint_id != 'None':
            conjoint_id = int(conjoint_id)
            return liste_patients_dune_famille[conjoint_id].generation
        else:
            if parents_id != None and parents_id != 'None':
                return liste_patients_dune_famille[parents_id[0]].generation - 1
            else:
                return False

    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def cluster_builder(liste_patients_dune_famille): #pour la refonte 3 du code un jour peut-être
        a = 2

    def colour_code(liste_patients_dune_famille): #colour coder
        
        for patient in liste_patients_dune_famille.values():
            patient.colourstyle = "radial" #radial or filled, u can also choose a gradient angle
            if patient.maladie == None:
                patient.colour = "#757575" #grey #can also use colorlist for a gradient
            elif patient.maladie == 'Parodontite':
                patient.colour = "#ff0005:#d40042" #red
            elif patient.maladie == 'Gingivite':
                patient.colour = "#ff9005:#fe205f" #"#e57000" #orange
            elif patient.maladie == 'Santé Gingivale':
                patient.colour = "#1ea5ff:#4d20ff" #blue
            else:
                patient.colour = "#f0f000:#ffcc07" #yellow



    def image_code(liste_patients_dune_famille): #like colour coder but with bg images
        
        for patient in liste_patients_dune_famille.values():
            #patient.colourstyle = "radial" #radial or filled, u can also choose a gradient angle
            if patient.sexe == 'Femme':
                if patient.maladie == None:
                    patient.image = 'PAS_DE_DONNEE_FEMME.png' #grey #can also use colorlist for a gradient
                elif patient.maladie == 'Parodontite':
                    patient.image = 'PARODONDITE_FEMME.png' #red
                elif patient.maladie == 'Gingivite':
                    patient.image = 'GINGIVITE_FEMME.png' #"#e57000" #orange
                elif patient.maladie == 'Santé Gingivale':
                    patient.image = 'SANTE_FEMME.png' #blue
                else:
                    patient.image = 'SUSPICION_FEMME.png' #yellow
            else: #Homme
                if patient.maladie == None:
                    patient.image = 'PAS_DE_DONNEE_HOMME.png' #grey #can also use colorlist for a gradient
                elif patient.maladie == 'Parodontite':
                    patient.image = 'PARODONTITE_HOMME.png' #red
                elif patient.maladie == 'Gingivite':
                    patient.image = 'GINGIVITE_HOMME.png' #"#e57000" #orange
                elif patient.maladie == 'Santé Gingivale':
                    patient.image = 'SANTE_HOMME.png' #blue
                else:
                    patient.image = 'SUSPICION_HOMME.png' #yellow


    def max_gen(liste_patients_dune_famille): #Compte le nombre de générations d'une famille (commence à 0 inclus)
        
        maximum_gen = 0
        #for i in range(len(liste_patients_dune_famille)):
        for key in liste_patients_dune_famille.keys():
            if liste_patients_dune_famille[key].generation > maximum_gen:
                maximum_gen = liste_patients_dune_famille[key].generation
        return maximum_gen

    #print(max_gen(liste_patients_dune_famille))

    def nom_depuis_id(id): #pour objet MembreFamille uniquement
        
        for member in liste_patients_dune_famille.values():
            if member.id == id:
                return member.nom

    def colour_from_id(id):
        
        for member in liste_patients_dune_famille.values():
            if member.id == id:
                return member.colour

    def liste_id_parents_depuis_id_enfant(id_enfant):#retourne la liste d'id des parents depuis l'id d'un de leurs enfants
        
        for member in liste_patients_dune_famille.values():
            if member.id == id_enfant:
                return member.parents_id


    def liste_enfants_depuis_id_enfant(id_enfant):#C'est à dire je veux la liste des identifiants de la fratrie, donc la personne elle-même et tous ses frères et soeurs
        
        for member in liste_patients_dune_famille.values():
            if member.enfants != None and id_enfant in member.enfants:
                return member.enfants

    def image_conjoint(id_conjoint): #retourne l'image du conjoint à partir de son id
        
        for member in liste_patients_dune_famille.values():
            if member.id == id_conjoint:
                return member.image

    def colourstyle_conjoint(id_conjoint): #retourne la colourstyle du conjoint à partir de son id
        
        for member in liste_patients_dune_famille.values():
            if member.id == id_conjoint:
                return member.colourstyle

    def supprimer_personne(): #Page 1
        
        st.header("Supprimer un individu")
        button_label = 'Supprimer'
        with st.form(key='form2', clear_on_submit=True):
            #df = pd.read_csv(file, sep=',')
            #file.seek(0)
            #add_id = st.number_input(label=f"{id_label}", min_value=0)
            id_dictionnaire = {}
            for index, row in st.session_state['donnees'].iterrows():
                id = st.session_state['donnees'].loc[index, "id"]
                name = st.session_state['donnees'].loc[index, "nom"]
                id_dictionnaire[name+' (ID: '+str(id)+' )'] = id
                #st.write(row[0], row[1], row[2])
            idbox = st.selectbox("Nom / Identifiant",id_dictionnaire.keys(),key="ajouter_conjoint")
            add_id = id_dictionnaire[idbox]
            button_press = st.form_submit_button(label=f"{button_label}")
        if button_press:
            #df = pd.read_csv(file, sep=',')
            #file.seek(0)
            st.session_state['donnees'] = st.session_state['donnees'][st.session_state['donnees'].id != add_id]
            #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')
            if liste_patients_dune_famille[add_id].parents_id != None and liste_patients_dune_famille[add_id].parents_id != 'None' and liste_patients_dune_famille[add_id].parents_id != '':
                supprimer_enfant_parents(add_id, liste_patients_dune_famille[add_id].parents_id, liste_patients_dune_famille)
            if liste_patients_dune_famille[add_id].conjoint_id != None and liste_patients_dune_famille[add_id].conjoint_id != 'None' and liste_patients_dune_famille[add_id].conjoint_id != '':
                supprimer_mariage(liste_patients_dune_famille[add_id].conjoint_id, liste_patients_dune_famille)
            liste_patients_dune_famille.pop(add_id) #Suppression de l'entry dans le dictionnaire. L'objet MembreFamille n'existe plus
            st.balloons()

    def ajouter_personne():
        
        #id;nom;maladie;generation;conjoint_id;parents_id;enfants;colour;colourstyle
        name_label = 'Nom'
        #maladie_label = 'Maladie'
        generation_label = 'Génération (UNIQUEMENT si aucun parents ni conjoint)'
        conjoint_id_label = 'Identifiant conjoint'
        parents_id_label = 'ID parents' #à changer pour array de noms dans la même famille? oui, dans la génération juste au-dessus |faiblesse si meme gen 2 couples mariés mêmes noms
        enfants_label = 'ID enfants'
        button_label = 'Ajouter'
        st.header("Ajouter un individu")
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        df = st.session_state['donnees']
        add_id = df['id'].max() + 1
        with st.form(key='form3', clear_on_submit=True):
        #form = st.form(key='form3', clear_on_submit=True)
            add_name = st.text_input(label=f"{name_label}", value='Tapez le nom...')

            #CONJOINT//////////////
            #add_conjoint_id = st.text_input(label=f"{conjoint_id_label}")
            conjoint_dictionnaire = {"Aucun":'None'}
            for index, row in st.session_state['donnees'].iterrows():
                id = st.session_state['donnees'].loc[index, "id"]
                name = st.session_state['donnees'].loc[index, "nom"]
                conjoint_dictionnaire[name+' (ID: '+str(id)+' )'] = id
                #st.write(row[0], row[1], row[2])
            conjointbox = st.selectbox("Conjoint",conjoint_dictionnaire.keys(),key="ajouter_conjoint")
            add_conjoint_id = conjoint_dictionnaire[conjointbox]
            #add_maladie = st.text_input(label=f"{maladie_label}", value='Parodontite ou autre')
            #MALADIE///////////////
            maladies_dictionnaire = {"Pas de données": None,
            "Gingivite":'Gingivite',
            "Parodontite":'Parodontite',
            "Santé Gingivale": 'Santé Gingivale',
            "Suspicion de parodontite":'Suspicion'
            }
            maladiebox = st.selectbox("Maladie",maladies_dictionnaire.keys(),key="ajouter_maladie")
            #pages[selected_page]()
            add_maladie = maladies_dictionnaire[maladiebox]

            #PARENTS////////////////
            parents_possibles = trouver_couples(liste_patients_dune_famille)

            parents_dictionnaire = {"Aucun/Inconnus/Trop anciens":'None'}
            for couple in parents_possibles:
                nom1 = nom_depuis_id(couple[0])
                nom2 = nom_depuis_id(couple[-1])
                parents_dictionnaire[nom1+' (ID: '+str(couple[0])+'), '+nom2+' (ID: '+str(couple[1])+')'] = str(couple[0])+';'+str(couple[-1])

            parentsbox = st.selectbox("Parents",parents_dictionnaire.keys(),key="ajouter_parents")
            #pages[selected_page]()
            add_parents_id = parents_dictionnaire[parentsbox]



            #add_parents_id = st.text_input(label=f"{parents_id_label}", value='Exemple: 1;2')
            #if add_parents_id == '':
            #    add_parents_id = None
            #df = pd.read_csv(file, sep=',')
            #if autogen(traitement_donnees_listes(add_parents_id), add_conjoint_id, liste_patients_dune_famille) == False:
            add_generation = st.number_input(label=f'{generation_label}',min_value=0)

            button_press = st.form_submit_button(label=f"{button_label}")

        if button_press:
            if autogen(traitement_donnees_listes(add_parents_id), add_conjoint_id, liste_patients_dune_famille) != False:
                add_generation = autogen(traitement_donnees_listes(add_parents_id), add_conjoint_id, liste_patients_dune_famille)
            if add_conjoint_id != '' and add_conjoint_id != 'None' and add_conjoint_id != None:
                new_data = {'id':add_id,'nom':add_name,'generation': int(add_generation),'conjoint_id':int(add_conjoint_id),'maladie':str(add_maladie), 'parents_id':add_parents_id}
                liste_patients_dune_famille[add_id] = MembreFamille(int_les_nombres_donnees_listes(add_id), add_name, add_maladie, int_les_nombres_donnees_listes(add_generation), int_les_nombres_donnees_listes(add_conjoint_id), traitement_donnees_listes(add_parents_id), None, None, None, None, None)
            else:
                new_data = {'id':add_id,'nom':add_name,'generation': int(add_generation),'conjoint_id':None,'maladie':str(add_maladie), 'parents_id':add_parents_id}
                liste_patients_dune_famille[add_id] = MembreFamille(int_les_nombres_donnees_listes(add_id), add_name, add_maladie, int_les_nombres_donnees_listes(add_generation), None, traitement_donnees_listes(add_parents_id), None, None, None, None, None)
            #MembreFamille(int_les_nombres_donnees_listes(donnees.loc[index,"id"]), donnees.loc[index,"nom"], donnees.loc[index,"maladie"],
            #int_les_nombres_donnees_listes(donnees.loc[index,"generation"]), int_les_nombres_donnees_listes(donnees.loc[index,"conjoint_id"]), traitement_donnees_listes(donnees.loc[index,"parents_id"]),
            #traitement_donnees_listes(donnees.loc[index,"enfants"]), donnees.loc[index,"colour"], donnees.loc[index,"colourstyle"], donnees.loc[index,"sexe"], donnees.loc[index,"image"])
            st.session_state['donnees'] = st.session_state['donnees'].append(new_data, ignore_index=True)
            st.session_state['donnees'].replace("", 'None', inplace=True)
            st.session_state['donnees'].replace('<NA>','None')
            st.session_state['donnees'].fillna('None', inplace=True)
            #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')
            if add_parents_id != None and add_parents_id != 'None' and add_parents_id != '':
                update_enfant_parents(add_id, traitement_donnees_listes(add_parents_id), liste_patients_dune_famille)
            if add_conjoint_id != None and add_conjoint_id != 'None' and add_conjoint_id != '':
                update_mariage(add_id, int(add_conjoint_id), liste_patients_dune_famille)
            st.balloons()
        else:
            st.write("Veuillez remplir/modifier les données.")

    def modifier_personne():
        
        st.header("Editer un individu")
        #df = pd.read_csv(file, sep=',')
        #file.seek(0)
        pages = {}
        for index, row in st.session_state['donnees'].iterrows():
            id = st.session_state['donnees'].loc[index, "id"]
            name = st.session_state['donnees'].loc[index, "nom"]
            pages[name+' (ID: '+str(id)+' )'] = modifier_personne_choix_fait
            #st.write(row[0], row[1], row[2])
        selected_page = st.selectbox(
            "Choose page",
            pages.keys()
        )
        a = [int(s) for s in selected_page.split() if s.isdigit()]
        #st.write("HEEEEERE: ", a[0])
        pages[selected_page](a[-1])

    def modifier_personne_choix_fait(id):
        
        #st.write("Hello "+str(id)+" !")
        #df = pd.read_csv(file, sep=',')
        for index, row in st.session_state['donnees'].iterrows():
            if st.session_state['donnees'].loc[index,"id"] == id:
                break
        #st.write(st.session_state['donnees'].loc[index, "id"])
        #st.write(st.session_state['donnees'].loc[index, "nom"])
        #st.write(st.session_state['donnees'].loc[index, "maladie"])
        #st.write(st.session_state['donnees'].loc[index, "generation"])
        #st.write(st.session_state['donnees'].loc[index, "conjoint_id"])
        #id_label = 'ID'
        name_label = 'Nom'
        #maladie_label = 'Maladie'
        generation_label = 'Génération (UNIQUEMENT si aucun parents ni conjoint)'
        #conjoint_id_label = 'Identifiant conjoint'
        parents_id_label = 'ID parents' #à changer pour array de noms dans la même famille? oui, dans la génération juste au-dessus |faiblesse si meme gen 2 couples mariés mêmes noms
        button_label = 'Modifier'
        with st.form(key='form4', clear_on_submit=False):
            #add_id = form.number_input(label=f'{id_label}',min_value=0, value=st.session_state['donnees'].loc[index, "id"])
            add_name = st.text_input(label=f"{name_label}", value=st.session_state['donnees'].loc[index, "nom"])
            #add_maladie = form.text_input(label=f"{maladie_label}", value=st.session_state['donnees'].loc[index, "maladie"])
            #MALADIE///////////////
            maladies_dictionnaire = {"Pas de données": None,
            "Gingivite":'Gingivite',
            "Parodontite":'Parodontite',
            "Santé Gingivale": 'Santé Gingivale',
            "Suspicion de parodontite":'Suspicion'
            }
            maladiebox = st.selectbox("Maladie",maladies_dictionnaire.keys(),key="ajouter_maladie")
            #pages[selected_page]()
            add_maladie = maladies_dictionnaire[maladiebox]

            #CONJOINT//////////////
            #add_conjoint_id = st.text_input(label=f"{conjoint_id_label}")
            conjoint_dictionnaire = {"Aucun":'None'}
            #df = st.session_state['donnees']
            df_conjoint = st.session_state['donnees'][st.session_state['donnees'].id != id]
            for index, row in df_conjoint.iterrows():
                id = df_conjoint.loc[index, "id"]
                name = df_conjoint.loc[index, "nom"]
                conjoint_dictionnaire[name+' (ID: '+str(id)+' )'] = id
                #st.write(row[0], row[1], row[2])
            conjointbox = st.selectbox("Conjoint",conjoint_dictionnaire.keys(),key="ajouter_conjoint")
            add_conjoint_id = conjoint_dictionnaire[conjointbox]
            #add_conjoint_id = st.text_input(label=f"{conjoint_id_label}", value=st.session_state['donnees'].loc[index, "conjoint_id"])

            #PARENTS////////////////
            parents_possibles = trouver_couples(liste_patients_dune_famille)

            parents_dictionnaire = {"Aucun/Inconnus/Trop anciens":'None'}
            for couple in parents_possibles:
                nom1 = nom_depuis_id(couple[0])
                nom2 = nom_depuis_id(couple[-1])
                parents_dictionnaire[nom1+' (ID: '+str(couple[0])+'), '+nom2+' (ID: '+str(couple[1])+')'] = str(couple[0])+';'+str(couple[-1]) #doit être = '14;15' | IL Y A FORCEMENT IL DOIT Y AVOIR 2 PARENTS

            parentsbox = st.selectbox("Parents",parents_dictionnaire.keys(),key="ajouter_parents")
            #pages[selected_page]()
            add_parents_id = parents_dictionnaire[parentsbox]
            #add_parents_id = st.text_input(label=f"{parents_id_label}", value=st.session_state['donnees'].loc[index, "parents_id"])

            add_generation = st.number_input(label=f'{generation_label}')#, value=st.session_state['donnees'].loc[index, "generation"])


            button_press = st.form_submit_button(label=f"{button_label}")

        if button_press:
            if autogen(traitement_donnees_listes(add_parents_id), add_conjoint_id, liste_patients_dune_famille) != False:
                add_generation = autogen(traitement_donnees_listes(add_parents_id), add_conjoint_id, liste_patients_dune_famille)
            #new_data = {'id':add_id,'nom':add_name,'generation': int(add_generation),'conjoint_id':int(add_conjoint_id),'maladie':add_maladie, 'parents_id':add_parents_id}
            #st.session_state['donnees'].loc[index, "id"] = add_id
            st.session_state['donnees'].loc[index, "nom"] = add_name
            st.session_state['donnees'].loc[index, "maladie"] = str(add_maladie) #OK
            st.session_state['donnees'].loc[index, "generation"] = int(add_generation)
            if add_conjoint_id != 'None' and add_conjoint_id != None and add_conjoint_id != '': #OK
                st.session_state['donnees'].loc[index, "conjoint_id"] = int(add_conjoint_id)
            else:
                st.session_state['donnees'].loc[index, "conjoint_id"] = add_conjoint_id
            st.session_state['donnees'].loc[index, "parents_id"] = add_parents_id #OK
            st.session_state['donnees'].replace("", 'None', inplace=True)
            st.session_state['donnees'].replace('<NA>','None')
            st.session_state['donnees'].fillna('None', inplace=True)
            #st.session_state['donnees'] = st.session_state['donnees'].to_csv(file, index=False, sep=',')

            #Modifications de l'objet MembreFamille associé
            liste_patients_dune_famille[id].nom = add_name
            liste_patients_dune_famille[id].maladie = add_maladie
            liste_patients_dune_famille[id].generation = int(add_generation)
            if add_conjoint_id == '' or add_conjoint_id == 'None':
                liste_patients_dune_famille[id].conjoint_id = None
            else:
                liste_patients_dune_famille[id].conjoint_id = int(add_conjoint_id)
            if add_parents_id == '' or add_parents_id == 'None':
                liste_patients_dune_famille[id].parents_id = None
            else:
                liste_patients_dune_famille[id].parents_id = traitement_donnees_listes(add_parents_id)
            st.balloons()
        else:
            st.write("Veuillez remplir/modifier les données.")



    def clusterize_generation(liste_patients_dune_famille):
        for i in range(0,max_gen(liste_patients_dune_famille)+1):
            with tree.subgraph(name='cluster_gen_'+str(i)) as sub_tree:
                sub_tree.attr(rank='same', peripheries='0')
                #for j in range(len(liste_patients_dune_famille)): #Clustering generationnel
                for key in liste_patients_dune_famille.keys():
                    if liste_patients_dune_famille[key].generation == i:
                        liste_fratrie = liste_enfants_depuis_id_enfant(liste_patients_dune_famille[key].id)
                        if liste_patients_dune_famille[key].parents_id != None and (len(liste_fratrie) % 2 != 0) and (liste_patients_dune_famille[key].id == liste_fratrie[len(liste_fratrie)//2]):
                            sub_tree.node(str(liste_patients_dune_famille[key].id), liste_patients_dune_famille[key].nom, group='G'+str(liste_patients_dune_famille[key].parents_id[0])+'_'+str(liste_patients_dune_famille[key].parents_id[1]), image=liste_patients_dune_famille[key].image, fillcolor=liste_patients_dune_famille[key].colour, style=liste_patients_dune_famille[key].colourstyle)#, fillcolor=liste_patients_dune_famille[j].colour, style=liste_patients_dune_famille[j].colourstyle, image=liste_patients_dune_famille[j].image)
                            #print("HERE")
                            #print("Liste fratrie ", liste_fratrie)
                            #print(liste_fratrie[len(liste_fratrie)//2])
                        else:
                            sub_tree.node(str(liste_patients_dune_famille[key].id), liste_patients_dune_famille[key].nom, group='G'+str(liste_patients_dune_famille[key].id), image=liste_patients_dune_famille[key].image, fillcolor=liste_patients_dune_famille[key].colour, style=liste_patients_dune_famille[key].colourstyle)#, fillcolor=liste_patients_dune_famille[j].colour, style=liste_patients_dune_famille[j].colourstyle, image=liste_patients_dune_famille[j].image)#, image="Exemple_UEPAROPEDO.png")
                list_marriages_done = [] #liste d'ID des personnes déjà marriées via clustering
                n = 0
                #for k in range(len(liste_patients_dune_famille)): #Clustering intra-generationnel de marriage
                for key in liste_patients_dune_famille.keys():
                    if liste_patients_dune_famille[key].generation == i and liste_patients_dune_famille[key].conjoint_id != None and (liste_patients_dune_famille[key].id not in list_marriages_done):
                        list_marriages_done.append(liste_patients_dune_famille[key].id)
                        list_marriages_done.append(liste_patients_dune_famille[key].conjoint_id)
                        with sub_tree.subgraph(name='cluster_gen_'+str(i)+'_marriage_'+str(n)) as sub_sub_tree:
                            sub_sub_tree.attr(rank='same', peripheries='0')
                            liste_fratrie = liste_enfants_depuis_id_enfant(liste_patients_dune_famille[key].id)
                            if liste_patients_dune_famille[key].parents_id != None and (len(liste_fratrie) % 2 != 0) and (liste_patients_dune_famille[key].id == liste_fratrie[len(liste_fratrie)//2]):
                                sub_sub_tree.node(str(liste_patients_dune_famille[key].id), liste_patients_dune_famille[key].nom, group='G'+str(liste_patients_dune_famille[key].parents_id[0])+'_'+str(liste_patients_dune_famille[key].parents_id[1]), image=liste_patients_dune_famille[key].image, fillcolor=liste_patients_dune_famille[key].colour, style=liste_patients_dune_famille[key].colourstyle)#, fillcolor=liste_patients_dune_famille[k].colour, style=liste_patients_dune_famille[k].colourstyle, image=liste_patients_dune_famille[k].image)#, image="Exemple_UEPAROPEDO.png")
                                #print("HERE")
                                #print("Liste fratrie ", liste_fratrie)
                                #print(liste_fratrie[len(liste_fratrie)//2])
                            else:
                                sub_sub_tree.node(str(liste_patients_dune_famille[key].id), liste_patients_dune_famille[key].nom, group='G'+str(liste_patients_dune_famille[key].id), image=liste_patients_dune_famille[key].image, fillcolor=liste_patients_dune_famille[key].colour, style=liste_patients_dune_famille[key].colourstyle)#, fillcolor=liste_patients_dune_famille[k].colour, style=liste_patients_dune_famille[k].colourstyle, image=liste_patients_dune_famille[k].image)
                            sub_sub_tree.node(str(liste_patients_dune_famille[key].conjoint_id), nom_depuis_id(liste_patients_dune_famille[key].conjoint_id), group='G'+str(liste_patients_dune_famille[key].conjoint_id), image=image_conjoint(liste_patients_dune_famille[key].conjoint_id), fillcolor=colour_from_id(liste_patients_dune_famille[key].conjoint_id), style=colourstyle_conjoint(liste_patients_dune_famille[key].conjoint_id))#, fillcolor=colour_from_id(liste_patients_dune_famille[k].conjoint_id), style=colourstyle_conjoint(liste_patients_dune_famille[k].conjoint_id), image=image_conjoint(liste_patients_dune_famille[k].conjoint_id))#, image="Exemple_UEPAROPEDO.png")
                            if liste_patients_dune_famille[key].enfants != None and liste_patients_dune_famille[key].enfants != 'None':
                                if len(liste_patients_dune_famille[key].enfants) % 2 == 0:
                                    sub_sub_tree.node('N' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id), shape='point', **{'width':str(0.08)}, group='G' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id))
                                else:
                                    sub_sub_tree.node('N' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id), shape='point', **{'width':str(0.08)}, group='G' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id))
                            else:
                                    sub_sub_tree.node('N' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id), shape='point', **{'width':str(0.08)}, group='G' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id))    
                        tree.edge(str(liste_patients_dune_famille[key].id), 'N' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id))
                        tree.edge('N' + str(liste_patients_dune_famille[key].id) + '_' + str(liste_patients_dune_famille[key].conjoint_id), str(liste_patients_dune_famille[key].conjoint_id))
                        n+=1
                #print(list_marriages_done)
            with tree.subgraph(name='gen_'+str(i+1)+'_parentchildnodes') as sub_tree2:
                sub_tree2.attr(rank='same', peripheries='0')
                list_parentchildnodes_done = [] #id des enfants déjà faits
                #for l in range(len(liste_patients_dune_famille)):
                for key in liste_patients_dune_famille.keys():
                    if liste_patients_dune_famille[key].generation == i and liste_patients_dune_famille[key].enfants != None and (liste_patients_dune_famille[key].enfants[0] not in list_parentchildnodes_done):
                        if len(liste_patients_dune_famille[key].enfants) % 2 == 0:
                            center_node = 'N' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0]) + '_' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1]) + 'B'
                            sub_tree2.node(center_node, shape='point', **{'width':str(0.08)}, group='G'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0]) + '_' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1]))
                        for id_enfant in liste_patients_dune_famille[key].enfants:
                            list_parentchildnodes_done.append(id_enfant)
                            #print("HERE 4: ", id_enfant)
                            #print("HERE 5: ", liste_id_parents_depuis_id_enfant(id_enfant))
                            parent_child_node = 'N' + str(liste_id_parents_depuis_id_enfant(id_enfant)[0]) + '_' + str(liste_id_parents_depuis_id_enfant(id_enfant)[1]) + '_' + str(id_enfant)
                            if len(liste_patients_dune_famille[key].enfants) % 2 != 0 and id_enfant == liste_patients_dune_famille[key].enfants[int(len(liste_patients_dune_famille[key].enfants)//2)]:
                                sub_tree2.node(parent_child_node, shape='point', **{'width':str(0.08)}, group='G'+str(liste_patients_dune_famille[key].id)+'_'+str(liste_patients_dune_famille[key].conjoint_id))
                            else:
                                sub_tree2.node(parent_child_node, shape='point', **{'width':str(0.08)}, group='G'+str(id_enfant))
                        if len(liste_patients_dune_famille[key].enfants) % 2 == 0:
                            if len(liste_patients_dune_famille[key].enfants) == 2:
                                tree.edge('N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'_'+str(liste_patients_dune_famille[key].enfants[0]), 'N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'B')
                                tree.edge('N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'B', 'N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'_'+str(liste_patients_dune_famille[key].enfants[1]))
                            else:
                                for u in range(int(len(liste_patients_dune_famille[key].enfants)/2-1)):
                                    tree.edge('N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u]), 'N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u+1]))
                                tree.edge('N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'_'+str(liste_patients_dune_famille[key].enfants[int(len(liste_patients_dune_famille[key].enfants)/2-1)]), 'N' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0]) + '_' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1]) + 'B')
                                tree.edge('N' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0]) + '_' + str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1]) + 'B', 'N'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[0])+'_'+str(liste_id_parents_depuis_id_enfant(liste_patients_dune_famille[key].enfants[0])[1])+'_'+str(liste_patients_dune_famille[key].enfants[int(len(liste_patients_dune_famille[key].enfants)/2)]))
                                for u in range(int(len(liste_patients_dune_famille[key].enfants)/2-1), len(liste_patients_dune_famille[key].enfants)-1):
                                    tree.edge('N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u]), 'N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u+1]))
                        else:
                            for u in range(len(liste_patients_dune_famille[key].enfants)-1):
                                tree.edge('N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u]), 'N'+str(liste_id_parents_depuis_id_enfant(id_enfant)[0])+'_'+str(liste_id_parents_depuis_id_enfant(id_enfant)[1])+'_'+str(liste_patients_dune_famille[key].enfants[u+1]))
        #edging
        #tree.edge('N1_2', 'N1_2_5')
        #tree.edge('N1_2_5', '5')
        
        list_parentchildedges_done = []
        #for gen in range(0, max_gen(liste_patients_dune_famille)+1):
        #for family_member in liste_patients_dune_famille:
        for family_member in liste_patients_dune_famille.values():
            #if family_member.generation == gen:
            if family_member.enfants != None and (family_member.id not in list_parentchildedges_done):
                list_parentchildedges_done.append(family_member.id)
                list_parentchildedges_done.append(family_member.conjoint_id)
                if len(family_member.enfants) % 2 == 0:
                    tree.edge('N'+str(family_member.id)+'_'+str(family_member.conjoint_id), 'N'+str(family_member.id)+'_'+str(family_member.conjoint_id)+'B')
                else:
                    tree.edge('N'+str(family_member.id)+'_'+str(family_member.conjoint_id), 'N'+str(family_member.id)+'_'+str(family_member.conjoint_id)+'_'+str(family_member.enfants[len(family_member.enfants)//2]))
                for p in range(len(family_member.enfants)):
                        tree.edge('N'+str(family_member.id)+'_'+str(family_member.conjoint_id)+'_'+str(family_member.enfants[p]), str(family_member.enfants[p]))


    def image_ou_non(un_booleen):
        if un_booleen:
            image_code(liste_patients_dune_famille)
        else:
            colour_code(liste_patients_dune_famille)


    #####RENDERING ////////////////////////////////////////////////////////////////////////////////////////////////////////


    tree = graphviz.Graph(  engine='dot',
                            graph_attr={
                                        'splines': 'false',
                                        'newrank':'true',
                                        'ranksep': '0.1',
                                        'concentrate': 'false',
                            },
                            node_attr={'style': 'filled, rounded', 'shape': 'none'},
                            edge_attr={'dir': 'none', 'arrowhead': 'none'},
                            encoding='utf8',
                            filename='family_tree',
                            format='pdf')


    with st.sidebar:
        pages = {
            "Ajouter": ajouter_personne,
            "Supprimer": supprimer_personne,
            "Modifier": modifier_personne
        }
        selected_page = st.selectbox(
            "Choose page",
            pages.keys()
        )
        pages[selected_page]()

    st.session_state['donnees'].replace("", 'None', inplace=True)
    st.session_state['donnees'].replace('<NA>','None')
    st.session_state['donnees'].fillna('None', inplace=True)
    st.download_button("Télécharger les données", st.session_state['donnees'].to_csv(index=False, sep=',').encode('ansi'),file_name="donnees.csv", key="b1")
    st.session_state['donnees'].to_excel("donnees.xlsx")
    #st.download_button("Télécharger les données", st.session_state['donnees'].to_excel("donnees.xlsx"), key="b2", mime="text/csv")
    image_ou_non(False)
    clusterize_generation(liste_patients_dune_famille)

    #print(tree.source)
    #tree.view()
    tree.render()

    #st.graphviz_chart(tree)

    def displayPDF(file):
        # Opening file from file path
        with open(file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # Embedding PDF in HTML
        #pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)


    # def highlight_col(x):
    #     r = 'background-color: red'
    #     df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    #     df1.iloc[:, 0] = r
    #     return df1    
    # donnees.style.apply(highlight_col, axis=None)

    #donnees = pd.read_csv(file, sep=',')
    #file.seek(0)
    #st.dataframe(pd.read_csv(file, low_memory=False))
    #st.session_state['donnees'] = df
    dataframe = st.session_state['donnees'].drop(columns=['colour', 'colourstyle', 'image'])
    #id, nom, maladie, generation, conjoint_id, parents_id, enfants, colour, colourstyle, sexe, image
    st.dataframe(dataframe.style.set_properties(**{'background-color': 'salmon'}, subset=['id']))

    displayPDF("C:\\Programming_late_2022\\python_projects\\giraffe\\family_tree.pdf")