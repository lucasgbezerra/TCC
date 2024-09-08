import re
import os
import json
import random

raiz = ''
dirMetodos = '/home/lucas/tcc/metodos'

def getClass(project, dir):
    lstInfoClass = []
    lstInfoClass.append({'project': project, 'classes': []})
    count = 0
    for sourceDir, subDir, files in os.walk(dir):
        for file in files:
            if file.endswith(".java") and not "test" in file.lower() and not "test" in sourceDir.lower():
                lstInfoClass[-1]['classes'].append({'name': '','classPath': '','testPath': '', 'methods': []})
                lstInfoClass[-1]['classes'][count]['name'] = file.removesuffix('.java')
                lstInfoClass[-1]['classes'][count]['classPath'] = os.path.join(sourceDir, file)
                count += 1

        
    # for classInfo in lstInfoClass:
    #     javaFile = classInfo['name'] + ".java"
    #     for sourceDir, subDir, files in os.walk(dir):
    #         if javaFile in files:
    #             classInfo['classPath'] = os.path.join(sourceDir, javaFile)
    
    return lstInfoClass
 
def findTestFileForClass(lstClass, dir):

    for classe in lstClass[-1]['classes']:
        for sourceDir, subDir, files in os.walk(dir):
            for file in files:
                if file.endswith(".java") and "test" in file.lower():
                    if file.startswith(classe['name']):
                        classe['testPath'] = os.path.join(sourceDir, file)
                        break
        
        classe['testPath'] = classe['classPath'].replace("main", "test").replace(".java", "Test.java")

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
        
        # Improve the regex
        method_pattern = re.compile(r'(?:(?:public|private|protected|static)\s+)+[\w\<\>\[\]]*\s*(\w+)\s*\([^\)]*\)\s*[^\{}]*{')

        with open(class_info['classPath'], 'r') as class_file:
            class_file_lines = class_file.readlines()
        for line in class_file_lines:
            match = method_pattern.search(line)
            if match:
                method_signature = match.group(1)
                if method_signature not in method_names and len(method_signature) > 1:
                    method_names.append(method_signature)

        # test_pattern = re.compile(r'\b(\w+)\.(\w+)\s*\([^)]*\)(.*)')
        # with open(class_info['testPath'], 'r') as test_file:
        #     test_file_lines = test_file.readlines()
        #     for test_line in test_file_lines:
        #         match = re.search(test_pattern, test_line)
        #         if match:
        #             instance_name = match.group(1)
        #             method_name = match.group(2)
        #             complement = match.group(3)

        #             if method_name in method_names and method_name not in class_info['methods']:
        #                 class_info['methods'].append(method_name)
        #             elif complement.startswith('.'):
        #                 for method in method_names:
        #                     if method in complement and method not in class_info['methods']:
        #                         class_info['methods'].append(method)
        #                         break

        
        class_list[index]['methods'] = method_names

    return class_list

def randonlyPickClass(classes):
    filtersClasses = [c for c in classes if len(c['methods']) > 0]
    totalMethods = 0
    selectedClasses = []
    while totalMethods < 200 and len(filtersClasses) > 0:
        selectedClass = random.choice(filtersClasses)
        selectedClasses.append(selectedClass)
        totalMethods += len(selectedClass['methods'])
        filtersClasses.remove(selectedClass)
    
    print(len(selectedClasses))
    return selectedClasses


def saveInfo(classList, name, path):
    jsonData = json.dumps(classList)
    createFile(name, jsonData, "json", path)

def getProjectsInfos(filePath):
    with open(filePath, 'r') as arquivo:
        return json.load(arquivo)
    
def main():
    projects = getProjectsInfos("/home/lucas/tcc/projectsInfos.json")
    # json = [{"name": "nameProject", "source": "source/nameProject", "gradlew": boolean},]
    allProjectsInfo = []
    for project in projects:
        projectList = []
        projectList = getClass(project['name'], project['source'])
        print("findTestFileForClass")
        findTestFileForClass(projectList, project['source'])
        # print("removeClassIfNotTested")
        # projectList[-1]['classes'] = removeClassIfNotTested(projectList[-1]['classes'])
        print("extractMethodSignatures")
        projectList[-1]['classes'] = extractMethodSignatures(projectList[-1]['classes'])
        projectList[-1]['classes'] = randonlyPickClass(projectList[-1]['classes'])
        print(len(projectList[-1]['classes']))
        # for c in classList:
        #     print(c['classes'])
        #     print(c['project'])
        # print(len(classList))
        allProjectsInfo.append(projectList[-1])
    saveInfo(allProjectsInfo, "infos", "/home/lucas/tcc/")


if __name__ == "__main__":
    main()