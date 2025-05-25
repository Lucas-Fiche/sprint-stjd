from google import genai
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

        Utilize o seguinte texto como base: {conteudo_pdf}

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
            'nome_arquivo': f"peticao_{dados_cliente['nome'].replace(' ', '_').lower()}.txt"
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'erro': str(e),
            'conteudo': None
        }

def salvar_peticao(conteudo, nome_arquivo):
    """Salva a petição em arquivo"""
    try:
        # Criar diretório se não existir
        pasta_peticoes = os.path.join('static', 'peticoes')
        os.makedirs(pasta_peticoes, exist_ok=True)
        
        # Salvar arquivo
        caminho_completo = os.path.join(pasta_peticoes, nome_arquivo)
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        
        return {
            'sucesso': True,
            'caminho': caminho_completo,
            'nome_arquivo': nome_arquivo
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'erro': str(e)
        }