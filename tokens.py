import tiktoken

def contar_tokens_gpt35(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    # Usar o codificador de tokens do GPT-3.5 Turbo
    codificador = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    # Codificar o conteúdo em tokens
    tokens = codificador.encode(conteudo)
    
    # Retornar o número total de tokens
    return len(tokens)


total_tokens = contar_tokens_gpt35("/home/lucas/tcc/responses/AbstractFormDialog.java")
print(f"Total de tokens (GPT-3.5): {total_tokens}")