from openai import OpenAI
from dotenv import dotenv_values
import os
import json
import re

env_vars = dotenv_values(".env")
KEY = env_vars.get("OPENAI_API_KEY")
PROJECT_ID = env_vars.get("PROJECT_ID")
client = OpenAI(
    api_key=KEY,
    organization='org-hb4V3o4P9oJnavCMtYL4yWDi',
    project=PROJECT_ID,
)


raiz = "/home/lucas/tcc"

def createFile():
    with open('arquivo.txt', 'w') as f:
        f.write("Olá, tudo bem?")

def getOpenAiResponse(prompt):

    response = client.chat.completions.create(    
        model="gpt-3.5-turbo",
        messages=[
         {"role": "user", "content": prompt},
        ],)

    return response.choices[0].message.content


def readFile(nome):
    with open(nome, 'r') as f:
        return f.read()

def readJson(nome):
    with open(nome, 'r') as f:
        return json.load(f)

def writeFile(fileName, content):
    try:
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print("Erro: " + e)

def readClass(filename):
    result = ""
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip().startswith(('*', '/')):
                result += line
    return result

def extractCode(response_text):
    # Expressão regular para extrair blocos de código Java
    java_code_pattern = re.compile(r'```java(.*?)```', re.DOTALL)
    java_code_blocks = java_code_pattern.findall(response_text)
    return "\n\n".join(java_code_blocks)


def main():
    template = readFile('template.txt')
    infos = readJson('infos.json')
    count = 0
    # while count < len(infos):
    while count < 1:
        for item in infos:
            # Escolhendo as melhores classes
            classe = readClass(f"{item['path']}")
            if len(classe.splitlines())/len(item['metodos']) < 30:
                template = template.replace('CLASS_NAME', item['classe'])
                template = template.replace('METHOD_NAME', ', '.join(item['metodos']))
                prompt = f'{classe}\n\n{template}'
                response = getOpenAiResponse(prompt)
                javaCode = extractCode(response)
                writeFile(f"{raiz}/responses/{item['classe']}Teste.java", javaCode)
                break
        count +=1
if __name__ == "__main__":
    main()
