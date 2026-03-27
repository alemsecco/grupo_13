def gerarAssembly(tokens_rpn):
    assembly = []
    
    mapa_instrucoes = {
        '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
        '//': 'IDIV', '%': 'MOD', '^': 'POW'
    }

    for i, token in enumerate(tokens_rpn):
        if token.lstrip('-').replace('.', '', 1).isdigit():  
            assembly.append(f"PUSH {token}")     
            
        elif token in mapa_instrucoes:           
            assembly.append(mapa_instrucoes[token]) 
            
        elif token == "RES":
            assembly.append("CMD RES") # O 'N' já foi feito PUSH antes
            
        elif token.isupper() or (token.isalpha() and len(token) == 1):
            # Se for o último token e tivermos mais itens (como um valor), é atribuição
            if i == len(tokens_rpn) - 1 and len(tokens_rpn) > 1:
                assembly.append(f"STORE {token}")
            else:
                assembly.append(f"LOAD {token}")
                
        else:
            raise ValueError(f"Token inválido: {token}")

    return '\n'.join(assembly)

def lerArquivo(nomeArquivo):
    try:
        with open(nomeArquivo, 'r') as file:
            # O 'if linha.strip()' garante que linhas em branco não entrem na lista
            return [linha.strip() for linha in file if linha.strip()]
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