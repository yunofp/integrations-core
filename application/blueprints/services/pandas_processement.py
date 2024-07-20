from ..utils import formatting
import pandas as pd
from datetime import datetime, timezone

def verify_work_contract(df, index):
    contract = df.iloc[index]['Contrato']
    responsible_name = df.iloc[index]['Nome do Cônjuge/Responsável da Empresa']

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
    debt_day = df.iloc[index, 27]
    #add_source_acquisition(contracts)

    contracts["cod"] = cod
    contracts["closer"] = df.iloc[index]['Closer']
    contracts["profileId"] = profile_id

    # ORIGEM INTERNA E EXTERNA 
    #contracts["internalOrigin"] = 1
    #contracts["externalOrigin"] = 0

    contracts["status"] = df.iloc[index, 1]
    contracts["contractType"] = df.iloc[index]['Contrato']

    # VALORES
    contracts["aum.estimated"] = formatting.extract_numbers_as_double(df.iloc[index, 34])
    contracts["aum.actual"] = formatting.extract_numbers_as_double(df.iloc[index, 34])
    #contracts["mrr"] = 
    contracts["implantation"] = formatting.extract_numbers_as_double(df.iloc[index, 26])
    #contracts["implantationPaymentDate"] = 
    contracts["firstPaymentDate"] = formatting.convert_to_utc_date(df.iloc[index, 27])
    contracts["implantationPaymentMethod"] = df.iloc[index]['Forma de Pagamento do FEE']
    contracts["implantationInstallment"] = int(df.iloc[index]['Parcelamento da Implantação'])
    contracts["minimalFee"] = formatting.extract_numbers_as_double(df.iloc[index, 29])
    contracts["deadline"] = df.iloc[index]['Vigência (meses)']
    contracts["debtDay"] = debt_day[:2]
    #contracts["averageMonthlyIncome"] = df.iloc[index]['']


    if df.iloc[index]['Autorização de Cobrança Pela Corretora'] == "NÃO": 
      contracts["brokerPermission"] = False
    else:
      contracts["brokerPermission"] = True
    
    contracts["rootContractCode"] = "" if df.iloc[index]['Vinculação Contrato Pai'] == "0" else df.iloc[index]['Vinculação Contrato Pai']
    contracts["accountNumber.cpf"] = formatting.clear_cpf(df.iloc[index]['CPF / CPNJ'])
    contracts['sourceAcquisition'] = add_source_acquisition(df.iloc[index]['Canal de Aquisição'])
    #contracts["accountNumber.accountNum"] = df.iloc[index]['CPF / CPNJ']
    #contracts["cancelDate"] = df.iloc[index]['Vigência (meses)']
    #contracts["signedAt"] = "1/"
    #contracts["comments"] = 

    return contracts

def create_payment_dict(index, df, mmaaaa, profile_dict, contract_dict, status):
    dueDate = df.iloc[index, 27]
    payments = {}
    payments["cod"] = contract_dict['cod']
    payments["payer.name"] = df.iloc[index]['Nome do Cliente']
    payments["payer.CPFCNPJ"] = formatting.clear_cpf(df.iloc[index]['CPF / CPNJ'])
    payments["value"] = contract_dict['minimalFee']
    payments["dueDate"] = dueDate[:2] + "/" + mmaaaa
    payments["status"] = df.iloc[index][status]
    payments["currency"] = "BRL"
    payments["createdAt"] = datetime.now(timezone.utc)
    payments["paymentMethod"] = df.iloc[index]['Forma de Pagamento do FEE']
    #payments["contractId"] = df.iloc[index]['Data do Primeiro Pagamento da Implantação']

    return payments

