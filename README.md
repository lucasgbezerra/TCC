# Projeto TCC - Geração de Testes Unitários com OpenAI GPT-3.5 Turbo

Este projeto é desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) para analisar um projeto Java, extrair classes e métodos, e submetê-los à API OpenAI (modelo GPT-3.5 Turbo) para gerar casos de teste unitários automaticamente. A ferramenta facilita a criação de testes unitários, utilizando inteligência artificial para propor assertivas e verificar a funcionalidade do código-fonte.

## Pré-requisitos

Antes de executar o projeto, verifique se você possui os seguintes requisitos instalados:
- **Python 3.8+**
- **Gradle** (caso o projeto Java utilize Gradle para build)
-  **Maven** (caso o projeto Java utilize Maven para build)
- **API Key do OpenAI** (necessária para usar o GPT-3.5 Turbo)
- **Virtualenv** para criar um ambiente virtual Python

## Configuração do Projeto

### Passo 1: Configurar `projectsInfos.json`

Altere o arquivo `arquivos_de_configuracao/projectsInfos.json` para incluir as informações do seu projeto Java. O arquivo deve seguir o seguinte formato:

```json
{
  "name": "Nome do Projeto",
  "source": "caminho/para/o/projeto",
  "gradlew": true/false
}
```
## Passo 2:
### Na raiz do seu projeto, crie um arquivo chamado .env com as seguintes variáveis de ambiente:

```
OPENAI_API_KEY=#Adicione-sua-Chave-API-Aqui
PROJECT_ID=#Adicione-o-ID-do-Projeto
ORGANIZATION_ID=#Adicione-o-ID-da-Organização
```
### Passo 3: Instalar Dependências
Crie um ambiente virtual e instale as dependências necessárias para o projeto. Use os comandos abaixo:
```bash
# Criar o ambiente virtual
python3 -m venv venv
```
```bash
# Ativar o ambiente virtual
source venv/bin/activate  # Para Linux/Mac
# venv\Scripts\activate  # Para Windows
```
```bash
# Instalar os requisitos
pip install -r requirements.txt

```
## Executar os Scripts

### Passo 1: Executar o Analisador de Projetos
Com as configurações prontas, você pode agora executar o script de análise para obter as informações das classes e métodos do projeto Java. Execute o seguinte comando:

```bash
python projectAnalyzer.py
```
### Passo 2: Gerar os Testes Unitários
Após a análise do projeto, execute o seguinte script para gerar os testes unitários usando a API GPT-3.5 Turbo:

```bash
python projectAnalyzer.py
```
Os testes unitários gerados serão salvos no diretório configurado, prontos para serem utilizados no seu projeto.

### Scripts auxiliares
Os scripts cleanProject.py e extractDataReports.py são auxiliares para a obtenção das métricas destinadas ao projeto e precisam ser modificados para utlizição.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

