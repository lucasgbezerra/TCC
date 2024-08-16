from openai import OpenAI
from dotenv import dotenv_values
import os
import json
import re
import subprocess

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
            file.close()
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


def runTest(projectPath, testPath, isGradlew):
    testPackage = packagePath(testPath)
    print("Test Package: " + testPackage)
    try:
        os.chdir(projectPath)
        print(f"Successfully changed the directory to: {os.getcwd()}")
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
            return False , result.stderr
        
    except FileNotFoundError:
        print(f"Error: The directory {projectPath} does not exist.")

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
            print(result.stdout)
            return True, "Tests ran successfully:\n" + result.stdout
        else:
            print(result.stderr)
            return False , result.stderr
    finally:
        os.chdir(raiz)

# def runTestMaven(projectPath, testPath):
#     testPackage = packagePath(testPath)
#     print(testPackage)
#     try:
#         os.chdir(projectPath)
#         print(f"Successfully changed the directory to: {os.getcwd()}")
#         print("Running test: "+testPackage+ "...")
#         result = subprocess.run(command, capture_output=True, text=True)
#         if result.returncode == 0:
#             return True, "Tests ran successfully:\n" + result.stdout
#         else:
#             return False ,result.stderr

#     except FileNotFoundError:
#         print(f"Error: The directory {projectPath} does not exist.")
    
#     finally:
#         os.chdir(raiz)

def optmizeTest(testPath, errorMessage, isGradlew):
    optmizerTemplate = readFile('optmizerTemplate.txt')
    if isGradlew:
        pattern = re.compile(r"(.*?)(\* Try:)", re.DOTALL)
        match = pattern.search(errorMessage)
        if match:
            error = match.group(1)
    else:
        error_lines = [line for line in errorMessage if '[ERROR]' in line]
        error = '\n'.join(error_lines)
    try:
        print(error)
        prompt = buildPrompt(testPath, optmizerTemplate, error)
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
def main():
    packagePath("/home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/ZAPUnitTest.java")

def main():
    generatioTemplate = readFile('template2.txt')
    projectsInfos = readJson('projectsInfos.json')
    classesInfo = readJson('infos.json')
    count = 0
    optmizeTries = 0
    testcompiled = False

    while count < len(projectsInfos):
        print(classesInfo[count]['project'])
        for classInfo in classesInfo[count]['classes']:
            print(classInfo['name'])
            optmizeTries = 0
            # Create prompt with informations of the class
            generatioTemplate = generatioTemplate.replace('CLASS_NAME', classInfo['name'])
            generatioTemplate = generatioTemplate.replace('CLASS_PATH', classInfo['classPath'])
            generatioTemplate = generatioTemplate.replace('METHOD_NAME', ', '.join(classInfo['methods']))
            prompt = buildPrompt(classInfo['classPath'], generatioTemplate, classInfo['methods'])
            # submit the prompt to OpenAI
            response = getOpenAiResponse(prompt)
            # Extract the code from the response
            javaCode = extractCode(response)
            # Save the code in the test file
            writeFile(classInfo['testPath'], javaCode)
            # Run the test
            while optmizeTries < 3:
                print("Classe: "+ classInfo['name'])
                print("Optmize try: "+str(optmizeTries))
                optmizeTries += 1
                testcompiled, error = runTest(projectsInfos[count]['source'], classInfo['testPath'], projectsInfos[count]['gradlew'])
                if testcompiled:
                    break
                optmizeTest(classInfo['testPath'], error,  projectsInfos[count]['gradlew'])

        runTests(projectsInfos[count]['source'], projectsInfos[count]['gradlew'])
        count +=1

if __name__ == "__main__":
    main()

# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/ZAPUnitTest.java
# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/VersionUnitTest.java