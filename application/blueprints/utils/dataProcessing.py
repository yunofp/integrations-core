def findByName(list, name): 
    objectFound = next((item for item in list if item["name"] == name), None)
    if not objectFound:
        return ""
    return objectFound['value']

def defineVariablesGrow(contractValues):
    clickSignVariables = {
        "nomeCompletoDoTitular": findByName(contractValues, "nomeDoIndicado"),
        "email": findByName(contractValues, "emailDoIndicado"),
        "dataDeNascimento": findByName(contractValues, "dataDeNascimentoDoTitular"),
        "telefoneDoTitular":  findByName(contractValues, "telefone"),
        "cpfDoTitular":  findByName(contractValues, "cPF"),
        "endereco": findByName(contractValues, "endereco"),
        "bairro": findByName(contractValues, "bairro"),
        "cidade": findByName(contractValues, "cidade"),
        "uf": findByName(contractValues, "uf"),
        "cep": findByName(contractValues, "cEP"),
        "nomeCompletoDoConjuge": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "emailDoConjuge": findByName(contractValues, "email"),
        "dataDeNascimentoDoConjuge": findByName(contractValues, "dataDeNascimento"),
        "prazoDeVigencia": findByName(contractValues, "prazoDeVigencia"),
        "closerResponsavel": findByName(contractValues, "informeOCloser"),
        "origemInterna": findByName(contractValues, "origemInterna"),
        "origemExterna": findByName(contractValues, "origemExterna"),
        "valorDaImplantacão": findByName(contractValues, "valorDeImplantacao"),
        "dataDePagamentoDaImplantacao": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "formaDePagamentoDaImplantacao": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        "fee": findByName(contractValues, "valorDoFEE"),
        "diaDeCobrançaDoFee": findByName(contractValues, "diaDeCobrançaDoFee"),
        "observacoes": findByName(contractValues, "observacao"),
        "telefoneDoConjuge": findByName(contractValues, "telefone"),
        "qualOTipoDeTrabalho": findByName(contractValues, "qualOTipoDeTrabalho"),
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
        "emailDeContato": findByName(contractValues, "email"),
        "telefoneDaEmpresa": findByName(contractValues, "telefone"),
        "cnpj": findByName(contractValues, "cPFCPNJ"),
        "endereco": findByName(contractValues, "endereco"),
        "bairro": findByName(contractValues, "bairro"),
        "cidade": findByName(contractValues, "cidade"),
        "uf": findByName(contractValues, "uf"),
        "cep": findByName(contractValues, "cEP"),
        "nomeCompletoDoResponsavel": findByName(contractValues, "nomeDoIndicado"),
        "cpfDoResponsavel": findByName(contractValues, "cPF"),
        "emailDoResponsavel": findByName(contractValues, "emailDoIndicado"),
        "cargoDoResponsavel": findByName(contractValues, "profissaoDoTitular"),
        "dataDeNascimentoDoResponsavel": findByName(contractValues, "dataDeNascimento"),
        "prazoDeVigencia": findByName(contractValues, "prazoDeVigencia"),
        "closerResponsavel": findByName(contractValues, "informeOCloser"),
        "origemInterna": findByName(contractValues, "origemInterna"),
        "origemExterna": findByName(contractValues, "origemExterna"),
        "valorDaImplantacão": findByName(contractValues, "valorDeImplantacao"),
        "dataDePagamentoDaImplantacao": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "formaDePagamentoDaImplantacao": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        "fee": findByName(contractValues, "valorDoFEE"),
        "diaDeCobrançaDoFee": findByName(contractValues, "diaDeCobrançaDoFee"),
        "observacoes": findByName(contractValues, "observacao"),
        "telefoneDoConjuge": findByName(contractValues, "telefone"),
        "qualOTipoDeTrabalho": findByName(contractValues, "qualOTipoDeTrabalho"),
        "cobrancaPelaCorretora": findByName(contractValues, "autorizacaoDeCobrancaPelaCorretora"),
        "patrimonioFinanceiroEstimado": findByName(contractValues, "patrimonioFinanceiro"),
        "vincularAContratoPai": findByName(contractValues, "haveraVinculacaoContratoPai"),
        "numeroDoContratoPai": findByName(contractValues, "numeroDoContratoPai")
    }
    return clickSignVariables
