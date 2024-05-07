from openai import OpenAI
from dotenv import dotenv_values
import os
import json

env_vars = dotenv_values(".env")
key = env_vars.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=key
)

def enviar(texto):

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": texto},
    ]
    )

    return completion.choices[0].message


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read()

def main():
    nome_arquivo = 'arquivo.txt'  # Substitua pelo caminho do seu arquivo
    texto = ler_arquivo(nome_arquivo)
    resposta_gpt = enviar(texto)
    print(resposta_gpt)

if __name__ == "__main__":
    main()
