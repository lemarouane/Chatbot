import streamlit as st
import streamlit_survey as ss
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector

st.set_page_config(page_title="Chatbot with Questionnaire")

survey = ss.StreamlitSurvey("Survey Example - Advanced Usage")
pages = survey.pages(8, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
with pages:
    if pages.current == 0:
        st.write("Avez-vous déjà consulté un psychologue ou un professionnel de la santé mentale?")
        consulted_before = survey.radio(
            "consulted_before",
            options=["NA", "Oui", "Non"],
            index=0,
            label_visibility="collapsed",
            horizontal=True,
        )
        
        if consulted_before == "Oui":
            st.write("Combien de fois avez-vous consulté?")
            consult_frequency = survey.select_slider(
                "consult_frequency",
                options=["Régulièrement", "Occasionnellement", "Une fois", "Jamais"],
                label_visibility="collapsed",
            )
        
        elif consulted_before == "Non":
            st.write("Avez-vous déjà utilisé d'autres méthodes d'auto-assistance pour la santé mentale?")
            used_self_help = survey.radio(
                "used_self_help",
                options=["NA", "Oui", "Non"],
                index=0,
                label_visibility="collapsed",
                horizontal=True,
            )
            
            if used_self_help == "Oui":
                st.write("Lesquelles?")
                self_help_methods = survey.multiselect(
                    "self_help_methods",
                    options=["Méditation", "Exercice", "Livres d'auto-assistance", "Applications de bien-être", "Autres"],
                    label_visibility="collapsed",
                )
    elif pages.current == 1:
        st.write("Quelle est votre principale source de stress actuelle?")
        stress_source = survey.selectbox(
        "stress_source",
        options=["Travail", "Relations familiales", "Relations amoureuses", "Finances", "Santé", "Autre"],
        label_visibility="collapsed",
    )
        if stress_source == "Autre":
            st.write("Précisez la principale source de stress:")
            other_stress_source = survey.text_input("Source de stress autre")
    

    elif pages.current == 2:
        st.write("Imaginez que vous êtes dans un endroit sûr et paisible de votre imagination.")
        st.write("Décrivez cet endroit en détail. Comment se sent-il? Quelles couleurs, sons et sensations y associez-vous?")
        imaginary_place = survey.text_area("Décrivez votre lieu imaginaire de paix", height=200)

        st.write("Quand vous ressentez du stress, pensez-vous à votre lieu imaginaire de paix?")
        peace_oasis = survey.radio(
        "peace_oasis",
            options=["NA", "Oui, souvent", "Parfois", "Non, jamais"],
            index=0,
            label_visibility="collapsed",
            horizontal=True,
    )

    elif pages.current == 3:
        st.write("Les émotions peuvent être complexes. Cochez les émotions qui décrivent le mieux ce que vous ressentez en ce moment :")
    
        joy = survey.checkbox("Joie")
        sadness = survey.checkbox("Tristesse")
        anger = survey.checkbox("Colère")
        fear = survey.checkbox("Peur")
        serenity = survey.checkbox("Sérénité")
        confusion = survey.checkbox("Confusion")
        determination = survey.checkbox("Détermination")
        other_emotion = ""

        if survey.checkbox("Autre"):
            other_emotion = survey.text_input("Émotion autre")

    elif pages.current == 4:
        st.write("Pensez à un événement récent qui vous a apporté de la joie ou du bonheur.")
        st.write("Sélectionnez la date de cet événement et partagez ce qui s'est passé :")
    
        joy_event_date = st.date_input("Date de l'événement")
        st.write("Qu'est-ce qui s'est passé lors de cet événement qui vous a apporté de la joie ou du bonheur?")
        joy_event_description = survey.text_area("Description de l'événement", height=200)
    elif pages.current == 5:
        st.write("Imaginez que votre niveau de bonheur est représenté par un curseur.")
        st.write("Où placeriez-vous le curseur en ce moment pour indiquer votre niveau de bonheur?")
    
        happiness_level = st.slider("Niveau de bonheur:", min_value=0, max_value=100, value=50)

        st.write("Pourquoi avez-vous choisi ce niveau de bonheur? Quelles sont les raisons derrière votre choix?")
        happiness_reason = survey.text_area("Raisons du choix", height=200)

    # Vous pouvez maintenant enregistrer le niveau de bonheur et les raisons du choix.

    elif pages.current == 6:
        st.write("Imaginez que vous évaluez votre niveau de stress sur une échelle de 0 à 5, où 0 signifie aucun stress et 5 signifie un stress maximal.")
        st.write("Sur cette échelle, quel niveau de stress attribueriez-vous à votre situation actuelle?")

        stress_level = st.number_input("Niveau de stress (0-5):", min_value=0, max_value=5, value=2, step=1)

        if stress_level == 5:
            st.write("Pouvez-vous expliquer ce qui contribue à votre niveau de stress maximal?")
            stress_reason = survey.text_area("Raisons du stress maximal", height=200)

    # Vous pouvez maintenant enregistrer le niveau de stress et les raisons du choix.

    elif pages.current == 7:
        st.write("Imaginez que vous évaluez votre niveau général de satisfaction avec votre vie en utilisant une échelle de Likert.")
        st.write("Choisissez l'emoji qui représente le mieux votre niveau de satisfaction actuel :")

        satisfaction_level = survey.radio("Niveau de satisfaction:", options=["😞", "🙁", "😐", "🙂", "😀"], horizontal=True)

        if satisfaction_level in ["😞", "🙁"]:
            st.write("Quels facteurs contribuent à votre niveau de satisfaction actuel?")
            satisfaction_reason = survey.text_area("Raisons de la satisfaction actuelle", height=200)

    # Vous pouvez maintenant enregistrer le niveau de satisfaction et les raisons du choix.


