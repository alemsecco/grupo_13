# Alex Menegatti Secco @alemsecco
# Mariana de Castro @maricastroo
# Grupo 13


# Autômatos Finitos Determinísticos
def estadoInicial(linha, i):
    if linha[i].isdigit() or linha[i] == '.':
        return estadoNumero
    if linha[i] in '+-*%^':
        return estadoOperador
    if linha[i] == '/':
        return estadoDivisao
    if linha[i] in '()':
        return estadoParenteses
    if linha[i].isalpha():
        return estadoComando
    raise ValueError(f"Token inválido: {linha[i]}")

def estadoNumero(linha, i): # recebe a linha e o índice atual, extrai um número (inteiro ou real) e retorna o número e o novo índice
    num = linha[i]
    i += 1
    while i < len(linha) and (linha[i].isdigit() or linha[i] == '.'): # continua enquanto for dígito ou ponto decimal
        num += linha[i]
        i += 1
    if num.count('.') > 1: # verifica se o número tem mais de um ponto decimal -> malformado
        raise ValueError(f"Número malformado: {num}")
    return num, i

def estadoOperador(linha, i): # recebe a linha e o índice atual, extrai um operador e retorna o operador e o novo índice
    return linha[i], i + 1 

def estadoParenteses(linha, i): # recebe a linha e o índice atual, extrai um parêntese e retorna o parêntese e o novo índice
    return linha[i], i + 1

def estadoComando(linha, i): # recebe a linha e o índice atual, extrai um comando (RES ou MEM) e retorna o comando e o novo índice
    cmd = linha[i]
    i += 1
    while i < len(linha) and linha[i].isalpha():
        cmd += linha[i]
        i += 1
    if cmd in ['RES', 'MEM']:
        return cmd, i
    else:
        raise ValueError(f"Token inválido: {cmd}")
    
def estadoDivisao(linha, i): # recebe a linha e o índice atual, extrai um operador de divisão (/, //) e retorna o operador e o novo índice
    if linha[i] == '/':
        if i + 1 < len(linha) and linha[i + 1] == '/':
            return '//', i + 2
        else:
            return '/', i + 1
    raise ValueError(f"Token inválido: {linha[i]}")

# parseExpressão 
def parseExpressao(linha): # recebe uma linha de texto e retorna um vetor de tokens
    tokens = []
    i = 0
    while i < len(linha):
        if linha[i].isspace():
            i += 1
            continue
        estado = estadoInicial(linha, i)
        token, i = estado(linha, i) # chama o estado atual para extrair o token e atualizar o índice
        tokens.append(token)
    return tokens

# Testes
def testeParseExpressao():
    assert parseExpressao("3.14 + 2 * (1 - 5)") == ['3.14', '+', '2', '*', '(', '1', '-', '5', ')'] # teste com expressão válida
    assert parseExpressao("RES MEM") == ['RES', 'MEM'] # teste com comandos especiais
    try:
        parseExpressao("3.14.5 + 2") # teste com número malformado
    except ValueError as e:
        assert str(e) == "Número malformado: 3.14.5"
    try:        parseExpressao("3.14 + @") # teste com token inválido
    except ValueError as e:
        assert str(e) == "Token inválido: @"
    print("Todos os testes passaram!")
    
if __name__ == "__main__": 
    testeParseExpressao()



