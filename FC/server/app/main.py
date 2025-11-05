import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- Mapeamento de IDs dos Jogadores ---
PLAYER_IDS = {
    # Overall 91
    "mbappe": "231747", "salah": "209331", "putellas": "227203",
    "bonmati": "241667", "rodri": "231866", "haaland": "239085",
    
    # Overall 90
    "bellingham": "252371", "van dijk": "203376", "hansen": "227102",
    "kane": "202126", "dembele": "231443", "messi": "158023",
    "lewandowski": "188545", "de bruyne": "192985",
    
    # Overall 89
    "vini jr": "238794", "alisson": "212831", "donnarumma": "230621",
    "courtois": "192119", "lautaro martinez": "231478", "sophia smith": "264012",
    "valverde": "239053", "hakimi": "235212", "yamal": "277643",
    "kimmich": "212622", "mapi leon": "236479", "griezmann": "194765",
    "ruben dias": "239818", "bruno fernandes": "212198", "bernardo silva": "218667",
    "osimhen": "232293",
    
    # Overall 88
    "saka": "246669", "rice": "234378", "odegaard": "222665",
    "wirtz": "256630", "reiten": "227323", "katoto": "227361",
    "diani": "227361", "ter stegen": "192448", "neuer": "167495",
    "son": "200104", "musiala": "256790", "rafael leao": "241721",
    "araujo": "253163", "de jong": "228702", "paralluelo": "269404",
    "oberdorf": "248717", "debora": "226893",
    
    # Overall 87
    "musah": "253177", "theo hernandez": "232656", "marquinhos": "207865",
    "maignan": "215698", "kvaratskhelia": "247635", "foden": "237692",
    "militao": "240130", "barella": "224232", "grealish": "206517",
    "rodrygo": "243812", "dybala": "211110", "popp": "226302",
    "morgan": "226301", "neymar": "190871", "pedri": "251854",
    
    # Overall 86
    "tonali": "241096", "rashford": "231677", "gvardiol": "251517",
    "gabriel": "246420", "saliba": "243715", "alexander-arnold": "231281",
    "robertson": "216267", "gundogan": "186942", "cancelo": "210514",
    "kounde": "241486", "tchouameni": "241637", "camavinga": "248243",
    "nkunku": "232411", "diogo jota": "224458", "szoboszlai": "236772",
    "bono": "226786", "kerr": "227125", "walsh": "242830",
    
    # Overall 85
    "gimenez": "216460", "kostic": "208574", "trippier": "186345",
    "luis diaz": "241084", "diaby": "241852", "coman": "213345",
    "cristiano ronaldo": "20801", "gavi": "264240", "alaba": "197445",
    "bremer": "239580", "vlahovic": "246430", "darwin nunez": "253072",
    "isak": "233731", "bruno guimaraes": "247851", "julian alvarez": "246191",
}

# URLs base para imagens
CARD_BACKGROUND_URL = "https://cdn3.futbin.com/content/fifa26/img/cards/hd/1_gold.png"
PLAYER_IMAGE_BASE_URL = "https://cdn.futbin.com/content/fifa26/img/players/"

def get_player_image_url(player_key):
    """Retorna a URL da imagem do jogador"""
    player_id = PLAYER_IDS.get(player_key.lower())
    if player_id:
        return f"{PLAYER_IMAGE_BASE_URL}{player_id}.png"
    return None

