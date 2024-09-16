import re
import os
import json
import random


classesTeste = []

def getClass(dir):
    lstInfoClass = []

    for sourceDir, subDir, files in os.walk(dir):
        for file in files:
            if file.endswith(".java") and not "test" in file.lower() and not "test" in sourceDir.lower():
                filePath = os.path.join(sourceDir, file)
                className = file.removesuffix('.java')
                with open(filePath, 'r') as javaFile:
                    fileContent = javaFile.read()
                    if f"interface {className}" in fileContent:
                        continue  # Ignora interfaces

                lstInfoClass.append({'name': className,'testName': '','classPath': filePath,'testPath': '', 'methods': []})



    
    return lstInfoClass
 
def findTestFileForClass(lstClass, dir):
    print("findTestFileForClass")
    
    for classe in lstClass:
        for sourceDir, subDirs, files in os.walk(dir):
            for file in files:
                if file.lower() == f"{classe['name']}test.java".lower() or file.lower() == f"{classe['name']}unittest.java".lower():
                    classe['testPath'] = os.path.join(sourceDir, file)
                    classe['testName'] = file.removesuffix('.java')
                    break  

            if classe['testPath']:
                break

        if not classe['testPath']:
            classe['testPath'] = classe['classPath'].replace("main", "test").replace(".java", "Test.java")
            classe['testName'] = classe['name'] + "Test"

def removeClassIfNotTested(lstClass):
    newLstClass = []
    for c in lstClass:
        if c['testPath'] != '' and c['classPath'] != '':
            newLstClass.append(c)

    return newLstClass


def extractMethodSignatures(class_list):
    print("extractMethodSignatures")
    for index, class_info in enumerate(class_list, start=0):
        method_names = []
        if not os.path.exists(class_info['classPath']):
            print(f"The file does not exist.")
            return
        
        with open(class_info['classPath'], 'r') as class_file:
            class_file_lines = class_file.readlines()

        method_pattern = re.compile(r'(?:(?:public|protected)\s+)+[\w\<\>\[\]]*\s*(\w+)\s*\([^\)]*\)\s*[^\{}]*{')

        for line in class_file_lines:
            match = method_pattern.search(line)
            if match:
                method_signature = match.group(1)
                if method_signature not in method_names and len(method_signature) > 1:
                    method_names.append(method_signature)
        
        class_list[index]['methods'] = method_names

    return class_list

def selectRandomClasses(classesList, numClasses=5, seed=42):

    classesWithMethods = [c for c in classesList if len(c['methods']) > 0]

    if numClasses > len(classesWithMethods):
        raise ValueError("Number of elements to select cannot be greater than the length of the list.")
    
    selectedClasses = random.sample(classesWithMethods, numClasses)
    
    return selectedClasses


def saveInfo(classList, name, path):
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, f"{name}.json")

    jsonData = json.dumps(classList, indent=4)

    with open(file_path, 'w') as json_file:
        json_file.write(jsonData)

def getProjectsInfos(filePath):
    with open(filePath, 'r') as arquivo:
        return json.load(arquivo)


def main():
    projects = getProjectsInfos("arquivos_de_configuracao/projectsInfos.json")

    
    for project in projects:
        projectClasses = {'project': project['name'], 'classes': []}
        projectClasses["classes"] = getClass(f"{project['source']}")
        
        findTestFileForClass(projectClasses['classes'], project['source'])
        projectClasses['classes'] = extractMethodSignatures(projectClasses['classes'])
        projectClasses['classes'] = selectRandomClasses(projectClasses['classes'])
        print(len(projectClasses['classes']))

        
        saveInfo(projectClasses, f"{project['name']}-info", "./arquivos_de_configuracao/")


if __name__ == "__main__":
    main()