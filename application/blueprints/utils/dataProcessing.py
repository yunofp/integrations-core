def findByName(list, name): 
    objectFound = next((item for item in list if item["name"] == name), '')
    if not objectFound:
        return ""
    return objectFound['value']

def defineVariablesGrow(contractValues):

    clickSignVariables = {
        "nomeCompletoDoTitular": findByName(contractValues, "nomeDoCliente-Llaz"),
        "email": findByName(contractValues, "emailDoCliente"),
        "dataDeNascimento": findByName(contractValues, "dataDeNascimentoDoTitular"),
        "telefoneDoTitular": findByName(contractValues, "contatoDoCliente"),
        "cpfDoTitular": findByName(contractValues, "cPFCPNJ"),
        "endereco": findByName(contractValues, "endereco"),
        "bairro": findByName(contractValues, "bairro"),
        "cidade": findByName(contractValues, "cidade"),
        "uf": findByName(contractValues, "uF"),
        "cep": findByName(contractValues, "cEP"),
        "nomeCompletoDoConjuge": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "emailDoConjuge": findByName(contractValues, "email"),
        "dataDeNascimentoDoConjuge": findByName(contractValues, "dataDeNascimento"),
        "telefoneDoConjuge": findByName(contractValues, "telefone"),
        "prazoDeVigencia": findByName(contractValues, "prazoDeVigencia"),
        "closerResponsavel": findByName(contractValues, "responsavelPelaContratacao") or findByName(contractValues, "informeOCloser"),
        "origemInterna": findByName(contractValues, "origemInterna"),
        "origemExterna": findByName(contractValues, "origemExterna"),
        "valorDaImplantacao": findByName(contractValues, "valorDeImplantacao"),
        "dataDoPagamentoDaImplantacao": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "formaDePagamentoDaImplantacao": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        "fee": findByName(contractValues, "valorDoFEE"),
        "diaDaCobrançaDoFee": findByName(contractValues, "diaDaCobrancaRecorrente"),
        "observacoes": findByName(contractValues, "observacao") or findByName(contractValues, "obervacao")
    }
    return clickSignVariables

def defineVariablesWealth(contractValues):
    clickSignVariablesGrow = defineVariablesGrow(contractValues)
    clickSignVariablesWealth = {
        "cobrancaPelaCorretora": findByName(contractValues, "autorizacaoDeCobrancaPelaCorretora"),
        "patrimonioFinanceiroEstimado": findByName(contractValues, "patrimonioFinanceiro"),
        "vincularAContratoPai": findByName(contractValues, "haveraVinculacaoContratoPai"),
        "numeroDoContratoPai": findByName(contractValues, "numeroDoContratoPai")
    }
    
    clickSignVariables = {**clickSignVariablesGrow, **clickSignVariablesWealth}
    return clickSignVariables

def defineVariablesWork(contractValues):
    clickSignVariables = {
        "nomeDaEmpresa": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "emailDeContato": findByName(contractValues, "emailDoCliente"),
        "telefoneDaEmpresa": findByName(contractValues, "contatoDoCliente"),
        "cnpj": findByName(contractValues, "cPFCPNJ"),
        "endereco": findByName(contractValues, "endereco"),
        "bairro": findByName(contractValues, "bairro"),
        "cidade": findByName(contractValues, "cidade"),
        "uf": findByName(contractValues, "uf"),
        "cep": findByName(contractValues, "cEP"),
        "nomeCompletoDoResponsavel": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "cargoDoResponsavel": findByName(contractValues, "profissaoDoTitular"),
        "emailDoResponsavel": findByName(contractValues, "email"),
        "dataDeNascimentoDoResponsavel": findByName(contractValues, "dataDeNascimento"),
        "cpfDoResponsavel": findByName(contractValues, "cPF"),
        "telefoneDoResponsavel": findByName(contractValues, "telefone"),
        
        "prazoDeVigencia": findByName(contractValues, "prazoDeVigencia"),
        "closerResponsavel": findByName(contractValues, "responsavelPelaContratacao") or findByName(contractValues, "informeOCloser"),
        "origemInterna": findByName(contractValues, "origemInterna"),
        "origemExterna": findByName(contractValues, "origemExterna"),
        
        "valorDaImplantacão": findByName(contractValues, "valorDeImplantacao"),
        "dataDoPagamentoDaImplantacao": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "formaDePagamentoDaImplantacao": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        
        "fee": findByName(contractValues, "valorDoFEE"),
        "diaDaCobrançaDoFee": findByName(contractValues, "diaDaCobrancaRecorrente"),
        "observacoes": findByName(contractValues, "observacao") or findByName(contractValues, "obervacao"),
    }
    return clickSignVariables

def validate_contract_code(value):
    if len(value) == 6 and value.isdigit():
        if value[0] in '123' and value[1] in '12':
            return True
    return False