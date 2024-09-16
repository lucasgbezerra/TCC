from bs4 import BeautifulSoup
import csv
import json

def readJson(nome):
    with open(nome, 'r') as f:
        return json.load(f)

def extractTableFromDiv(soup, divId):
    div = soup.find('div', id=divId)
    if not div:
        print(f"Não foi possível encontrar o div com id='{divId}'.")
        return None

    table = div.find('table')
    if not table:
        print(f"Não foi possível encontrar a tabela dentro do div com id='{divId}'.")
        return None

    return table

def extractRowData(row):
    cols = row.find_all('td')
    if len(cols) >= 3:
        classTest = cols[0].find('a').get_text().split('.')[-1]
        numTests = cols[1].get_text()
        numFails = cols[2].get_text()
        return [classTest, numTests, numFails]
    return None

def writeTableToCsv(table, csvFile):
    with open(csvFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ClassTest', 'numTests', 'numFails'])

        for row in table.find_all('tr')[1:]:
            rowData = extractRowData(row)
            if rowData:
                writer.writerow(rowData)

def htmlToCsv(htmlFile, csvFile):
    with open(htmlFile, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    table = extractTableFromDiv(soup, 'tab3')
    if table:
        writeTableToCsv(table, csvFile)

def readCsvA(csvAFile):
    csvAData = {}
    with open(csvAFile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            className = row['class']
            csvAData[className] = row
    return csvAData

def readCsvB(csvBFile):
    csvBData = {}
    with open(csvBFile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            testName = row['ClassTest']
            csvBData[testName] = row
    return csvBData

def writeCombinedCsv(outputCsvFile, csvAData, csvBData, listData):
    with open(outputCsvFile, 'w', newline='') as file:
        fieldnames = ['class', 'numMethods', 'numTries', 'numImports', 'testName', 'numTests', 'numFails', 'output0', 'output1', 'output2', 'output3']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in listData:
            className = item['name']
            testName = item['testName'] if item['testName'] else "-"
            
            if className in csvAData:
                csvARow = csvAData[className]
                if testName in csvBData:
                    csvBRow = csvBData[testName]
                    numTests = csvBRow['numTests']
                    numFails = csvBRow['numFails']
                else:
                    numTests = '0'
                    numFails = '0'
                
                writer.writerow({
                    'class': className,
                    'numMethods': csvARow['numMethods'],
                    'numTries': csvARow['numTries'],
                    'numImports': csvARow['numImports'],
                    'testName': testName,
                    'numTests': numTests,
                    'numFails': numFails,
                    'output0': csvARow['output0'],
                    'output1': csvARow['output1'],
                    'output2': csvARow['output2'],
                    'output3': csvARow['output3']
                })

def main():
    htmlToCsv('/home/lucas/tcc/reps/zaproxy/zap/build/reports/tests/test/index.html', 'resultados-report.csv')
    infos = readJson('infos.json')
    
    csvAData = readCsvA('metricas-zaproxy.csv')	
    csvBData = readCsvB('resultados-report.csv')
    writeCombinedCsv('tabela-resultados.csv', csvAData, csvBData, infos[0]['classes'])

if __name__ == "__main__":
    main()
