import streamlit as st
import app_01
import app_02

# Função para exibir a página inicial
def show_landing_page():
    st.title("Bem-vindo ao Programa de Raspagem da FGV!")
    st.write("Este programa permite raspar o site da FGV para demonstrar somente informações essenciais sobre os integrantes.")

# Crie um dicionário de opções de páginas
PAGES = {
    "Página Inicial": show_landing_page,
    "Corpo docente da ECMI": app_01.app,
    "Corpo docente da EMAP": app_02.app,
}

# Função principal para controlar a navegação e a renderização do aplicativo
def main():
    st.sidebar.title('Raspagem do Corpo Docente da FGV')
    st.sidebar.markdown('---')
    st.sidebar.subheader('Selecione qual das opções você deseja raspar:')
    
    # Obtenha a seleção do usuário
    selection = st.sidebar.radio("", list(PAGES.keys()))

    # Renderize o aplicativo selecionado
    if selection == "Página Inicial":
        show_landing_page()
    else:
        page = PAGES[selection]
        page()

if __name__ == "__main__":
    main()
