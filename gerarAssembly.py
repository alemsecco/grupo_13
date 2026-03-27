def gerarAssembly(tokens):
    assembly = []
    for token in tokens:
        if token.replace('.', '', 1).isdigit():  # verifica se é um número (inteiro ou real)
            assembly.append(f"LOAD {token}")  # exemplo de comando para carregar um número
        elif token in ['+', '-', '*', '/', '//', '%', '^']:
            assembly.append(f"OP {token}")  # exemplo de comando para operador
        elif token in ['RES', 'MEM']:
            assembly.append(f"CMD {token}")  # exemplo de comando para comandos especiais
        else:
            raise ValueError(f"Token inválido: {token}")
    return '\n'.join(assembly)

def lerArquivo(nomeArquivo):
    try:
        with open(nomeArquivo, 'r') as file:
            linhas = file.readlines()
        return [linha.strip() for linha in linhas]
    except FileNotFoundError:
        raise FileNotFoundError(f"Erro! O arquivo '{nomeArquivo}' não foi encontrado.")
    except IOError as e:
        raise IOError(f"Erro ao ler o arquivo '{nomeArquivo}': {e}")
    
# testes
def testarGerarAssembly():
    tokens = ["3.14", "2.0", "+", "RES", "5.0", "MEM"]
    assembly = gerarAssembly(tokens)
    print(assembly)
    print('--- \n')

def testarLerArquivo():
    nomeArquivo = "teste.txt"
    linhas = lerArquivo(nomeArquivo)
    for linha in linhas:
        print(linha)

if __name__ == "__main__":
    testarGerarAssembly()
    testarLerArquivo()