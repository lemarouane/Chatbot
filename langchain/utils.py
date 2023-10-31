import os
import random
import streamlit as st

# Définir votre token API OpenAI en tant que variable globale
OPENAI_API_KEY = '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'

#decorator
def enable_chat_history(func):
    if OPENAI_API_KEY:

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Comment pourrais-je vous aider ?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Méthode pour afficher un message sur l'interface utilisateur

    Args:
        msg (str): message à afficher
        author (str): auteur du message - utilisateur/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_openai_api_key():
    # Utilisez la variable globale pour configurer l'environnement OpenAI API
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

if __name__ == "__main__":
    configure_openai_api_key()  # Configurez l'environnement OpenAI API au début de l'exécution

    obj = Basic()
    obj.main()
