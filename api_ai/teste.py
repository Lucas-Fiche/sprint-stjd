from google import genai

while True:
    num = input("Digite 1 se desejar usar as informações predefinidas e 2 se quiser muda-las: ")

    if int(num) == 1:
        nome = "João da Silva"
        atividade = "Jogador profissional de futebol, inscrito na Série B do Campeonato Brasileiro"
        acusacao = "Suposto uso de substância proibida (doping) detectado após partida oficial"
        print("Aguarde...")
        break
    elif int(num) == 2:
        nome = input("Escreva o nome do cliente: ")
        atividade = input("Escreva a atividade que o cliente exerce: ")
        acusacao = input("Escreva a acusação que o cliente está sofrendo: ")
        print("Aguarde...")
        break
    else:
        print("Digite um número válido.\n")

prompt = f"""
Atue como um advogado experiente em Direito Desportivo no Brasil. Elabore uma petição de defesa com linguagem técnica e estrutura formal.

Cliente:
Nome: {nome}
Atividade: {atividade}
Acusação: {acusacao}

Utilize argumentos baseados no Código Brasileiro de Justiça Desportiva (CBJD) e nos princípios do direito processual desportivo. Apresente a petição de forma compatível com o protocolo em Tribunais de Justiça Desportiva.
"""

client = genai.Client(api_key="AIzaSyCAgvlIKULzL6ZepH3ZH6fqJvw6eZeZaPQ")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

filename = "peticao_defesa.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(response.text)

print("\nArquivo Criado")