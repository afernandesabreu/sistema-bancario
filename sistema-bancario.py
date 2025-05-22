def obter_valor_valido(prompt: str) -> float:
    while True:
        valor_string = input(prompt)
        try:
            valor_float = float(valor_string)
            if valor_float > 0:
                return valor_float
            else:
                print('O valor informado não pode ser igual ou menor que 0.')
        except ValueError:
            print('Valor inválido. Por favor, informe um valor númérico.')

def verifica_quantidade_saque(numero_saques_realizados: int, numero_saques_possiveis: int) -> bool:
    if numero_saques_realizados < numero_saques_possiveis:
        return True
    else:
        print(f'O número máximo de operações de saque por dia é de {numero_saques_possiveis}. Você já alcançou este limite.')
        return False

def verifica_limite_saque(valor_saque: float, valor_limite_saque: float) -> bool:
    if valor_saque <= valor_limite_saque:
        return True
    else:
        print('Você ultrapassou o valor permitido para esta operação. Valor limite por saque: R$500,00')
        return False

def processar_deposito(saldo_atual: float, valor_depositado: float) -> float:
    novo_saldo = saldo_atual + valor_depositado
    print('Depósito realizado com sucesso')
    return novo_saldo

def processar_quantidade_saque(numero_saques_realizados: int) -> int:
        numero_saques_realizados += 1
        return numero_saques_realizados
    
def processar_saque(valor_sacado: float,
                    saldo_atual: float,
                    numero_saques_feitos: int,
                    limite_num_saques: int,
                    limite_valor_saque: float) -> tuple[float, int]:
    if not verifica_quantidade_saque(numero_saques_feitos, limite_num_saques):
        return saldo_atual, numero_saques_feitos
    if not verifica_limite_saque(valor_sacado, limite_valor_saque):
        return saldo_atual, numero_saques_feitos
    if valor_sacado > saldo_atual:
        print(f'A operação falhou. Saldo insuficiente. Saldo atual: R${saldo_atual:.2f}')
        return saldo_atual, numero_saques_feitos
    
    saldo_atual -= valor_sacado
    numero_saques_feitos = processar_quantidade_saque(numero_saques_feitos)
    print('Saque realizado com sucesso.')
    return saldo_atual, numero_saques_feitos



def gerar_extrato(saldo_atual: float, historico_transacoes: str, num_saques_feitos: int, limite_total_saques: int) -> None:
    saques_restantes = limite_total_saques - num_saques_feitos
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXTRATO BANCÁRIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    if not historico_transacoes:
        print("\nNão foram realizadas movimentações.")
    else:
        print("\nHistórico de Transações:")
        print(historico_transacoes.strip())

    print(f"\nSeu saldo é de: R$ {saldo_atual:.2f}")
    print(f"Você ainda pode realizar {saques_restantes} operação(ões) de saque hoje.")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXTRATO BANCÁRIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

menu = """
Escolha uma Opção:
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair 

==>
"""
saldo = 0.00
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
   

while True:
    opcao = input(menu)
    if opcao == 'd':
        print('Depósito')
        valor_depositado = obter_valor_valido('Por favor, informe o valor da operação: R$ ')
        saldo = processar_deposito(saldo, valor_depositado)
        extrato += f"Depósito: R$ {valor_depositado:>7.2f}\n"
        gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

    elif opcao == 's':
        print('Saque')
        valor_a_ser_sacado = obter_valor_valido('Por favor, informe o valor para operação: R$ ')
        saldo_anterior = saldo
        saldo, numero_saques = processar_saque(valor_a_ser_sacado, saldo, numero_saques, LIMITE_SAQUES, limite)
        if saldo < saldo_anterior:
            extrato += f"Saque:    R$ {valor_a_ser_sacado:>7.2f}\n"
        gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

    elif opcao == 'e':
        print('Extrato')
        gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

    elif opcao == 'q':
        print('Saindo do Sistema')
        break
    else:
        print('Operação Inválida, por favor, selecione novamente a operação desejada.')