# --- Banco de Dados (Dicionário de Jogadores) ---
PLAYERS_DB = {
    # Chave em minúsculo (para busca), dados com nome correto
    
    # === Overall 91 ===
    "mbappe": {"name": "Kylian Mbappé", "overall": 91},
    "salah": {"name": "Mohamed Salah", "overall": 91},
    "putellas": {"name": "Alexia Putellas", "overall": 91},
    "bonmati": {"name": "Aitana Bonmatí", "overall": 91},
    "rodri": {"name": "Rodri", "overall": 91},
    "haaland": {"name": "Erling Haaland", "overall": 91},

    # === Overall 90 ===
    "bellingham": {"name": "Jude Bellingham", "overall": 90},
    "van dijk": {"name": "Virgil van Dijk", "overall": 90},
    "hansen": {"name": "Caroline Graham Hansen", "overall": 90},
    "kane": {"name": "Harry Kane", "overall": 90},
    "dembele": {"name": "Ousmane Dembélé", "overall": 90},
    "messi": {"name": "Lionel Messi", "overall": 90},
    "lewandowski": {"name": "Robert Lewandowski", "overall": 90},
    "de bruyne": {"name": "Kevin De Bruyne", "overall": 90},

    # === Overall 89 ===
    "vini jr": {"name": "Vini Jr.", "overall": 89},
    "alisson": {"name": "Alisson", "overall": 89},
    "donnarumma": {"name": "Gianluigi Donnarumma", "overall": 89},
    "courtois": {"name": "Thibaut Courtois", "overall": 89},
    "lautaro martinez": {"name": "Lautaro Martínez", "overall": 89},
    "sophia smith": {"name": "Sophia Smith", "overall": 89},
    "valverde": {"name": "Federico Valverde", "overall": 89},
    "hakimi": {"name": "Achraf Hakimi", "overall": 89},
    "yamal": {"name": "Lamine Yamal", "overall": 89},
    "kimmich": {"name": "Joshua Kimmich", "overall": 89},
    "mapi leon": {"name": "Mapi León", "overall": 89},
    "griezmann": {"name": "Antoine Griezmann", "overall": 89},
    "ruben dias": {"name": "Rúben Dias", "overall": 89},
    "bruno fernandes": {"name": "Bruno Fernandes", "overall": 89},
    "bernardo silva": {"name": "Bernardo Silva", "overall": 89},
    "osimhen": {"name": "Victor Osimhen", "overall": 89},

    # === Overall 88 ===
    "saka": {"name": "Bukayo Saka", "overall": 88},
    "rice": {"name": "Declan Rice", "overall": 88},
    "odegaard": {"name": "Martin Ødegaard", "overall": 88},
    "wirtz": {"name": "Florian Wirtz", "overall": 88},
    "reiten": {"name": "Guro Reiten", "overall": 88},
    "katoto": {"name": "Marie-Antoinette Katoto", "overall": 88},
    "diani": {"name": "Kadidiatou Diani", "overall": 88},
    "ter stegen": {"name": "Marc-André ter Stegen", "overall": 88},
    "neuer": {"name": "Manuel Neuer", "overall": 88},
    "son": {"name": "Heung Min Son", "overall": 88},
    "musiala": {"name": "Jamal Musiala", "overall": 88},
    "rafael leao": {"name": "Rafael Leão", "overall": 88},
    "araujo": {"name": "Ronald Araújo", "overall": 88},
    "de jong": {"name": "Frenkie de Jong", "overall": 88},
    "paralluelo": {"name": "Salma Paralluelo", "overall": 88},
    "oberdorf": {"name": "Lena Oberdorf", "overall": 88},
    "debora": {"name": "Debinha", "overall": 88},

    # === Overall 87 ===
    "musah": {"name": "Yunus Musah", "overall": 87},
    "theo hernandez": {"name": "Theo Hernández", "overall": 87},
    "marquinhos": {"name": "Marquinhos", "overall": 87},
    "maignan": {"name": "Mike Maignan", "overall": 87},
    "kvaratskhelia": {"name": "Khvicha Kvaratskhelia", "overall": 87},
    "foden": {"name": "Phil Foden", "overall": 87},
    "militao": {"name": "Éder Militão", "overall": 87},
    "barella": {"name": "Nicolò Barella", "overall": 87},
    "grealish": {"name": "Jack Grealish", "overall": 87},
    "rodrygo": {"name": "Rodrygo", "overall": 87},
    "dybala": {"name": "Paulo Dybala", "overall": 87},
    "popp": {"name": "Alexandra Popp", "overall": 87},
    "morgan": {"name": "Alex Morgan", "overall": 87},
    "neymar": {"name": "Neymar Jr.", "overall": 87},
    "pedri": {"name": "Pedri", "overall": 87},

    # === Overall 86 ===
    "tonali": {"name": "Sandro Tonali", "overall": 86},
    "rashford": {"name": "Marcus Rashford", "overall": 86},
    "gvardiol": {"name": "Joško Gvardiol", "overall": 86},
    "gabriel": {"name": "Gabriel Magalhães", "overall": 86},
    "saliba": {"name": "William Saliba", "overall": 86},
    "alexander-arnold": {"name": "Trent Alexander-Arnold", "overall": 86},
    "robertson": {"name": "Andrew Robertson", "overall": 86},
    "gundogan": {"name": "İlkay Gündoğan", "overall": 86},
    "cancelo": {"name": "João Cancelo", "overall": 86},
    "kounde": {"name": "Jules Koundé", "overall": 86},
    "tchouameni": {"name": "Aurélien Tchouaméni", "overall": 86},
    "camavinga": {"name": "Eduardo Camavinga", "overall": 86},
    "nkunku": {"name": "Christopher Nkunku", "overall": 86},
    "diogo jota": {"name": "Diogo Jota", "overall": 86},
    "szoboszlai": {"name": "Dominik Szoboszlai", "overall": 86},
    "bono": {"name": "Bono", "overall": 86},
    "kerr": {"name": "Sam Kerr", "overall": 86},
    "walsh": {"name": "Keira Walsh", "overall": 86},

    # === Overall 85 ===
    "gimenez": {"name": "José María Giménez", "overall": 85},
    "kostic": {"name": "Filip Kostić", "overall": 85},
    "trippier": {"name": "Kieran Trippier", "overall": 85},
    "luis diaz": {"name": "Luis Díaz", "overall": 85},
    "diaby": {"name": "Moussa Diaby", "overall": 85},
    "coman": {"name": "Kingsley Coman", "overall": 85},
    "cristiano ronaldo": {"name": "Cristiano Ronaldo", "overall": 85},
    "gavi": {"name": "Gavi", "overall": 85},
    "alaba": {"name": "David Alaba", "overall": 85},
    "bremer": {"name": "Bremer", "overall": 85},
    "vlahovic": {"name": "Dušan Vlahović", "overall": 85},
    "darwin nunez": {"name": "Darwin Núñez", "overall": 85},
    "isak": {"name": "Alexander Isak", "overall": 85},
    "bruno guimaraes": {"name": "Bruno Guimarães", "overall": 85},
    "julian alvarez": {"name": "Julián Álvarez", "overall": 85},
}

