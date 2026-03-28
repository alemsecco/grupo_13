import sys
from parseExpressao import parseExpressao
from gerarAssembly import gerarAssembly, lerArquivo
from executarExpressao import executar_expressao, parenteses_aninhados

def exibirResultados(programa_rpn, memoria, historico):

    for idx, tokens_linha in enumerate(programa_rpn):
        try:
            # atualiza a memória e o histórico automaticamente a cada linha
            res = executar_expressao(tokens_linha, memoria, historico)
            
            # imprime com uma casa decimal 
            if res is not None:
                print(f"Linha {idx + 1:02d}: {res:.1f}")
            else:
                print(f"Linha {idx + 1:02d}: (Sem retorno)")

        except Exception as e:
            # em caso de erro, avisa a linha e o motivo
            print(f"Linha {idx + 1:02d}: ERRO -> {str(e)}")
            # adiciona 0.0 no histórico para não perder o índice do RES
            historico.append(0.0)

def main():
    if len(sys.argv) < 2:
        print("Erro! python main.py nome_do_arquivo.txt")
        return
    
    nome_arquivo = sys.argv[1]
    print(f"Iniciando compilador para ARMv7. Lendo arquivo '{nome_arquivo}'...\n")
    
    # le o arquivo
    linhas = lerArquivo(nome_arquivo)
    if not linhas:
        return # parar se der erro na leitura
        
    programa_rpn = []
    memoria = {}
    historico = []
    
    # análise léxica 
    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue

        tokens = parseExpressao(linha_limpa)
        tokens_rpn = parenteses_aninhados(tokens)
        programa_rpn.append(tokens_rpn)

        
    # programa roda a calculadora e atualiza memoria/historico
    exibirResultados(programa_rpn, memoria, historico)

    # gerando codigo assembly
    print("\nGerando Assembly ARMv7...")
    codigo_arm = gerarAssembly(programa_rpn)
    
    # salva o arquivo 
    with open("saida_arm.s", "w") as f:
        f.write(codigo_arm)
        
    print("Sucesso! O arquivo 'saida_arm.s' foi gerado.")
    print("Copie o conteúdo dele e cole no CPULator (Arquitetura ARMv7).")

if __name__ == "__main__":
    main()