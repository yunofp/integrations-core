def extract_fields(field_mapping, response_json, response2_json):
    contractContent = {}
    for key, (source, i, j) in field_mapping.items():
        contractContent[key] = source[i].get("formFields")[j].get("value")
    return contractContent

def defineVariablesGrow(response_json, response2_json):
    field_mapping = {
        "nomeCompletoDoTitular": (response_json, 0, 2),
        "email": (response_json, 0, 48),
        "dataDeNascimento": (response2_json, 0, 1),
        "telefoneDoTitular": (response_json, 0, 47),
        "cpfDoTitular": (response_json, 0, 45),
        "endereco": (response_json, 0, 49),
        "bairro": (response_json, 0, 50),
        "cidade": (response_json, 0, 51),
        "uf": (response_json, 0, 52),
        "cep": (response_json, 0, 53),
        "nomeCompletoDoConjuge": (response_json, 0, 54),
        "emailDoConjuge": (response2_json, 0, 10),
        "dataDeNascimentoDoConjuge": (response2_json, 0, 9),
        "prazoDeVigencia": (response_json, 0, 59),
        "closerResponsavel": (response_json, 0, 0),
        "origemInterna": (response_json, 0, 60),
        "origemExterna": (response_json, 0, 61),
        "valorDaImplantacão": (response_json, 0, 63),
        "dataDePagamentoDaImplantacao": (response_json, 0, 64),
        "formaDePagamentoDaImplantacao": (response_json, 0, 65),
        "fee": (response_json, 0, 67),
        "diaDeCobrançaDoFee": (response_json, 0, 68),
        "observacoes": (response_json, 0, 72),
        "telefoneDoConjuge": (response2_json, 0, 11),
        "qualOTipoDeTrabalho": (response_json, 0, 1)
    }
    return extract_fields(field_mapping, response_json, response2_json)

def defineVariablesWealth(response_json, response2_json):
    field_mapping = {
        "nomeCompletoDoTitular": (response_json, 0, 2),
        "email": (response_json, 0, 48),
        "dataDeNascimento": (response2_json, 0, 1),
        "telefoneDoTitular": (response_json, 0, 47),
        "cpfDoTitular": (response_json, 0, 45),
        "endereco": (response_json, 0, 49),
        "bairro": (response_json, 0, 50),
        "cidade": (response_json, 0, 51),
        "uf": (response_json, 0, 52),
        "cep": (response_json, 0, 53),
        "nomeCompletoDoConjuge": (response_json, 0, 54),
        "emailDoConjuge": (response2_json, 0, 10),
        "dataDeNascimentoDoConjuge": (response2_json, 0, 9),
        "prazoDeVigencia": (response_json, 0, 59),
        "closerResponsavel": (response_json, 0, 0),
        "origemInterna": (response_json, 0, 60),
        "origemExterna": (response_json, 0, 61),
        "valorDaImplantacão": (response_json, 0, 63),
        "dataDePagamentoDaImplantacao": (response_json, 0, 64),
        "formaDePagamentoDaImplantacao": (response_json, 0, 65),
        "fee": (response_json, 0, 67),
        "diaDeCobrançaDoFee": (response_json, 0, 68),
        "observacoes": (response_json, 0, 72),
        "telefoneDoConjuge": (response2_json, 0, 11),
        "qualOTipoDeTrabalho": (response_json, 0, 1),
        "cobrancaPelaCorretora": (response2_json, 0, 18),
        "patrimonioFinanceiroEstimado": (response_json, 0, 33),
        "vincularAContratoPai": (response_json, 0, 19),
        "numeroDoContratoPai": (response_json, 0, 20)
    }
    return extract_fields(field_mapping, response_json, response2_json)

def defineVariablesWork(response_json, response2_json):
    field_mapping = {
        "nomeDaEmpresa": (response_json, 0, 44),
        "emailDeContato": (response_json, 0, 48),
        "telefoneDaEmpresa": (response_json, 0, 47),
        "cnpj": (response_json, 0, 45),
        "endereco": (response_json, 0, 49),
        "bairro": (response_json, 0, 50),
        "cidade": (response_json, 0, 51),
        "uf": (response_json, 0, 52),
        "cep": (response_json, 0, 53),
        "nomeCompletoDoResponsavel": (response_json, 0, 54),
        "cpfDoResponsavel": (response2_json, 0, 8),
        "emailDoResponsavel": (response2_json, 0, 10),
        "cargoDoResponsavel": (response_json, 0, 38),
        "dataDeNascimentoDoResponsavel": (response2_json, 0, 9),
        "prazoDeVigencia": (response_json, 0, 59),
        "closerResponsavel": (response_json, 0, 0),
        "origemInterna": (response_json, 0, 60),
        "origemExterna": (response_json, 0, 61),
        "valorDaImplantacão": (response_json, 0, 63),
        "dataDePagamentoDaImplantacao": (response_json, 0, 64),
        "formaDePagamentoDaImplantacao": (response_json, 0, 65),
        "fee": (response_json, 0, 67),
        "diaDeCobrançaDoFee": (response_json, 0, 68),
        "observacoes": (response_json, 0, 72),
        "telefoneDoConjuge": (response2_json, 0, 11),
        "qualOTipoDeTrabalho": (response_json, 0, 1),
        "cobrancaPelaCorretora": (response2_json, 0, 18),
        "patrimonioFinanceiroEstimado": (response_json, 0, 33),
        "vincularAContratoPai": (response_json, 0, 19),
        "numeroDoContratoPai": (response_json, 0, 20)
    }
    return extract_fields(field_mapping, response_json, response2_json)