def create_profile_dict(index, df, cod):
     maritalStatus = verify_work_contract(df, index)
     profile = {}
     #profile["cod"] = cod
     profile["name"] = df.iloc[index]['Nome do Cliente']
     profile["email"] = df.iloc[index, 6]
     profile["birthdate"] = formatting.convert_to_utc_date(df.iloc[index]['Data de Nascimento'])
     profile["phone"] = formatting.clean_numbers(df.iloc[index]['Telefone'])
     profile["cpfcnpj"] = formatting.clear_cpf(df.iloc[index]['CPF / CPNJ'])
     profile["jobPosition"] = ""
     profile["address"] = df.iloc[index]['Endereço']
     profile["neighborhood"] = df.iloc[index]['Bairro']
     profile["zipCode"] = formatting.clean_numbers(df.iloc[index]['CEP'])
     profile["city"] = df.iloc[index]['Cidade']
     profile["state"] = df.iloc[index]['UF']
     #profile["type"] = ""
     profile["financialAssets"] = formatting.clean_currency_string_to_double(df.iloc[index, 34])
     profile["budgetProfile"] = "" if pd.isna(df.iloc[index, 39]) else df.iloc[index, 39]
     profile["residenceProperty"] = ""
     profile["maritalStatus"] = maritalStatus
     profile["primaryProfession"] = ""
     profile["businessSector"] = ""
     profile["consenting.name"] = df.iloc[index]['Nome do Cônjuge/Responsável da Empresa']
     profile["consenting.email"] = df.iloc[index, 17]
     profile["consenting.birthdate"] = formatting.convert_to_utc_date(df.iloc[index, 18])
     profile["consenting.phone"] = df.iloc[index, 19]
     profile["consenting.cpfCnpj"] = df.iloc[index, 20]

     return profile

def create_extract_dict(index, df, cod, mmaaaa, paymentId, contractId, aum_pos, mrr_pos, planner_name_pos, status_pos, imp_payment_pos, paid_mrr_pos, cancel_day_pos):
    extract = {}
    payDate = df.iloc[index, 27]
    dueDate = df.iloc[index, 27]
    extract["paymentId"] = paymentId
    extract["cod"] = cod
    extract["payer.name"] = df.iloc[index]['Nome do Cliente']
    extract["payer.CNPJCPF"] = formatting.clear_cpf(df.iloc[index]['CPF / CPNJ'])
    extract["planners.name"] = "DESCONHECIDO" if df.iloc[index, planner_name_pos] == "INATIVO" else df.iloc[index, planner_name_pos]
    #extract["planners[0].cpf"] = df.iloc[index]['CPF do Planejador']
    #extract["contractId"] = contractId
    extract["aum.estimated"] = formatting.processing_number_insert(df.iloc[index][aum_pos])
    extract["aum.actual"] = formatting.processing_number_insert(df.iloc[index][aum_pos])
    extract["mrr"] = formatting.clean_currency_string_to_double(df.iloc[index][mrr_pos])
    extract["dueDate"] = dueDate[:2] + "/" + mmaaaa
    #extract["paidMrr"] = formatting.clean_currency_string_to_double(paid_mrr_pos)
    extract["paymentDate"] = payDate[:2] + "/" + mmaaaa
    extract["value"] = formatting.clean_currency_string_to_double(df.iloc[index, 29])
    extract["implementedPayment"] = formatting.clean_currency_string_to_double(df.iloc[index, imp_payment_pos])
    extract["status"] = df.iloc[index][status_pos]
    extract["currency"] = "BRL"
    extract["createdAt"] = datetime.now(timezone.utc)
    extract["paymentMethod"] = df.iloc[index, 30]
    extract["income"] = formatting.clean_currency_string_to_double(df.iloc[index, 38])
    extract["budgetProfile"] = "" if pd.isna(df.iloc[index, 39]) else df.iloc[index, 39]
    #extract["suitability"] = df.iloc[index]['Adequação']
    if not df.iloc[index, cancel_day_pos] == "INATIVO":
        extract["cancelDay"] = df.iloc[index, cancel_day_pos]

    return extract