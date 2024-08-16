import sys
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
    contracts["firstPaymentDate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 'Data do Primeiro Pagamento da Implantação'))
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

def create_profile_dict(index, df, code):
    maritalStatus = verify_work_contract(df, index)
    profile = {}
    profile["name"] = get_cell_content(df, index, 'Nome do Cliente')
    profile["email"] = get_cell_content(df, index, 6)
    profile["birthdate"] = formatting.convert_to_utc_date(get_cell_content(df, index, 'Data de Nascimento'))
    profile["phone"] = formatting.clean_numbers(get_cell_content(df, index, 'Telefone'))
    profile["cpf_cnpj"] = formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    profile["job_position"] = ""
    profile["address"] = get_cell_content(df, index, 'Endereço')
    profile["neighborhood"] = get_cell_content(df, index, 'Bairro')
    profile["zip_code"] = formatting.clean_numbers(get_cell_content(df, index, 'CEP'))
    profile["city"] = get_cell_content(df, index, 'Cidade')
    profile["state"] = get_cell_content(df, index, 'UF')
    profile["financial_assets"] = 0.0
    profile["budget_profile"] = "" 
    profile["residence_property"] = ""
    profile["marital_status"] = maritalStatus
    profile["primary_profession"] = ""
    profile["business_sector"] = ""
    profile["consenting"] = {
        "name": get_cell_content(df, index, 'Nome do Cônjuge/Responsável da Empresa'),
        "email": get_cell_content(df, index, 'Email Anuente'),
        "birthdate": formatting.convert_to_utc_date(get_cell_content(df, index, 'Data de Nascimento do Anuente')),
        "phone": get_cell_content(df, index, 'Telefone do Anuente'),
        "cpf": get_cell_content(df, index, 'CPF do Anuente')
    }

    return profile

def create_entry_dict(month_year,index, df, code, month_year_index, contract_id, aum_index, mrr_index, planner_name_index, status_index, imp_payment_index, paid_mrr_index, cancel_day_index):
    entry = {}
    pay_date = formatting.convert_to_utc_date(formatting.format_date(month_year))
    due_date = pay_date
    value = formatting.clean_currency_string_to_double(get_cell_content(df, index, paid_mrr_index))
    entry["contract_id"] = contract_id
    entry["code"] = code
    entry["payer"] = {
        "name": get_cell_content(df, index, 'Nome do Cliente'),
        "cpf": formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    }
    planner_name = "DESCONHECIDO" if get_cell_content(df, index, planner_name_index) == "INATIVO" else get_cell_content(df, index, planner_name_index)
    entry["planners"] = [{"name": planner_name}]
    entry["aum"] = {
        "estimated": formatting.processing_number_insert(get_cell_content(df, index, "AUM Estimado")),
        "actual": formatting.processing_number_insert(get_cell_content(df, index, aum_index))
    }
    entry["due_date"] = due_date
    entry["payment_date"] = pay_date 
    entry["value"] = value
    entry["implemented_payment"] = formatting.clean_currency_string_to_double(get_cell_content(df, index, imp_payment_index))
    entry["status"] = "approved" if value > 0 else "pending"
    entry["currency"] = "BRL"
    entry["created_at"] = datetime.now(timezone.utc)
    entry["payment_method"] = get_cell_content(df, index, "Forma de Pagamento do FEE")
    entry["income"] = ""
    entry["budget_profile"] = ""
    cancel_day = get_cell_content(df, index, cancel_day_index)
    entry["cancel_day"] = ""
    if isinstance(cancel_day, str) and cancel_day.strip():
        entry["cancel_day"] = cancel_day
    return entry
