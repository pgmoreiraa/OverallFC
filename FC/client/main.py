import streamlit as st
import requests

# URL da API FastAPI (servidor)
API_URL = "http://127.0.0.1:8000"

def carregar_lista_jogadores():
    """
    Busca o dicionário de nomes de jogadores na API para popular o selectbox.
    """
    try:
        response = requests.get(f"{API_URL}/jogadores_nomes")
        if response.status_code == 200:
            st.session_state.lista_jogadores = response.json()
        else:
            st.error("Erro ao carregar a lista de jogadores.")
            st.session_state.lista_jogadores = {}
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar ao servidor (lista de jogadores).")
        st.session_state.lista_jogadores = {}


def iniciar_jogo():
    """
    Busca um novo jogador aleatório na API e zera a pontuação.
    """
    try:
        response = requests.get(f"{API_URL}/jogador_aleatorio")
        if response.status_code == 200:
            st.session_state.jogador_atual = response.json()
            st.session_state.pontos = 0
            st.session_state.game_over = False
        else:
            st.error("Erro ao iniciar o jogo. O servidor FastAPI está rodando?")
            st.session_state.jogador_atual = None
            st.session_state.game_over = True
    except requests.exceptions.ConnectionError:
        st.error("NÃO FOI POSSÍVEL CONECTAR AO SERVIDOR DA API.")
        st.info("Verifique se o servidor FastAPI (server/app/main.py) está em execução.")
        st.session_state.jogador_atual = None
        st.session_state.game_over = True

def fazer_palpite(palpite_chave):
    """
    Envia o palpite (agora uma CHAVE, ex: "vini jr") para a API 
    e trata o resultado.
    """
    if not palpite_chave:
        st.warning("Por favor, selecione um jogador.")
        return

    jogador_a_nome = st.session_state.jogador_atual["name"]
    payload = {
        "jogador_a_nome": jogador_a_nome,
        "jogador_b_input": palpite_chave
    }

    try:
        response = requests.post(f"{API_URL}/comparar", json=payload)
        
        if response.status_code != 200:
            st.error("Erro na API. Tente novamente.")
            return

        data = response.json()
        resultado = data.get("resultado")
        
        if resultado == "correto":
            jogador_a = data["jogador_a"]
            jogador_b = data["jogador_b"]
            st.session_state.pontos += 1
            st.success(f"BOA! {jogador_b['name']} (OVR {jogador_b['overall']}) é maior que {jogador_a['name']} (OVR {jogador_a['overall']}).")
            st.session_state.jogador_atual = jogador_b # Próxima rodada

        elif resultado == "incorreto":
            jogador_a = data["jogador_a"]
            jogador_b = data["jogador_b"]
            st.error(f"ERROU! {jogador_b['name']} (OVR {jogador_b['overall']}) NÃO é maior que {jogador_a['name']} (OVR {jogador_a['overall']}).")
            st.session_state.game_over = True # Fim de jogo

        elif resultado == "nao_encontrado":
            st.warning(f"Jogador '{data.get('palpite')}' não foi encontrado.")
        
        else:
            st.error("Resposta inesperada da API.")
            
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar ao servidor da API.")

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Jogo do Maior Overall", page_icon="🎮")
st.title("🎮 Jogo do Maior Overall")

# --- Inicialização do Estado do Jogo ---
if "lista_jogadores" not in st.session_state:
    carregar_lista_jogadores()

if "jogador_atual" not in st.session_state or st.session_state.get("game_over", False):
    if st.session_state.get("game_over", False):
        st.info(f"Fim de jogo! Sua pontuação final foi: {st.session_state.pontos}")
    
    if st.button("Iniciar Jogo" if "jogador_atual" not in st.session_state else "Jogar Novamente"):
        st.session_state.game_over = False
        iniciar_jogo()
        st.rerun()
    
    st.stop()


# --- Interface do Usuário (Se o jogo está rodando) ---
if st.session_state.jogador_atual and st.session_state.lista_jogadores:
    
    st.metric("Pontuação Atual", st.session_state.pontos)
    st.divider()
    st.header(f"Jogador Atual: {st.session_state.jogador_atual['name']}")
    st.subheader(f"Overall: ???")
    st.write("\n")
    st.write("Selecione um jogador que você acha que tem um Overall **MAIOR**:")

    #
    # --- CORREÇÃO ESTÁ AQUI ---
    #
    
    # 1. Definimos o formulário sem o 'on_submit'
    with st.form(key="palpite_form"):
        
        opcoes_chaves = list(st.session_state.lista_jogadores.keys())
        
        def formatar_nome(chave):
            return st.session_state.lista_jogadores.get(chave, "Erro")

        st.selectbox(
            "Selecione o jogador:", 
            key="palpite_select",
            options=opcoes_chaves,
            format_func=formatar_nome,
            index=None, 
            placeholder="Selecione um jogador...",
            label_visibility="collapsed"
        )
        
        # 2. Capturamos o estado do botão DE DENTRO do formulário
        submitted = st.form_submit_button(label="Adivinhar!")

    # 3. Verificamos se o botão foi pressionado FORA do formulário
    if submitted:
        palpite_chave = st.session_state.palpite_select 
        fazer_palpite(palpite_chave)
        st.rerun() # Recarrega a página para refletir a mudança

elif not st.session_state.get("game_over", False):
    st.error("Não foi possível carregar o jogo.")
    if st.button("Tentar conectar novamente"):
        carregar_lista_jogadores()
        iniciar_jogo()
        st.rerun()