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
            st.session_state.mostrar_resultado = False
            st.session_state.ultimo_resultado = None
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
    Envia o palpite para a API e trata o resultado.
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
        
        # Armazena o resultado para exibição
        st.session_state.ultimo_resultado = {
            "resultado": resultado,
            "jogador_a": data["jogador_a"],
            "jogador_b": data["jogador_b"],
        }
        st.session_state.mostrar_resultado = True
        
        if resultado == "correto":
            st.session_state.pontos += 1
            # Próximo jogador é aleatório (vem da API)
            st.session_state.jogador_atual = data["proximo_jogador"]

        elif resultado == "empate":
            # Mantém pontuação, mas muda para próximo jogador aleatório
            st.session_state.jogador_atual = data["proximo_jogador"]

        elif resultado == "incorreto":
            st.session_state.game_over = True

        elif resultado == "nao_encontrado":
            st.warning(f"Jogador '{data.get('palpite')}' não foi encontrado.")
            st.session_state.mostrar_resultado = False
        
        else:
            st.error("Resposta inesperada da API.")
            st.session_state.mostrar_resultado = False
            
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar ao servidor da API.")

def continuar_jogo():
    """
    Limpa o resultado e continua para a próxima rodada.
    """
    st.session_state.mostrar_resultado = False
    st.session_state.ultimo_resultado = None

# --- Configuração da Página Streamlit ---
st.set_page_config(
    page_title="Jogo do Maior Overall", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    /* Esconder elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo geral */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    .main .block-container {
        padding-bottom: 5rem;
    }
    
    /* Card do jogador */
    .player-card {
        text-align: center;
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 20px 0;
        transition: transform 0.3s ease;
    }
    
    .player-card:hover {
        transform: translateY(-5px);
    }
    
    /* Nome do jogador */
    .player-name {
        font-size: 2.5em;
        font-weight: bold;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin: 15px 0;
        letter-spacing: 1px;
    }
    
    /* Overall */
    .player-overall {
        font-size: 2em;
        color: #FFD700;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 10px 0;
    }
    
    /* Imagem do jogador */
    .player-image {
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 10px auto;
        display: block;
    }
    
    /* Resultado */
    .resultado-box {
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.3em;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .resultado-correto {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .resultado-incorreto {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
    
    .resultado-empate {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    /* Título */
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-title">JOGO DO MAIOR OVERALL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Teste seus conhecimentos sobre EA FC 26!</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Inicialização do Estado do Jogo ---
if "lista_jogadores" not in st.session_state:
    carregar_lista_jogadores()

if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False

if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = None

# --- Tela Inicial / Game Over ---
if "jogador_atual" not in st.session_state or st.session_state.get("game_over", False):
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.get("game_over", False):
            st.markdown("### 🏆 FIM DE JOGO!")
            st.markdown(f"### Sua pontuação final: **{st.session_state.pontos}** pontos")
            
            if st.session_state.pontos == 0:
                st.markdown("💪 Não desanime! Tente novamente!")
            elif st.session_state.pontos < 5:
                st.markdown("👍 Bom começo! Continue praticando!")
            elif st.session_state.pontos < 10:
                st.markdown("🔥 Muito bem! Você conhece bem os jogadores!")
            else:
                st.markdown("🌟 INCRÍVEL! Você é um expert em EA FC 26!")
        
        st.markdown("")
        if st.button(
            "🎲 INICIAR JOGO" if "jogador_atual" not in st.session_state else "🔄 JOGAR NOVAMENTE", 
            type="primary",
            use_container_width=True
        ):
            st.session_state.game_over = False
            iniciar_jogo()
            st.rerun()
    
    st.stop()

# --- Exibir Resultado da Rodada Anterior ---
if st.session_state.mostrar_resultado and st.session_state.ultimo_resultado:
    resultado_data = st.session_state.ultimo_resultado
    resultado = resultado_data["resultado"]
    jogador_a = resultado_data["jogador_a"]
    jogador_b = resultado_data["jogador_b"]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if resultado == "correto":
            st.markdown(
                f'<div class="resultado-box resultado-correto">'
                f'✅ CORRETO! +1 PONTO<br>'
                f'{jogador_b["name"]} ({jogador_b["overall"]} OVR) > {jogador_a["name"]} ({jogador_a["overall"]} OVR)'
                f'</div>',
                unsafe_allow_html=True
            )
        elif resultado == "empate":
            st.markdown(
                f'<div class="resultado-box resultado-empate">'
                f'🤝 EMPATE! Mantém a streak!<br>'
                f'{jogador_b["name"]} ({jogador_b["overall"]} OVR) = {jogador_a["name"]} ({jogador_a["overall"]} OVR)'
                f'</div>',
                unsafe_allow_html=True
            )
        elif resultado == "incorreto":
            st.markdown(
                f'<div class="resultado-box resultado-incorreto">'
                f'❌ ERROU! Fim de jogo!<br>'
                f'{jogador_b["name"]} ({jogador_b["overall"]} OVR) ≤ {jogador_a["name"]} ({jogador_a["overall"]} OVR)'
                f'</div>',
                unsafe_allow_html=True
            )
        
        if resultado != "incorreto":
            if st.button("➡️ CONTINUAR", type="primary", use_container_width=True):
                continuar_jogo()
                st.rerun()
        else:
            if st.button("🔄 JOGAR NOVAMENTE", type="primary", use_container_width=True):
                st.session_state.game_over = False
                iniciar_jogo()
                st.rerun()
    
    st.stop()

# --- Interface do Jogo ---
if st.session_state.jogador_atual and st.session_state.lista_jogadores:
    
    # Exibir pontuação
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"### ⭐ Pontuação: **{st.session_state.pontos}**")
    
    st.markdown("")
    
    # Exibir carta do jogador atual
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Exibir imagem do jogador se disponível
        if st.session_state.jogador_atual.get("image_url"):
            st.image(
                st.session_state.jogador_atual["image_url"],
                width=250,
                use_container_width=False
            )
        
        # Nome do jogador
        st.markdown(
            f'<div class="player-name">{st.session_state.jogador_atual["name"]}</div>',
            unsafe_allow_html=True
        )
        
        # Overall oculto
        st.markdown(
            '<div class="player-overall">Overall: ???</div>',
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
    # Formulário de palpite
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("### 🤔 Escolha um jogador com Overall **MAIOR**:")
        
        with st.form(key="palpite_form"):
            
            opcoes_chaves = list(st.session_state.lista_jogadores.keys())
            
            def formatar_nome(chave):
                return st.session_state.lista_jogadores.get(chave, "Erro")

            st.selectbox(
                "Escolha o jogador:", 
                key="palpite_select",
                options=opcoes_chaves,
                format_func=formatar_nome,
                index=None, 
                placeholder="🔍 Selecione um jogador...",
                label_visibility="collapsed"
            )
            
            submitted = st.form_submit_button(
                label="✅ CONFIRMAR PALPITE", 
                type="primary", 
                use_container_width=True
            )

        if submitted:
            palpite_chave = st.session_state.palpite_select 
            fazer_palpite(palpite_chave)
            st.rerun()

elif not st.session_state.get("game_over", False):
    st.error("❌ Não foi possível carregar o jogo.")
    if st.button("🔄 Tentar conectar novamente"):
        carregar_lista_jogadores()
        iniciar_jogo()
        st.rerun()
