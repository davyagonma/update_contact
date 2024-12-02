import streamlit as st
import pandas as pd
import re

def process_phone_numbers(file):
    # Charger le fichier CSV
    contacts = pd.read_csv(file)
    
    # Identifier la colonne contenant les numéros (supposons qu'elle s'appelle "phone")
    # if "phone" not in contacts.columns:
    #     st.error("Le fichier CSV doit contenir une colonne 'phone' avec les numéros de téléphone.")
    #     return None
    
    # Fonction pour nettoyer et mettre à jour les numéros
    def update_phone_number(phone):
        phone = re.sub(r'\s+', '', str(phone))  # Supprimer les espaces
        if phone.startswith("+229") or phone.startswith("00229"):
            phone = re.sub(r"(\+229|00229)", r"\1 01", phone)
        elif len(phone) == 8 and phone.isdigit():
            phone = "+229 01" + phone
        return phone
    
    # Mettre à jour les numéros dans la colonne 'phone'
    contacts["Phone 1 - Value"] = contacts["Phone 1 - Value"].apply(update_phone_number)
    
    return contacts

def main():
    st.title("Mise à jour des numéros Béninois 📞")
    st.write("Importez un fichier CSV contenant la liste de vos contacts, et obtenez un nouveau CSV avec les numéros mis à jour.")
    
    # Charger le fichier CSV
    uploaded_file = st.file_uploader("Chargez votre fichier CSV", type=["csv"])
    
    if uploaded_file:
        # Traiter les numéros
        updated_contacts = process_phone_numbers(uploaded_file)
        
        if updated_contacts is not None:
            st.success("Les numéros ont été mis à jour avec succès !")
            
            # Permettre le téléchargement du fichier mis à jour
            csv = updated_contacts.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Télécharger le fichier mis à jour 📥",
                data=csv,
                file_name="contacts_updated.csv",
                mime="text/csv",
            )
    st.write("## Made by Davy AGONMA +229 0154073727")

if __name__ == "__main__":
    main()
