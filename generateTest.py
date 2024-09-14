from openai import OpenAI
from dotenv import dotenv_values
import os
import json
import re
import subprocess
from time import sleep
import csv

env_vars = dotenv_values(".env")
KEY = env_vars.get("OPENAI_API_KEY")
PROJECT_ID = env_vars.get("PROJECT_ID")
client = OpenAI(
    api_key=KEY,
    organization='org-hb4V3o4P9oJnavCMtYL4yWDi',
    project=PROJECT_ID,
)


raiz = "/home/lucas/tcc"


def getOpenAiResponse(messages, temperature=0.7, top_p=0.9, frequency_penalty=0.0, presence_penalty=0.0):
    try:
        response = client.chat.completions.create(    
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        # response = client.chat.completions.create(    
        # model="gpt-3.5-turbo",
        # messages=messages,
        # )

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Retornar None ou outro valor padrão em caso de erro


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

def appendFile(fileName, content):
    try:
        with open(fileName, 'a', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Erro: {e}")

def readClass(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    
    inline_comment_pattern = r'//.*?$'
    block_comment_pattern = r'/\*.*?\*/'
    
    without_block_comments = re.sub(block_comment_pattern, '', code, flags=re.DOTALL)
    
    without_comments = re.sub(inline_comment_pattern, '', without_block_comments, flags=re.MULTILINE)
    
    return without_comments


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
        # print("stdout:\n", result.stdout)
        # print("stderr:\n", result.stderr)

        if result.returncode == 0:
            print("Tests ran successfully")
            return True, None
        else:
            print("Tests failed")
            # if "tests completed" in result.stderr:
            #     return False , result.stdout
            return False, result.stderr
        
    except Exception as e:
        print(result.stderr)
        print(f"Error: {e}")

    finally:
        os.chdir(raiz)
   

# def runTests(projectPath, isGradlew):
#     try:
#         print("Running all tests...")
#         os.chdir(projectPath)
#         if isGradlew:
#             command = ["./gradlew",  "-x", "check", "cleanTest", "test"]
#         else:
#             command = ["mvn", "surefire-report:report"]
#         print("Running tests...")
#         result = subprocess.run(command, capture_output=True, text=True)
#         if result.returncode == 0:
#             # print(result.stdout)
#             return True, "Tests ran successfully:\n" + result.stdout
#         else:
#             print(result.stderr)
#             return False , result.stderr
#     finally:
#         os.chdir(raiz)


def processTest(classInfo, errorMessage=None):
    try:
        if errorMessage:
            print("Repairing test...")
            prompt = buildPrompt(classPath=classInfo['classPath'], testPath=classInfo['testPath'], error=errorMessage)
            # code = readClass(classInfo['testPath']) 
        else:
            print("Generating test...")
            prompt = buildPrompt(classPath=classInfo['classPath'], className=classInfo['name'], testName=classInfo['testName'], classMethods=classInfo['methods'])
            # code = readClass(classInfo['classPath'])
           
        response = getOpenAiResponse([
                        {"role": "user", "content": prompt}
                    ],)
        if response != None:
            javaCode = extractCode(response)
            if javaCode and javaCode.strip():
                writeFile(classInfo['testPath'], javaCode)
    
            # Save the code in the test file
            appendFile('/home/lucas/tcc/responses/prompt.txt', prompt)
            appendFile('/home/lucas/tcc/responses/response.txt', response)

    except Exception as e:
        print("Error: "+ e) 

    

def packagePath(filepath):
    path = os.path.splitext(filepath)[0]
    package = path.replace(os.path.sep, '.')
    items = package.split('.')
    if 'org' in items:
        package = '.'.join(items[items.index('org'):])

    return package

def buildPrompt(classPath, testPath=None, className=None, testName=None ,classMethods=None, error=None):

    if error and len(error) > 0:
        repairTemplate = readFile('repairTemplate.txt')
        # classCode = readClass(classPath)
        testCode = readClass(testPath)
        repairTemplate = repairTemplate.replace('ERROR_MESSAGE', error)
        # repairTemplate = repairTemplate.replace('CLASS_CODE', classCode)
        repairTemplate = repairTemplate.replace('TEST_CODE', testCode)

        # return f'{code}\n{repairTemplate}\n{error}'
        return f'{repairTemplate}'

    else:
        generatioTemplate = readFile('generatioTemplate.txt')
        generatioTemplate = generatioTemplate.replace('CLASS_NAME', className)
        generatioTemplate = generatioTemplate.replace('TEST_NAME', testName)
        generatioTemplate = generatioTemplate.replace('CLASS_PATH', classPath)
        generatioTemplate = generatioTemplate.replace('METHOD_NAME', ', '.join(classMethods))
        code = readClass(classPath)
        return f'{generatioTemplate}\n{code}'
        # return f'{generatioTemplate}'


def removeTestFile(testPath, currentTest):
    """Remove the test file specified by test_path."""
    if os.path.isfile(testPath):
        if currentTest != "":
            writeFile(testPath, currentTest)
        else:
            os.remove(testPath)
    else:
        print(f"Test file not found: {testPath}")

def writeCSV(data, file_name):
    try:
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if data == {}:
                writer.writerow(['class', 'numMethods', 'numTries', 'numImports', 'output0', 'output1', 'output2', 'output3'])
            else:
                writer.writerow([data['class'], data['numMethods'], data['numTries'], data['numImports']] + data['outputList'])
        
        print(f"Data appended to CSV '{file_name}' successfully.")
    except Exception as e:
        print(f"Error creating or appending to CSV file: {e}")

def hasFile(filePath):
    if os.path.exists(filePath):
        return readClass(filePath)
    return ""

def countImports(filePath):
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
        
        importsCount = 0

        for line in lines:
            strippedLine = line.strip()
            
            if strippedLine.startswith('class'):
                break
            
            if strippedLine.startswith('import'):
                importsCount += 1
        
        return importsCount

    
    except FileNotFoundError:
        print(f"File not found: {filePath}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def identifyError(errorMessage):
    print("Identifying error type...")
    if "Compilation failed" in errorMessage or "compiler error" in errorMessage:
        return "Compilation errors"
    elif "Test not configured" in errorMessage or "No tests found" in errorMessage:
        return "Test configuration errors"
    elif "gradle configuration failed" in errorMessage or "Could not create task" in errorMessage:
        return "Gradle configuration errors"
    elif "RuntimeException" in errorMessage or "NullPointerException" in errorMessage:
        return "Runtime errors"
    else:
        return "Unknown error type"

def main():
    projectsInfos = readJson('projectsInfos.json')
    infos = readJson('infos.json')
    outputTemplate = readFile('outputTemplate.txt')
    currentTest = ""
    repairTries = 0
    testcompiled = False

    # Open the CSV file and write the header
    csvFileName = '2metricas7.csv'
    writeCSV({}, csvFileName)

    # Process each class
    projectInfos = projectsInfos[0]
    classesInfo = infos[0]['classes']
   
    for classInfo in classesInfo:
        # Initialize data
        data = {
            'class': classInfo['name'],
            'numMethods': len(classInfo['methods']),
            'numTries': 0,
            'numImports': countImports(classInfo['classPath']),
            'outputList': []
        }

        repairTries = 0
        if os.path.exists(classInfo['testPath']):
            currentTest = readClass(classInfo['testPath'])
        processTest(classInfo)

        # Run the test
        while repairTries <= 3:
            print(f"Repair try: {repairTries} Class: {classInfo['name']}")
            testcompiled, error = runTest(projectInfos['source'], classInfo['testPath'], projectInfos['gradlew'])

            data['numTries'] = repairTries
            if testcompiled:
                data['outputList'].append("Success")
                break

            errorType = identifyError(error)
            if errorType == "Unknown error type":
                errorType = getOpenAiResponse([{"role": "user", "content": f'Error: {error}\n{outputTemplate}'}])
            data['outputList'].append(errorType)

            processTest(classInfo, error)
            repairTries += 1
        
        if not testcompiled:
            removeTestFile(classInfo['testPath'], currentTest)

        # Write data for the current class to the CSV file
        writeCSV(data, csvFileName)

if __name__ == "__main__":
    main()

# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/ZAPUnitTest.java
# /home/lucas/tcc/reps/zaproxy/zap/src/test/java/org/zaproxy/zap/VersionUnitTest.java