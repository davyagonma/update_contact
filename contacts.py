import streamlit as st
import pandas as pd
import re

def process_phone_numbers(file):
    # Charger le fichier CSV
    contacts = pd.read_csv(file)
    
    # Ajout de la checkbox pour afficher les conditions d'utilisation
    if st.checkbox("Comment ça marche !?"):
        st.subheader("Conditions d’utilisation de l’application")
        st.markdown("""
        ### Bienvenue sur notre application !  
        Avant de l’utiliser, voici tout ce que vous devez savoir pour une expérience simple et fluide.  

        #### **Ce que fait l’application :**  
        - Vous importez un fichier CSV contenant vos contacts.  
        - L’application met automatiquement à jour les numéros de téléphone béninois :  
        - Elle ajoute **"01"** après les indicatifs **+229** ou **00229**.  
        - Elle ajoute **"01"** devant les numéros à 8 chiffres sans indicatif.  
        - Elle supprime les espaces dans les numéros pour uniformiser le format.  
        - Vous téléchargez un nouveau fichier CSV prêt à être utilisé ou importé dans Google Contacts.  

        #### **Comment obtenir votre fichier CSV depuis Google Contacts ?**  
        1. Accédez à vos contacts Google : [Google Contacts](https://contacts.google.com).  
        2. Sélectionnez vos contacts :  
        - Par défaut, tous vos contacts sont sélectionnés.  
        - Si vous souhaitez exporter uniquement un groupe spécifique, utilisez le menu de gauche pour choisir un groupe.  
        3. Exportez vos contacts :  
        - Cliquez sur l’icône **"Exporter"** (dans le menu de gauche ou via les paramètres).  
        - Sélectionnez le format **Google CSV** pour l'exportation.  
        - Téléchargez le fichier sur votre ordinateur.  
        4. Consultez ce guide officiel de Google : [Exporter vos contacts](https://support.google.com/contacts/answer/1069522).  

        #### **Ce que vous devez faire :**  
        - Chargez le fichier CSV obtenu dans l’application en cliquant sur **"Charger un fichier"**.  
        - Lancez le traitement pour mettre à jour les numéros de téléphone.  
        - Téléchargez le fichier mis à jour une fois le traitement terminé.  
        - Réimportez le fichier dans Google Contacts :  
        - Retournez sur **Google Contacts**.  
        - Cliquez sur **"Importer"**, choisissez le fichier mis à jour et validez.  

        #### **Responsabilités et limites :**  
        - **Format du fichier** : Assurez-vous d’utiliser un fichier CSV valide. L’application ne peut pas traiter d’autres formats.  
        - **Vérification des résultats** : Vous devez vérifier les numéros mis à jour avant de les utiliser.  
        - **Données sensibles** : Aucun fichier n’est conservé sur nos serveurs. Tout traitement est effectué localement.  

        #### **Assistance :**  
        Si vous avez des questions ou des problèmes :  
        - Consultez notre documentation intégrée.  
        - Contactez-nous via [singbodavyagonma@gmail.com](mailto:singbodavyagonma@gmail.com) ou [kloo.me/davyagonma](https://kloo.me/davyagonma).  
        """)
    
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
