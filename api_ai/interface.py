from google import genai
import fitz

#Abertura da Conversa
print("Olá, sou o Justinho! Irei ajudá-lo a criar sua petição de defesa!")
print("Primeiro, irei perguntar algumas de suas informações")

#Informações Pessoais
while True:
    nome = input("Para começar, insira o seu nome completo: ")
    clube = input("Agora, o clube ao qual estava jogando quando houve a acusação: ")
    competicao = input("Por fim, a competição em que estava competindo quando houve a acusação: ")
    
    print(f"\nSuas informações foram as seguintes: \nNome - {nome}\nClube - {clube}\nCompetição - {competicao}")
    confirmacao = input("Essas informações estão corretas? (S/N): ")

    if(confirmacao == "S"):
        break
    else:
        print("Certo, vamos começar novamente!\n")

#Acusação
print("\nAgora, vamos conversar sobre sua acusação.")
while True:
    acusacao = input("Insira sua acusação: ")
    print("Escreva todo o contexto da situação. Seja detalhista e insira fatos que gostaria de destacar.")
    contexto = input("Escreva o contexto: ")

    print(f"\nA acusação e o contexto foram os seguintes: \nAcusação - {acusacao}\nContexto dado - {contexto}")
    confirmacao = input("Essas informações estão corretas? (S/N): ")

    if(confirmacao == "S"):
        break
    else:
        print("Vamos recolher as informações novamente!\n")

#Defesa
print("\nPor fim, vamos conversar sobre sua defesa.")
while True:
    print("Me fale agora o que você deseja alcançar com essa defesa (arquivamento da denúncia, desclassificação da conduta, ser ouvido pessoalmente, etc...)")
    pedidos = input("Escreva o que deseja alcançar por meio dessa defesa: ")

    print(f"\nO seus pedidos são os seguintes: \nDefesa - {pedidos}")
    confirmacao = input("Essas informações estão corretas? (S/N): ")

    if(confirmacao == "S"):
        break
    else:
        print("Vamos recolher as informações novamente!\n")

print("\nObrigado pelas informações! Agora irei gerar o documento.")

# Abrir o PDF e extrair texto
def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# Carregar o conteúdo do PDF
conteudo_pdf = extrair_texto_pdf("Defesa.pdf")

#Prompt
prompt = f"""
Atue como um advogado experiente em Direito Desportivo no Brasil. Elabore uma petição de defesa com linguagem técnica e estrutura formal.
Utilize argumentos baseados no Código Brasileiro de Justiça Desportiva (CBJD) e nos princípios do direito processual desportivo. 
Apresente a petição de forma compatível com o protocolo em Tribunais de Justiça Desportiva. 

Utilize o seguinte texto como base: {conteudo_pdf}

As informações do cliente são as seguintes:
Nome = {nome}
Clube = {clube}
Competição = {competicao}
Acussação = {acusacao}
Contexto = {contexto}
Defesa = {pedidos}
"""

print("Aguarde...")

#API Gemini
client = genai.Client(api_key="AIzaSyCAgvlIKULzL6ZepH3ZH6fqJvw6eZeZaPQ")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

#Criação do Arquivo
filename = "peticao_defesa.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(response.text)

print("\nArquivo Criado")