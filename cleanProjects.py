import json
import os
import subprocess

# Defina o caminho para o arquivo projectsInfos.json
file_path = "/home/lucas/tcc/projectsInfos.json"

# Dados do projeto fornecidos
# projects_data = [
#     {"name": "zaproxy", "source": "/home/lucas/tcc/reps/zaproxy/zap/src", "gradlew": True},
#     # {"name": "Stirling-PDF", "source": "/home/lucas/tcc/reps/Stirling-PDF/src", "gradlew": True},
#     # {"name": "jenkins", "source": "/home/lucas/tcc/reps/jenkins", "gradlew": False},
#     # {"name": "mybatis-3", "source": "/home/lucas/tcc/reps/mybatis-3", "gradlew": False},
#     # {"name": "zookeeper", "source": "/home/lucas/tcc/reps/zookeeper", "gradlew": False},
#     # {"name": "fastexcel", "source": "/home/lucas/tcc/reps/fastexcel", "gradlew": False}
# ]

# # Cria o arquivo JSON se não existir
# if not os.path.exists(file_path):
#     with open(file_path, 'w') as file:
#         json.dump(projects_data, file, indent=4)

# Carrega as informações do projeto do arquivo JSON
with open(file_path, 'r') as file:
    project = json.load(file)

# Itera sobre cada projeto e executa `git checkout .` no diretório de origem
# for project in projects:
source_dir = project["source"]
os.chdir(source_dir)
subprocess.run(["git", "clean", "-fd"])
subprocess.run(["git", "checkout", "--","."])

print("Script executado com sucesso.")
