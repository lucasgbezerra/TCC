import re
import os
import json

raiz = '/home/lucas/tcc'
dirProjeto = f'{raiz}/reps/zaproxy/zap/src'
dirMetodos = f'{raiz}/metodos'
lstClasses = []

def buscaClasse():
    count = 0
    for pasta_raiz, sub_pastas, arquivos in os.walk(dirProjeto):
        for arquivo in arquivos:
            if arquivo.endswith(".java") and not "test" in arquivo.lower():
                lstClasses.append({'classe': '','path': '','testePath': '', 'metodos': []})
                lstClasses[count]['classe'] = arquivo.removesuffix('.java')
                lstClasses[count]['path'] = os.path.join(pasta_raiz, arquivo)
                count += 1

        
    for classe in lstClasses:
        arquivoJava = classe['classe'] + ".java"
        for pasta_raiz, sub_pastas, arquivos in os.walk(dirProjeto):
            if arquivoJava in arquivos:
                classe['path'] = os.path.join(pasta_raiz, arquivoJava)
 
def buscaTeste():
    for pasta_raiz, sub_pastas, arquivos in os.walk(dirProjeto):
        for arquivo in arquivos:
            if arquivo.endswith(".java") and "test" in arquivo.lower():
                for classe in lstClasses:
                    if arquivo.startswith(classe['classe']):
                        classe['testePath'] = os.path.join(pasta_raiz, arquivo)
                        break

def removeClassesSemCaminho():
    novaLista = []
    for classe in lstClasses:
        if classe['testePath'] != '' and classe['path'] != '':
            novaLista.append(classe)
        if len(novaLista) == 10:
            break

    return novaLista

# def extraiMetodo(classe, arquivo_path, metodos):
#     with open(arquivo_path, 'r') as arquivo:
#         arquivoTexto = arquivo.readlines()

#     metodo_atual = None
#     corpo_metodo = ""
#     metodo_encontrado = False
#     numChavesAbertas = 0
#     padraoMetodo = re.compile(r'(?:(?:public|private|protected|static)\s+)+[\w\<\>\[\]]*\s*(\w+)\s*\([^\)]*\)\s*[^\{}]*{')

#     for line in arquivoTexto:
#         match =  padraoMetodo.search(line)
#         if match:
#             print(match.group(1) + "=====")
#             if match.group(1) in metodos:
#                 metodo_atual = match.group(1)
#                 metodo_encontrado = True
#                 corpo_metodo = ""
#                 numChavesAbertas = 0
                

#         if metodo_encontrado:
#             corpo_metodo += line
#             print(metodo_atual + "-------" + numChavesAbertas.__str__())

#             numChavesAbertas += line.count("{")
#             numChavesAbertas -= line.count("}")
            
#             if numChavesAbertas == 0:
#                 for metodo in metodos:
#                     if metodo == metodo_atual:
#                         criaArquivo(metodo, corpo_metodo, "java", dirMetodos, classe)
#                         metodo_encontrado = False
#                         break


def criaArquivo(nome, conteudo,extensao, dir, subDir=""):
    dir = os.path.join(dir, f"{dir}/{subDir}")

    if not os.path.exists(dir):
        os.makedirs(dir)
    arquivoMetodo = os.path.join(dir, f"{nome}.{extensao}")
    with open(arquivoMetodo, 'w') as arquivoSaida:
        arquivoSaida.write(conteudo)
        arquivoSaida.write("\n")

def armazenaMetodo(lista):
    for indice, classe in enumerate(lista, start=0):
        metodos = []
        if not os.path.exists(classe['path']):
            print(f"O arquivoTexto não existe.")
            return
        
        #melhorar a regex
        padraoMetodo = re.compile(r'(?:(?:public|private|protected|static)\s+)+[\w\<\>\[\]]*\s*(\w+)\s*\([^\)]*\)\s*[^\{}]*{')

        with open(classe['path'], 'r') as arquivo:
            arquivoTexto = arquivo.readlines()

        for line in arquivoTexto:
            match = padraoMetodo.search(line)
            if match:
                assMetodo = match.group(1)
                if not metodos.__contains__(assMetodo ) and len(assMetodo) > 1:
                    metodos.append(assMetodo)

        padraoTeste = r'\b(\w+)\.(\w+)\s*\([^)]*\)'
        with open(classe['testePath'], 'r') as f:
            linhas = f.readlines()
            for linha in linhas:
                match = re.search(padraoTeste, linha)
                if match:
                    instancia = match.group(1)
                    metodo = match.group(2)
                    if metodo in metodos and metodo not in classe['metodos']:
                        classe['metodos'].append(metodo)
        
        lista[indice]['metodos'] = classe['metodos']
        # extraiMetodo(classe["classe"], classe['path'], classe['metodos'])

def armazenaInfos(listaReduzida):
    jsonData = json.dumps(listaReduzida)
    criaArquivo("infos", jsonData, "json", raiz)

def main():        
    buscaClasse()
    buscaTeste()
    listaReduzida = removeClassesSemCaminho()
    armazenaMetodo(listaReduzida)
    for classe in listaReduzida:
        print(classe['classe'])
        print("PATH:" + classe['path'])
        print("TESTE: " + classe['testePath'])
        print(classe['metodos'])
        print("\n")
    print(len(listaReduzida))
    armazenaInfos(listaReduzida)


if __name__ == "__main__":
    main()