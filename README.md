# Apito Legal - Gerador de Petições com IA

Sistema de assistência jurídica desportiva com gerador automático de petições usando Inteligência Artificial.

## 🤖 Funcionalidades

- Geração automática de petições de defesa usando IA (Gemini)
- Sistema de assistência jurídica para atletas e clubes
- Interface web responsiva com Flask
- Páginas informativas sobre Direito Desportivo

## 🚀 Como Executar

1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Configure API key do Gemini no `config.py`
6. Execute: `python app.py`
7. Acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

apito_legal/
├── app.py                  # Aplicação principal Flask
├── config.py              # Configurações
├── peticao_service.py      # Serviço de IA
├── requirements.txt        # Dependências
├── static/                 # Arquivos estáticos
└── templates/              # Templates HTML

## 🔧 Tecnologias

- Flask
- Google Gemini AI
- HTML/CSS/JavaScript
- Python

## 📄 Licença

Este projeto está sob licença MIT.