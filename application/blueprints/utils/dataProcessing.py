def findByName(list, name): 
    objectFound = next((item for item in list if item["name"] == name), '')
    if not objectFound:
        return ""
    return objectFound['value']

def defineVariablesGrow(contractValues):
    clickSignVariables = {
        "Nome Completo do Titular": findByName(contractValues, "nomeDoCliente-Llaz"),
        "Email": findByName(contractValues, "emailDoCliente"),
        "Data de Nascimento": findByName(contractValues, "dataDeNascimentoDoTitular"),
        "Telefone do Titular": findByName(contractValues, "contatoDoCliente"),
        "CPF do Titular": findByName(contractValues, "cPFCPNJ"),
        "Endereço": findByName(contractValues, "endereco"),
        "Bairro": findByName(contractValues, "bairro"),
        "Cidade": findByName(contractValues, "cidade"),
        "UF": findByName(contractValues, "uF"),
        "CEP": findByName(contractValues, "cEP"),
        "Nome Completo do Cônjuge": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "Email do Cônjuge": findByName(contractValues, "email"),
        "Data de Nascimento do Cônjuge": findByName(contractValues, "dataDeNascimento"),
        "Telefone do Cônjuge": findByName(contractValues, "telefone"),
        "Prazo de Vigência": findByName(contractValues, "prazoDeVigencia"),
        "Closer Responsável": findByName(contractValues, "responsavelPelaContratacao") or findByName(contractValues, "informeOCloser"),
        "Origem Interna": findByName(contractValues, "origemInterna"),
        "Origem Externa": findByName(contractValues, "origemExterna"),
        "Valor da Implantação": findByName(contractValues, "valorDeImplantacao"),
        "Data do Pagamento da Implantação": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "Forma de Pagamento da Implantação": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        "Fee": findByName(contractValues, "valorDoFEE"),
        "Dia da Cobrança do Fee": findByName(contractValues, "diaDaCobrancaRecorrente"),
        "Observações": findByName(contractValues, "observacao") or findByName(contractValues, "obervacao")
    }
    return clickSignVariables

def defineVariablesWealth(contractValues):
    
    clickSignVariablesGrow = defineVariablesGrow(contractValues)
    clickSignVariablesWealth = {
        "Cobrança pela Corretora": findByName(contractValues, "autorizacaoDeCobrancaPelaCorretora"),
        "Patrimônio Financeiro Estimado": findByName(contractValues, "patrimonioFinanceiro"),
        "Vincular à contrato pai?": findByName(contractValues, "haveraVinculacaoContratoPai"),
        "Número do Contrato Pai": findByName(contractValues, "numeroDoContratoPai")
    }
    
    clickSignVariables = {**clickSignVariablesGrow, **clickSignVariablesWealth}
    return clickSignVariables

def defineVariablesWork(contractValues):
    
    clickSignVariables = {
        "Nome da Empresa": findByName(contractValues, "nomeDoCliente-Llaz"),
        "Email de Contato": findByName(contractValues, "emailDoCliente"),
        "Telefone da Empresa": findByName(contractValues, "contatoDoCliente"),
        "CNPJ": findByName(contractValues, "cPFCPNJ"),
        "Endereço": findByName(contractValues, "endereco"),
        "Bairro": findByName(contractValues, "bairro"),
        "Cidade": findByName(contractValues, "cidade"),
        "UF": findByName(contractValues, "uF"),
        "CEP": findByName(contractValues, "cEP"),
        "Nome Completo do Responsável": findByName(contractValues, "nomeDoConjugeResponsavelPelaEmpresa"),
        "Cargo do Responsável": findByName(contractValues, "profissaoDoTitular"),
        "Email do Responsável": findByName(contractValues, "emailDoCliente"),
        "Data de Nascimento do Responsável": findByName(contractValues, "dataDeNascimentoDoTitular"),
        "CPF do Responsável": findByName(contractValues, "cPF"),
        "Telefone do Responsável": findByName(contractValues, "telefone") or findByName(contractValues, "contatoDoCliente"),
        
        "Prazo de Vigência": findByName(contractValues, "prazoDeVigencia"),
        "Closer Responsável": findByName(contractValues, "responsavelPelaContratacao") or findByName(contractValues, "informeOCloser"),
        "Origem Interna": findByName(contractValues, "origemInterna"),
        "Origem Externa": findByName(contractValues, "origemExterna"),
        
        "Valor da Implantação": findByName(contractValues, "valorDeImplantacao"),
        "Data do Pagamento da Implantação": findByName(contractValues, "dataDoPagamentoDaImplantacao"),
        "Forma de Pagamento da Implantação": findByName(contractValues, "formaDePagamentoDaImplantacao"),
        
        "Fee": findByName(contractValues, "valorDoFEE"),
        "Dia da Cobrança do Fee": findByName(contractValues, "diaDaCobrancaRecorrente"),
        "Observações": findByName(contractValues, "observacao") or findByName(contractValues, "obervacao"),
    }
    return clickSignVariables
