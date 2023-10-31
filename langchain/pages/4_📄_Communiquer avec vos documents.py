import os
import utils
import streamlit as st
from streaming import StreamHandler

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header('Discutez avec vos documents')
st.write("La fonctionnalité 'Discutez avec vos documents' vous permet d'interagir avec un chatbot capable d'accéder à des documents personnalisés. Cette fonction peut être incroyablement utile pour votre santé mentale et votre bien-être. Voici comment :")

st.write("1. **Réflexion et Expression Personnelles :** Utilisez cette fonction pour écrire et exprimer vos pensées, émotions et expériences. Noter vos pensées peut vous aider à clarifier vos sentiments et à mieux comprendre votre bien-être émotionnel.")

st.write("2. **Journal Numérique :** Pensez-y comme un journal numérique. Enregistrez vos pensées quotidiennes, vos préoccupations et vos réalisations, ce qui facilite le suivi de votre parcours en matière de santé mentale.")

st.write("3. **Traitement des Traumatismes :** Pour certaines personnes, écrire sur des expériences traumatiques peut être un moyen de les traiter. En enregistrant et en discutant de ces expériences, les individus peuvent commencer à guérir et à faire face à ces événements.")

st.write("4. **Planification et Définition d'Objectifs :** Utilisez le chatbot pour définir des objectifs, créer des plans d'action et suivre votre progression. Cela peut être bénéfique pour le développement personnel et la gestion du stress.")

st.write("5. **Référence Future :** Sauvegardez les conversations avec le chatbot pour une référence future. Vous pouvez les revisiter et relire les discussions passées pour vous rappeler de précieux conseils, astuces ou moments de réflexion.")

st.write("6. **Prise de Conscience de Soi :** En examinant vos propres écrits, vous pouvez prendre conscience de schémas de pensée ou de comportements qui affectent votre santé mentale. Cette prise de conscience de soi peut vous aider à effectuer des changements positifs.")

st.write("7. **Suivi de la Progression :** Si vous souffrez de troubles de santé mentale, cette fonction peut vous aider à suivre les symptômes, les humeurs et votre progression au fil du temps. Elle est particulièrement utile pour les personnes atteintes de dépression, d'anxiété ou de troubles bipolaires.")

st.write("N'oubliez pas que, bien que cette fonction puisse être utile, elle ne remplace pas les soins de santé mentale professionnels. Elle peut cependant compléter les soins professionnels en offrant un espace d'auto-assistance et de réflexion. Il est essentiel de maintenir la confidentialité et la sécurité des données lors de l'utilisation de cette fonction, car elle enregistre des informations personnelles et des pensées intimes.")

class CustomDataChatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"

    def save_file(self, file):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = f'./{folder}/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return file_path

    @st.spinner('Analyzing documents..')
    def setup_qa_chain(self, uploaded_files):
        # Load documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # Create embeddings and store in vectordb
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type='mmr',
            search_kwargs={'k':2, 'fetch_k':4}
        )

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

        # Setup LLM and QA chain
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=True)
        return qa_chain

    @utils.enable_chat_history
    def main(self):

        # User Inputs
        uploaded_files = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=True)
        if not uploaded_files:
            st.error("Please upload PDF documents to continue!")
            st.stop()

        user_query = st.chat_input(placeholder="Ask me anything!")

        if uploaded_files and user_query:
            qa_chain = self.setup_qa_chain(uploaded_files)

            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                response = qa_chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = CustomDataChatbot()
    obj.main()