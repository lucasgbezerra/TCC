from openai import OpenAI
from dotenv import dotenv_values
import os
import json
import re
import subprocess
from time import sleep

env_vars = dotenv_values(".env")
KEY = env_vars.get("OPENAI_API_KEY")
PROJECT_ID = env_vars.get("PROJECT_ID")
client = OpenAI(
    api_key=KEY,
    organization='org-hb4V3o4P9oJnavCMtYL4yWDi',
    project=PROJECT_ID,
)


raiz = "/home/lucas/tcc"



# def getOpenAiResponse(prompt):

#     response = client.chat.completions.create(    
#         model="gpt-3.5-turbo",
#         messages=[
#          {"role": "user", "content": prompt},
#         ],
#         )

#     return response.choices[0].message.content

def getOpenAiResponse(prompt):
    response = client.chat.completions.create(    
        model="gpt-3.5-turbo",
        messages=[
         {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return response.choices[0].message.content

def readFile(nome):
    with open(nome, 'r') as f:
        return f.read()

def readJson(nome):
    with open(nome, 'r') as f:
        return json.load(f)

def writeFile(fileName, content):
    try:
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Erro: {e}")


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


def runTest(projectPath, testPath, isGradlew):
    testPackage = packagePath(testPath)
    try:
        os.chdir(projectPath)
        if(isGradlew):
            command = ["./gradlew",  "-x", "check", "cleanTest", "test", "--tests", testPackage]
        else:
            command = ["mvn", f'-Dtest={testPackage}', "test"]
        print("Running test: "+testPackage+ "...")
        result = subprocess.run(command, capture_output=True, text=True)
        # Print stdout and stderr for debugging
        print("stdout:\n", result.stdout)
        print("stderr:\n", result.stderr)

        if result.returncode == 0:
            print("Tests ran successfully")
            return True, None
        else:
            print("Tests failed")
            if "tests completed" in result.stderr:
                return False , result.stdout
            return False, result.stderr
        
    except Exception as e:
        print(result.stderr)
        print(f"Error: {e}")

    finally:
        os.chdir(raiz)
   


def runTests(projectPath, isGradlew):
    try:
        print("Running all tests...")
        os.chdir(projectPath)
        if isGradlew:
            command = ["./gradlew",  "-x", "check", "cleanTest", "test"]
        else:
            command = ["mvn", "surefire-report:report"]
        print("Running tests...")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            # print(result.stdout)
            return True, "Tests ran successfully:\n" + result.stdout
        else:
            print(result.stderr)
            return False , result.stderr
    finally:
        os.chdir(raiz)


def optmizeTest(testPath, errorMessage, isGradlew):
    optmizerTemplate = readFile('optmizerTemplate.txt')
    # if isGradlew:
    #     pattern = re.compile(r"(.*?)(\* Try:)", re.DOTALL)
    #     match = pattern.search(errorMessage)
    #     if match:
    #         error = match.group(1)
    # else:
    #     error_lines = [line for line in errorMessage if '[ERROR]' in line]
    #     error = '\n'.join(error_lines)
    try:
        prompt = buildPrompt(readClass(testPath), optmizerTemplate, errorMessage)
        # submit the prompt to OpenAI
        response = getOpenAiResponse(prompt)
        # Extract the code from the response
        javaCode = extractCode(response)
        # Save the code in the test file
        writeFile(testPath, javaCode) 

    except Exception as e:
        print("Error: "+ e) 

    

def packagePath(filepath):
    path = os.path.splitext(filepath)[0]
    package = path.replace(os.path.sep, '.')
    items = package.split('.')
    if 'org' in items:
        package = '.'.join(items[items.index('org'):])

    return package

def buildPrompt(code, template, error):
    if(len(error) > 0):
        return f'{code}\n\n{template}\{error}'
    else:
        return f'{code}\n\n{template}'


def saveTestFile(testPath, code):
    with open(testPath, 'w') as f:
        f.write(code)



def removeTestFile(testPath):
    """Remove the test file specified by test_path."""
    if os.path.isfile(testPath):
        os.remove(testPath)
        print(f"Removed test file: {testPath}")
    else:
        print(f"Test file not found: {testPath}")

def writeCSV(dataList, file_name):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            # Escreve o cabeçalho
            file.write('class,method,numTries,outputList\n')
            
            # Escreve cada dicionário como uma linha no CSV
            for data in dataList:
                output_str = ','.join(data['outputList'])
                # Concatena os valores e adiciona uma nova linha
                line = f"{data['class']},{data['method']},{data['numTries']},{output_str}\n"
                file.write(line)
        
        print(f"Arquivo CSV '{file_name}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o arquivo CSV: {e}")

def main():
    generatioTemplate = readFile('generatioTemplate.txt')
    projectInfos = readJson('projectsInfos.json')
    infos = readJson('infos.json')
    outputTemplate = readFile('outputTemplate.txt')
    count = 0
    optmizeTries = 0
    testcompiled = False
    dataList = []

    classesInfo = infos[0]['classes']
    for classInfo in classesInfo:
        data = {}
        data['class'] = classInfo['name']
        data['method'] = len(classInfo['methods'])
        data['numTries'] = 0
        data['outputList'] = []

        print(classInfo['name'])
        optmizeTries = 0
        # Create prompt with informations of the class
        generatioTemplate = generatioTemplate.replace('CLASS_NAME', classInfo['name'])
        generatioTemplate = generatioTemplate.replace('CLASS_PATH', classInfo['classPath'])
        generatioTemplate = generatioTemplate.replace('METHOD_NAME', ', '.join(classInfo['methods']))
        prompt = buildPrompt(readClass(classInfo['classPath']), generatioTemplate, classInfo['methods'])
        # submit the prompt to OpenAI
        response = getOpenAiResponse(prompt)
        # Extract the code from the response
        javaCode = extractCode(response)
        # Save the code in the test file
        print("Writing test file...")
        writeFile(classInfo['testPath'], javaCode)
        # writeFile(f"/home/lucas/tcc/responses/{classInfo['name']}{optmizeTries}.java", javaCode) 

        # Run the test
        while optmizeTries <= 3:
            sleep(1)
            print("Classe: "+ classInfo['name']+ " Optmize try: "+str(optmizeTries))
            testcompiled, error = runTest(projectInfos['source'], classInfo['testPath'], projectInfos['gradlew'])
            data['numTries'] = optmizeTries
            if testcompiled:
                data['outputList'].append("Success")
                break
            errorCategorize = buildPrompt(error, outputTemplate, "")
            data['outputList'].append(getOpenAiResponse(errorCategorize))
            optmizeTest(classInfo['testPath'], error,  projectInfos['gradlew'])
            optmizeTries += 1
            writeFile(f"/home/lucas/tcc/responses/{classInfo['name']}{optmizeTries}.java", readClass(classInfo['testPath'])) 

        # if optmizeTries > 3 and not testcompiled:
        #     removeTestFile(classInfo['testPath'])
            
    
        dataList.append(data)
        
        # runTests(projectsInfos[count]['source'], projectsInfos[count]['gradlew'])
        count +=1
    writeCSV(dataList, 'metricas.csv')
if __name__ == "__main__":
    main()

# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/ZAPUnitTest.java
# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/VersionUnitTest.java