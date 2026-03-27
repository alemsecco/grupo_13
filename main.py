from parseExpressao import parseExpressao
from gerarAssembly import gerarAssembly, lerArquivo
from executarExpressao import executar_expressao, parenteses_aninhados


def main():
    nome_arquivo = "teste1.txt"
    print(f"Iniciando compilador para ARMv7. Lendo arquivo '{nome_arquivo}'...\n")
    
    # 1. Lê o arquivo
    linhas = lerArquivo(nome_arquivo)
    if not linhas:
        return # Para se deu erro na leitura
        
    programa_rpn = []
    
    # 2. Análise Léxica (Passa as linhas pela MEF)
    for linha in linhas:
        tokens = parseExpressao(linha)
        tokens_rpn = parenteses_aninhados(tokens)
        programa_rpn.append(tokens_rpn)
        print(f"Tokens lidos: {tokens_rpn}")
        
    # 3. Geração de Código
    print("\nGerando Assembly ARMv7...")
    codigo_arm = gerarAssembly(programa_rpn)
    
    # Salva o arquivo final
    with open("saida_arm.s", "w") as f:
        f.write(codigo_arm)
        
    print("Sucesso! O arquivo 'saida_arm.s' foi gerado.")
    print("Copie o conteúdo dele e cole no CPULator (Arquitetura ARMv7).")

if __name__ == "__main__":
    main()