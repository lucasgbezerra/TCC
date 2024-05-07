import re
import os

raiz = '/home/lucas/tcc'
caminhoProjeto = f'{raiz}/zaproxy/zap/src'
lstClasses = []
lstClasseReduzida = []

def buscaClasse():
    count = 0
    for pasta_raiz, sub_pastas, arquivos in os.walk(caminhoProjeto):
        for arquivo in arquivos:
            if arquivo.endswith(".java") and not "test" in arquivo.lower():
                lstClasses.append({'classe': '','path': '','testePath': '', 'metodos': []})
                lstClasses[count]['classe'] = arquivo.removesuffix('.java')
                lstClasses[count]['path'] = os.path.join(pasta_raiz, arquivo)
                count += 1

        
    for classe in lstClasses:
        arquivoJava = classe['classe'] + ".java"
        for pasta_raiz, sub_pastas, arquivos in os.walk(caminhoProjeto):
            if arquivoJava in arquivos:
                classe['path'] = os.path.join(pasta_raiz, arquivoJava)
 
def buscaTeste():
    for pasta_raiz, sub_pastas, arquivos in os.walk(caminhoProjeto):
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

def buscaMetodo():
    ...

def armazenaMetodo(lista):
    for classe in lista:
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
                    metodos.append({"assinatura": assMetodo, "corpo": corpoMetodo})

        padraoTeste = r'\b(\w+)\.(\w+)\s*\([^)]*\)'
        print(classe['classe'])
        print(metodos
              )
        with open(classe['testePath'], 'r') as f:
            linhas = f.readlines()
            for linha in linhas:
                match = re.search(padraoTeste, linha)
                if match:
                    instancia = match.group(1)
                    metodo = match.group(2)
                    print("---"+ metodo + "---")
                    if metodo in metodos and metodo not in classe['metodos']:
                        classe['metodos'].append(metodo)
def main():        
    buscaClasse()
    buscaTeste()
    lstClasses = removeClassesSemCaminho()
    armazenaMetodo(lstClasses)
    for classe in lstClasses:
        print(classe['classe'])
        print("PATH:" + classe['path'])
        print("TESTE: " + classe['testePath'])
        print(classe['metodos'])
        print("\n")
    print(len(lstClasses))

    


if __name__ == "__main__":
    main()