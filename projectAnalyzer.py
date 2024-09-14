import re
import os
import json
import random

raiz = ''
dirMetodos = '/home/lucas/tcc/metodos'

classesTeste = []

def getClass(project, dir):
    lstInfoClass = []
    lstInfoClass.append({'project': project, 'classes': []})
    count = 0
    for sourceDir, subDir, files in os.walk(dir):
        for file in files:
            if file.endswith(".java") and not "test" in file.lower() and not "test" in sourceDir.lower():
                # Verifica se a classe é uma interface
                filePath = os.path.join(sourceDir, file)
                className = file.removesuffix('.java')
                with open(filePath, 'r') as javaFile:
                    fileContent = javaFile.read()
                    if f"interface {className}" in fileContent:
                        print(f"Ignoring interface: {filePath}")
                        continue  # Ignora interfaces

                lstInfoClass[-1]['classes'].append({'name': '','testName': '','classPath': '','testPath': '', 'methods': []})
                lstInfoClass[-1]['classes'][count]['name'] = className
                lstInfoClass[-1]['classes'][count]['classPath'] = filePath
                count += 1

    
    return lstInfoClass
 
def findTestFileForClass(lstClass, dir):

    for classe in lstClass[-1]['classes']:
        for sourceDir, subDir, files in os.walk(dir):
            for file in files:
                if file.endswith(".java") and "test" in file.lower():
                    if file.startswith(classe['name']):
                        classe['testPath'] = os.path.join(sourceDir, file)
                        classe['testName'] = file.removesuffix('.java')
                        classesTeste.append(classe)
                        break
        
        if classe['testPath'] == '':
            classe['testPath'] = classe['classPath'].replace("main", "test").replace(".java", "Test.java")
            classe['testName'] = classe['name'] + "Test"

def removeClassIfNotTested(lstClass):
    newLstClass = []
    # newLstClass.append({'name': '','classPath': '','testePath': '', 'methods': []})
    for c in lstClass:
        if c['testPath'] != '' and c['classPath'] != '':
            newLstClass.append(c)
        # if len(newLstClass) == 10:
        #     break

    return newLstClass

def createFile(nome, conteudo,extensao, dir, subDir=""):
    dir = os.path.join(dir, f"{dir}/{subDir}")

    if not os.path.exists(dir):
        os.makedirs(dir)
    arquivoMetodo = os.path.join(dir, f"{nome}.{extensao}")
    with open(arquivoMetodo, 'a') as arquivoSaida:
        arquivoSaida.write(conteudo)
        arquivoSaida.write("\n")

def extractMethodSignatures(class_list):
    for index, class_info in enumerate(class_list, start=0):
        method_names = []
        if not os.path.exists(class_info['classPath']):
            print(f"The file does not exist.")
            return
        
        with open(class_info['classPath'], 'r') as class_file:
            class_file_lines = class_file.readlines()

        # Regex pattern to extract method signatures
        method_pattern = re.compile(r'(?:(?:public|private|protected|static)\s+)+[\w\<\>\[\]]*\s*(\w+)\s*\([^\)]*\)\s*[^\{}]*{')

        for line in class_file_lines:
            match = method_pattern.search(line)
            if match:
                method_signature = match.group(1)
                if method_signature not in method_names and len(method_signature) > 1:
                    method_names.append(method_signature)
        
        class_list[index]['methods'] = method_names

    return class_list

def selectRandomClasses(dataList, numElements=5, seed=42):
    # Check if numElements is greater than the length of the list
    if numElements > len(dataList):
        raise ValueError("Number of elements to select cannot be greater than the length of the list.")
    
    # Select random elements
    selectedElements = random.sample(dataList, numElements)
    
    return selectedElements


def saveInfo(classList, name, path):
    jsonData = json.dumps(classList)
    createFile(name, jsonData, "json", path)

def getProjectsInfos(filePath):
    with open(filePath, 'r') as arquivo:
        return json.load(arquivo)
    
def main():
    projects = getProjectsInfos("/home/lucas/tcc/projectsInfos.json")

    allProjectsInfo = []
    for project in projects:
        projectList = []
        projectList = getClass(project['name'], f"{project['source']}/zap/src/main")
        print("findTestFileForClass")
        findTestFileForClass(projectList, project['source'])
        # print("removeClassIfNotTested")
        # projectList[-1]['classes'] = removeClassIfNotTested(projectList[-1]['classes'])
        print("extractMethodSignatures")
        projectList[-1]['classes'] = extractMethodSignatures(projectList[-1]['classes'])
        projectList[-1]['classes'] = selectRandomClasses(projectList[-1]['classes'])
        print(len(projectList[-1]['classes']))
        # for c in classList:
        #     print(c['classes'])
        #     print(c['project'])
        # print(len(classList))
        allProjectsInfo.append(projectList[-1])
    saveInfo(allProjectsInfo, "infos", "/home/lucas/tcc/")


if __name__ == "__main__":
    main()