from parseExpressao import parseExpressao
from gerarAssembly import gerarAssembly, lerArquivo
from executarExpressao import executar_expressao


def main():
    memoria = {}
    historico = []
    
    linhas = lerArquivo("teste.txt")
    
    for numero_linha, linha in enumerate(linhas, start=1):
        if not linha: 
            continue
            
        try:
            
            tokens_rpn = parseExpressao(linha)
            
            
            resultado = executar_expressao(tokens_rpn, memoria, historico)
            if resultado is not None:
                print(f"Linha {numero_linha} | Res: {resultado}")
            
           
            codigo_asm = gerarAssembly(tokens_rpn)
            print(codigo_asm)
            
        except Exception as e:
            print(f"Erro na linha {numero_linha}: {e}")

if __name__ == "__main__":
    main()