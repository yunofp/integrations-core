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

def create_contract_dict(index, code, df, profile_id):
    contracts = {}
    debt_day = get_cell_content(df, index, 27)

    contracts["code"] = code
    contracts["closer"] = get_cell_content(df, index, 'Closer')
    contracts["profileId"] = profile_id

    contracts['status'] = "DESCONHECIDO" if pd.isnull(get_cell_content(df, index, 1)) else get_cell_content(df, index, 1)
    contracts["contractType"] = get_cell_content(df, index, 'Contrato')

    contracts["aum.estimated"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 34))
    contracts["aum.actual"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 34))
    contracts["implantation"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 26))
    contracts["firstPaymentDate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 27))
    contracts["implantationPaymentMethod"] = get_cell_content(df, index, 'Forma de Pagamento do FEE')
    contracts["implantationInstallment"] = int(get_cell_content(df, index, 'Parcelamento da Implantação'))
    contracts["minimalFee"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 29))
    contracts["deadline"] = get_cell_content(df, index, 'Vigência (meses)')
    contracts["debtDay"] = debt_day[:2]
    if get_cell_content(df, index, 'Autorização de Cobrança Pela Corretora') == "NÃO": 
        contracts["brokerPermission"] = False
    else:
        contracts["brokerPermission"] = True
    
    contracts["rootContractCode"] = "" if get_cell_content(df, index, 'Vinculação Contrato Pai') == "0" else get_cell_content(df, index, 'Vinculação Contrato Pai')
    contracts["accountNumber.cpf"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    contracts['sourceAcquisition'] = add_source_acquisition(get_cell_content(df, index, 'Canal de Aquisição'))

    return contracts

def create_payment_dict(index, df, mmaaaa, profile_dict, contract_dict, status):
    dueDate = get_cell_content(df, index, 27)
    payments = {}
    payments["code"] = contract_dict['code']
    payments["payer.name"] = get_cell_content(df, index, 'Nome do Cliente')
    payments["payer.CPFCNPJ"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    payments["value"] = contract_dict['minimalFee']
    payments["dueDate"] = dueDate[:2] + "/" + mmaaaa
    payments["status"] = get_cell_content(df, index, status)
    payments["currency"] = "BRL"
    payments["createdAt"] = datetime.now(timezone.utc)
    payments["paymentMethod"] = get_cell_content(df, index, 'Forma de Pagamento do FEE')

    return payments

def create_profile_dict(index, df, code):
    maritalStatus = verify_work_contract(df, index)
    profile = {}
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

def create_entry_dict(index, df, code, mmaaaa, paymentId, contractId, aum_pos, mrr_pos, planner_name_pos, status_pos, imp_payment_pos, paid_mrr_pos, cancel_day_pos):
    entry = {}
    payDate = get_cell_content(df, index, 27)
    dueDate = get_cell_content(df, index, 27)
    entry["paymentId"] = paymentId
    entry["code"] = code
    entry["payer.name"] = get_cell_content(df, index, 'Nome do Cliente')
    entry["payer.CNPJCPF"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    entry["planners.name"] = "DESCONHECIDO" if get_cell_content(df, index, planner_name_pos) == "INATIVO" else get_cell_content(df, index, planner_name_pos)
    entry["aum.estimated"] = formatting.processing_number_insert(get_cell_content(df, index, aum_pos))
    entry["aum.actual"] = formatting.processing_number_insert(get_cell_content(df, index, aum_pos))
    entry["mrr"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, mrr_pos))
    entry["dueDate"] = formatting.convert_to_utc_date(dueDate[:2] + "/" + mmaaaa) if payDate != "-" else "01" + "/" + mmaaaa
    entry["paymentDate"] = payDate[:2] + "/" + mmaaaa
    entry["value"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, 29))
    entry["implementedPayment"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, imp_payment_pos))
    entry["status"] = get_cell_content(df, index, status_pos)
    entry["currency"] = "BRL"
    entry["createdAt"] = datetime.now(timezone.utc)
    entry["paymentMethod"] = get_cell_content(df, index, 30)
    entry["income"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, 38))
    entry["budgetProfile"] = "" if pd.isna(get_cell_content(df, index, 39)) else get_cell_content(df, index, 39)
    if not get_cell_content(df, index, cancel_day_pos) == "INATIVO":
        entry["cancelDay"] = get_cell_content(df, index, cancel_day_pos)

    return entry
