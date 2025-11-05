# ⚽ OverallFC - Jogo do Maior Overall

Um jogo interativo onde você testa seus conhecimentos sobre os jogadores do EA FC 26! Adivinhe qual jogador tem o Overall maior e acumule pontos.

![Python](https://img.shields.io/badge/Python-3.11-blue)![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)

📋 Sobre o Projeto

OverallFC é um jogo divertido que desafia você a comparar jogadores do EA FC 26 baseado em seus atributos Overall. O jogo apresenta imagens reais dos jogadores e oferece uma experiência visual moderna e responsiva.

### ✨ Funcionalidades

- 🎮 **Jogo Interativo**: Compare jogadores e acumule pontos

- 🖼️ **Imagens Reais**: Fotos dos jogadores integradas via FUTBIN

- 🎲 **Jogadores Aleatórios**: Cada rodada apresenta um jogador diferente

- 🤝 **Sistema de Empate**: Empates mantêm sua streak sem perder pontos

- 📊 **Feedback Visual**: Boxes coloridos mostram se você acertou, errou ou empatou

- 🏆 **Sistema de Pontuação**: Acompanhe seu progresso e tente bater seu recorde

- 🎨 **Interface Moderna**: Design responsivo com gradientes e animações

## 🎯 Como Jogar

1. Um jogador aleatório é apresentado com seu Overall oculto

1. Escolha outro jogador que você acha que tem Overall **maior**

1. Veja o resultado:
  - ✅ **Acertou?** Ganhe +1 ponto e continue jogando
  - 🤝 **Empatou?** Mantenha sua streak e continue
  - ❌ **Errou?** Fim de jogo! Tente novamente

## 🚀 Tecnologias Utilizadas

### Backend

- **FastAPI** - Framework web moderno e rápido

- **Uvicorn** - Servidor ASGI de alta performance

- **Python 3.11** - Linguagem de programação

### Frontend

- **Streamlit** - Framework para aplicações web interativas

- **Requests** - Biblioteca para requisições HTTP

### Dados

- **100 Jogadores** do EA FC 26 (Overalls 85-91)

- **Imagens via FUTBIN** - CDN de imagens dos jogadores

## 📦 Instalação

### Pré-requisitos

- Python 3.11 ou superior

- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/pgmoreiraa/OverallFC.git
cd OverallFC/FC
```

1. **Instale as dependências**

```bash
pip install -r requirements.txt
```

1. **Inicie o servidor (Terminal 1)**

```bash
cd server/app
python main.py
```

1. **Inicie o cliente (Terminal 2)**

```bash
cd client
streamlit run main.py
```

1. **Acesse o jogo**

```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
OverallFC/
├── FC/
│   ├── server/
│   │   └── app/
│   │       ├── __init__.py
│   │       └── main.py          # API FastAPI
│   ├── client/
│   │   └── main.py              # Interface Streamlit
│   ├── requirements.txt         # Dependências do projeto
│   ├── README.md               # Documentação
│   └── .gitignore              # Arquivos ignorados
└── README.md                    # Este arquivo
```

### Tela Principal

Interface moderna com foto do jogador e sistema de seleção.

### Resultado - Acerto

Box verde indicando acerto com comparação de Overalls.

### Resultado - Empate

Box rosa indicando empate e manutenção da streak.

### Game Over

Tela de fim de jogo com pontuação final e mensagem motivacional.

## 🔧 Configuração

### Servidor (FastAPI)

- **Porta:** 8000

- **Host:** 127.0.0.1

- **Reload:** Automático em desenvolvimento

### Cliente (Streamlit)

- **Porta:** 8501

- **Modo:** Headless (produção)

## 📊 Banco de Dados

O projeto utiliza um dicionário Python com 100 jogadores do EA FC 26:

- **Overalls:** 85 a 91

- **Dados:** Nome, Overall, URLs de imagens

- **Fonte:** FUTBIN (imagens)

### Distribuição de Jogadores por Overall

| Overall | Quantidade |
| --- | --- |
| 91 | 6 |
| 90 | 8 |
| 89 | 16 |
| 88 | 17 |
| 87 | 15 |
| 86 | 18 |
| 85 | 15 |

## 📝 Ideias para Futuras Melhorias

- [ ] Sistema de ranking/leaderboard

- [ ] Modo multiplayer

- [ ] Diferentes níveis de dificuldade

- [ ] Sistema de conquistas/badges

- [ ] Animações de transição entre cartas

- [ ] Efeitos sonoros

- [ ] Modo escuro/claro

- [ ] Cache de imagens para melhor performance

- [ ] Deploy em produção (Heroku, Railway, Vercel)

- [ ] Adicionar mais jogadores

## 👤 Autor

**Paulo Moreira**

- GitHub: [@pgmoreiraa](https://github.com/pgmoreiraa)

- Projeto: [OverallFC](https://github.com/pgmoreiraa/OverallFC)

## 🙏 Agradecimentos

- **FUTBIN** - Pelas imagens dos jogadores

- **EA Sports** - Pelos dados do EA FC 26

- **Comunidade Python** - Pelas excelentes bibliotecas

---

**⭐ Se você gostou do projeto, não esqueça de dar uma estrela!**

Feito com ❤️ e ⚽ por Paulo Moreira
