import mysql.connector
import utils
import streamlit as st
from streaming import StreamHandler

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Créez une connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot"
)
cursor = conn.cursor()

st.set_page_config(page_title="Psychologist Chat", page_icon="🧠")
st.header('Discutez avec Votre Psychologue 🧠')
st.write('Permet aux utilisateurs d\'interagir avec le chatbot psychologue.')

class ContextChatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"
    
    @st.cache_resource
    def setup_chain(_self):
        memory = ConversationBufferMemory()
        llm = OpenAI(model_name=_self.openai_model, temperature=0, streaming=True)
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Posez votre question ou partagez vos préoccupations :")
        if user_query:
            utils.display_msg(user_query, 'user')

            with st.chat_message("Réflexion en cours..."):
                st_cb = StreamHandler(st.empty())
                response = chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})

            # Insertion de la conversation dans la base de données après avoir obtenu la réponse
            insert_query = "INSERT INTO conversations (user_message, assistant_message) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_query, response))
            conn.commit()

if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()
    cursor.close()
    conn.close()
