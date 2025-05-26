from google import genai
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from fpdf import FPDF
import fitz
import os
from flask import current_app

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF"""
    try:
        doc = fitz.open(caminho_pdf)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
        return texto
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

def gerar_peticao(dados_cliente):
    """Gera petição usando IA do Gemini"""
    try:
        # Caminho para o PDF de referência
        caminho_pdf = os.path.join('static', 'documentos', 'Defesa.pdf')
        
        # Verifica se o arquivo PDF existe
        if os.path.exists(caminho_pdf):
            conteudo_pdf = extrair_texto_pdf(caminho_pdf)
        else:
            conteudo_pdf = "PDF de referência não encontrado. Utilize conhecimento jurídico padrão."
        
        # Prompt para o Gemini
        prompt = f"""
        Atue como um advogado experiente em Direito Desportivo no Brasil. Elabore uma petição de defesa com linguagem técnica e estrutura formal.
        Utilize argumentos baseados no Código Brasileiro de Justiça Desportiva (CBJD) e nos princípios do direito processual desportivo. 
        Apresente a petição de forma compatível com o protocolo em Tribunais de Justiça Desportiva. 
        Não invente dados. Não preencha campos que devem ser completados posteriormente. 
        Utilize marcações claras para que o usuário identifique os trechos editáveis.

        Utilize o seguinte modelo como base estrutural e de formatação: {conteudo_pdf}

        As informações do cliente são as seguintes:
        Nome: {dados_cliente['nome']}
        Clube: {dados_cliente['clube']}
        Competição: {dados_cliente['competicao']}
        Acusação: {dados_cliente['acusacao']}
        Contexto: {dados_cliente['contexto']}
        Objetivos da Defesa: {dados_cliente['pedidos']}
        
        Estruture a petição com:
        1. Cabeçalho identificando o tribunal
        2. Qualificação das partes
        3. Dos fatos
        4. Do direito
        5. Dos pedidos
        6. Requerimentos finais
        """
        
        # Configurar cliente Gemini
        client = genai.Client(api_key=current_app.config['GEMINI_API_KEY'])
        
        # Gerar conteúdo
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        return {
            'sucesso': True,
            'conteudo': response.text,
            'nome_arquivo': f"peticao_{dados_cliente['nome'].replace(' ', '_').lower()}"
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'erro': str(e),
            'conteudo': None
        }

def limpar_unicode_para_pdf(texto):
    """Substitui caracteres especiais não suportados pelo FPDF (latin-1)"""
    substituicoes = {
        "–": "-",   # travessão
        "—": "-",   # travessão longo
        "“": '"',   # aspas esquerda
        "”": '"',   # aspas direita
        "‘": "'",   # apóstrofo esquerdo
        "’": "'",   # apóstrofo direito
        "•": "-",   # ponto de lista
        "…": "...", # reticências
        "→": "->",  # seta
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "ç": "c", "Ç": "C",
        "ã": "a", "õ": "o", "Ã": "A", "Õ": "O"
    }

    for char, repl in substituicoes.items():
        texto = texto.replace(char, repl)
    return texto

def salvar_peticao(conteudo, nome_base):
    """Salva a petição em .docx e .pdf com formatação"""
    try:
        pasta_peticoes = os.path.join('static', 'peticoes')
        os.makedirs(pasta_peticoes, exist_ok=True)

        # === DOCX formatado ===
        caminho_docx = os.path.join(pasta_peticoes, f"{nome_base}.docx")
        doc = Document()

        # Definições de fonte padrão
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)

        # Processamento de parágrafos
        for paragrafo in conteudo.strip().split('\n\n'):
            texto = paragrafo.strip()

            # Remover marcadores de formatação
            texto = texto.replace('**', '')

            # Criar parágrafo no documento
            p = doc.add_paragraph(texto)

            # Centralizar se for título (heurística simples)
            if texto.isupper() or texto.startswith("I – ") or texto.startswith("II – ") or texto.startswith("III – "):
                p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                for run in p.runs:
                    run.bold = True
            elif texto.startswith("Termos em que") or texto.startswith("Pede deferimento"):
                p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                for run in p.runs:
                    run.bold = True
            else:
                p.paragraph_format.space_after = Pt(12)
                p.paragraph_format.first_line_indent = Pt(24)
                p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        doc.save(caminho_docx)

        # === PDF ===
        caminho_pdf = os.path.join(pasta_peticoes, f"{nome_base}.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Limpa e escreve o conteúdo
        conteudo_pdf = limpar_unicode_para_pdf(conteudo)
        for linha in conteudo_pdf.strip().split('\n'):
            pdf.multi_cell(0, 10, linha.strip())

        pdf.output(caminho_pdf)

        return {
            'sucesso': True,
            'arquivos': {
                'docx': f"{nome_base}.docx",
                'pdf': f"{nome_base}.pdf"
            }
        }

    except Exception as e:
        print(f"[ERRO salvar_peticao] {e}")
        return {
            'sucesso': False,
            'erro': str(e)
        }