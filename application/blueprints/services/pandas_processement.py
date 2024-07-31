from ..utils import formatting
import pandas as pd
from datetime import datetime, timezone

def get_cell_content(df, row, column):
    return df.iloc[row][column]

def verify_work_contract(df, index):
    contract = get_cell_content(df, index, 'Contrato')
    responsible_name = get_cell_content(df, index, 'Nome do Cônjuge/Responsável da Empresa')

    if contract != 'work':
        if pd.isna(responsible_name) or responsible_name == '-':
            return False
        else:
            return True
    else:
        return ""

def add_source_acquisition(source_acquisition_type):
    source_acquisition_enum = {
        'INDICAÇÃO INTERNA': 1,
        'INDICAÇÃO EXTERNA': 2,
        'FINDER': 3,
        'MARKETING': 4,
        'PROSPECÇÃO ATIVA': 5,
        'EVENTO': 6,
        'NÃO ESPECIFICADO': 0
    }

    source_acquisition_value = source_acquisition_enum.get(source_acquisition_type, 0)

    return source_acquisition_value

def create_contract_dict(index, cod, df, profile_id):
    contracts = {}
    debt_day = get_cell_content(df, index, 27)
    #add_source_acquisition(contracts)

    contracts["cod"] = cod
    contracts["closer"] = get_cell_content(df, index, 'Closer')
    contracts["profileId"] = profile_id

    # ORIGEM INTERNA E EXTERNA 
    #contracts["internalOrigin"] = 1
    #contracts["externalOrigin"] = 0

    contracts['status'] = "DESCONHECIDO" if pd.isnull(get_cell_content(df, index, 1)) else get_cell_content(df, index, 1)
    contracts["contractType"] = get_cell_content(df, index, 'Contrato')

    # VALORES
    contracts["aum.estimated"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 34))
    contracts["aum.actual"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 34))
    #contracts["mrr"] = 
    contracts["implantation"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 26))
    #contracts["implantationPaymentDate"] = 
    contracts["firstPaymentDate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 27))
    contracts["implantationPaymentMethod"] = get_cell_content(df, index, 'Forma de Pagamento do FEE')
    contracts["implantationInstallment"] = int(get_cell_content(df, index, 'Parcelamento da Implantação'))
    contracts["minimalFee"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 29))
    contracts["deadline"] = get_cell_content(df, index, 'Vigência (meses)')
    contracts["debtDay"] = debt_day[:2]
    #contracts["averageMonthlyIncome"] = get_cell_content(df, index, '')


    if get_cell_content(df, index, 'Autorização de Cobrança Pela Corretora') == "NÃO": 
        contracts["brokerPermission"] = False
    else:
        contracts["brokerPermission"] = True
    
    contracts["rootContractCode"] = "" if get_cell_content(df, index, 'Vinculação Contrato Pai') == "0" else get_cell_content(df, index, 'Vinculação Contrato Pai')
    contracts["accountNumber.cpf"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    contracts['sourceAcquisition'] = add_source_acquisition(get_cell_content(df, index, 'Canal de Aquisição'))
    #contracts["accountNumber.accountNum"] = get_cell_content(df, index, 'CPF / CPNJ')
    #contracts["cancelDate"] = get_cell_content(df, index, 'Vigência (meses)')
    #contracts["signedAt"] = "1/"
    #contracts["comments"] = 

    return contracts

def create_payment_dict(index, df, mmaaaa, profile_dict, contract_dict, status):
    dueDate = get_cell_content(df, index, 27)
    payments = {}
    payments["cod"] = contract_dict['cod']
    payments["payer.name"] = get_cell_content(df, index, 'Nome do Cliente')
    payments["payer.CPFCNPJ"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    payments["value"] = contract_dict['minimalFee']
    payments["dueDate"] = dueDate[:2] + "/" + mmaaaa
    payments["status"] = get_cell_content(df, index, status)
    payments["currency"] = "BRL"
    payments["createdAt"] = datetime.now(timezone.utc)
    payments["paymentMethod"] = get_cell_content(df, index, 'Forma de Pagamento do FEE')
    #payments["contractId"] = get_cell_content(df, index, 'Data do Primeiro Pagamento da Implantação')

    return payments

def create_profile_dict(index, df, cod):
    maritalStatus = verify_work_contract(df, index)
    profile = {}
    #profile["cod"] = cod
    profile["name"] = get_cell_content(df, index, 'Nome do Cliente')
    profile["email"] = get_cell_content(df, index, 6)
    profile["birthdate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 'Data de Nascimento'))
    profile["phone"] = formatting.clean_numbers(get_cell_content(df, index, 'Telefone'))
    profile["cpfcnpj"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    profile["jobPosition"] = ""
    profile["address"] = get_cell_content(df, index, 'Endereço')
    profile["neighborhood"] = get_cell_content(df, index, 'Bairro')
    profile["zipCode"] = formatting.clean_numbers(get_cell_content(df, index, 'CEP'))
    profile["city"] = get_cell_content(df, index, 'Cidade')
    profile["state"] = get_cell_content(df, index, 'UF')
    #profile["type"] = ""
    profile["financialAssets"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, 34))
    profile["budgetProfile"] = "" if pd.isna(get_cell_content(df, index, 39)) else get_cell_content(df, index, 39)
    profile["residenceProperty"] = ""
    profile["maritalStatus"] = maritalStatus
    profile["primaryProfession"] = ""
    profile["businessSector"] = ""
    profile["consenting.name"] = get_cell_content(df, index, 'Nome do Cônjuge/Responsável da Empresa')
    profile["consenting.email"] = get_cell_content(df, index, 17)
    profile["consenting.birthdate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 18))
    profile["consenting.phone"] = get_cell_content(df, index, 19)
    profile["consenting.cpfCnpj"] = get_cell_content(df, index, 20)

    return profile

def create_extract_dict(index, df, cod, mmaaaa, paymentId, contractId, aum_pos, mrr_pos, planner_name_pos, status_pos, imp_payment_pos, paid_mrr_pos, cancel_day_pos):
    extract = {}
    payDate = get_cell_content(df, index, 27)
    dueDate = get_cell_content(df, index, 27)
    extract["paymentId"] = paymentId
    extract["cod"] = cod
    extract["payer.name"] = get_cell_content(df, index, 'Nome do Cliente')
    extract["payer.CNPJCPF"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    extract["planners.name"] = "DESCONHECIDO" if get_cell_content(df, index, planner_name_pos) == "INATIVO" else get_cell_content(df, index, planner_name_pos)
    #extract["planners[0].cpf"] = get_cell_content(df, index, 'CPF do Planejador')
    #extract["contractId"] = contractId
    extract["aum.estimated"] = formatting.processing_number_insert(get_cell_content(df, index, aum_pos))
    extract["aum.actual"] = formatting.processing_number_insert(get_cell_content(df, index, aum_pos))
    extract["mrr"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, mrr_pos))
    extract["dueDate"] = dueDate[:2] + "/" + mmaaaa
    #extract["paidMrr"] = formatting.clean_currency_string_to_double(paid_mrr_pos)
    extract["paymentDate"] = payDate[:2] + "/" + mmaaaa
    extract["value"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, 29))
    extract["implementedPayment"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, imp_payment_pos))
    extract["status"] = get_cell_content(df, index, status_pos)
    extract["currency"] = "BRL"
    extract["createdAt"] = datetime.now(timezone.utc)
    extract["paymentMethod"] = get_cell_content(df, index, 30)
    extract["income"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, 38))
    extract["budgetProfile"] = "" if pd.isna(get_cell_content(df, index, 39)) else get_cell_content(df, index, 39)
    #extract["suitability"] = get_cell_content(df, index, 'Adequação')
    if not get_cell_content(df, index, cancel_day_pos) == "INATIVO":
        extract["cancelDay"] = get_cell_content(df, index, cancel_day_pos)

    return extract