# Adicionar URLs de imagem a cada jogador
for key in PLAYERS_DB:
    PLAYERS_DB[key]["image_url"] = get_player_image_url(key)
    PLAYERS_DB[key]["card_bg_url"] = CARD_BACKGROUND_URL

# --- Normalização e Busca ---
PLAYERS_BY_NAME_DB = {v["name"]: v for k, v in PLAYERS_DB.items()}

# --- Inicialização do FastAPI ---
app = FastAPI()

# --- Configuração do CORS ---
origins = [
    "http://localhost",
    "http://localhost:8501", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic ---
class ComparacaoRequest(BaseModel):
    jogador_a_nome: str
    jogador_b_input: str # Esta é a CHAVE (ex: "vini jr")

# --- Endpoints da API ---

@app.get("/jogador_aleatorio")
def get_jogador_aleatorio():
    """
    Sorteia e retorna um jogador aleatório do banco de dados.
    Agora inclui URLs de imagens.
    """
    nome_chave, dados = random.choice(list(PLAYERS_DB.items()))
    return dados

@app.post("/comparar")
def post_comparar(request: ComparacaoRequest):
    """
    Compara o palpite do usuário (jogador_b_input) com o jogador atual (jogador_a_nome).
    Agora inclui URLs de imagens nas respostas.
    """
    jogador_a_nome = request.jogador_a_nome
    jogador_b_input_chave = request.jogador_b_input 

    # 1. Busca o Jogador B (palpite) pela chave
    jogador_b_dados = PLAYERS_DB.get(jogador_b_input_chave)
    
    if not jogador_b_dados:
        return {"resultado": "nao_encontrado", "palpite": request.jogador_b_input}

    # 2. Busca o Jogador A (atual) pelo nome exato
    jogador_a_dados = PLAYERS_BY_NAME_DB.get(jogador_a_nome)
    
    if not jogador_a_dados:
        return {"resultado": "erro_jogador_a_nao_encontrado"}

    # 3. Compara os Overalls
    overall_a = jogador_a_dados["overall"]
    overall_b = jogador_b_dados["overall"]

    if overall_b > overall_a:
        resultado = "correto"
    elif overall_b == overall_a:
        resultado = "empate"
    else:
        resultado = "incorreto"
    
    # 4. Gera um novo jogador aleatório para a próxima rodada
    novo_jogador = random.choice(list(PLAYERS_DB.values()))
        
    return {
        "resultado": resultado,
        "jogador_a": jogador_a_dados,
        "jogador_b": jogador_b_dados,
        "proximo_jogador": novo_jogador,
    }

@app.get("/jogadores_nomes")
def get_jogadores_nomes():
    """
    Retorna um dicionário mapeando a CHAVE (ex: "vini jr") 
    para o NOME DE EXIBIÇÃO (ex: "Vini Jr.").
    """
    nomes_map = {key: data["name"] for key, data in PLAYERS_DB.items()}
    return nomes_map

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
