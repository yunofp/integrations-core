import sys
from ..utils import formatting
import pandas as pd
from datetime import datetime, timezone

def clean_none_values(data):
    cleaned = {k: v for k, v in data.items() if v is not None}
    return cleaned

def get_cell_content(df, row, column):
    content = None
    if isinstance(column, str):
        content = df.loc[row, column]
    else:
        content = df.iloc[row, column]

    if pd.isna(content) or content is "-" or content is "R$ -": 
        content = None
        
    return content 



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

def get_debt_day(df, index):
    content = get_cell_content(df, index, 'Cobrança Mensal no Dia')
    
    if pd.isnull(content):
        return 0  # Se o conteúdo for nulo, retorne 0
    
    if isinstance(content, str) and not content.isdigit():
        return content  # Se for uma string não numérica, retorne a string
    
    try:
        return int(content)  # Tente converter para inteiro se for possível
    except ValueError:
        return content  # Se falhar, retorne o conteúdo original

def create_contract_dict(index, code, df, profile_id):
    df.columns = df.columns.str.strip()
    print(df.head())

    contract = {}
    debt_day = get_debt_day(df, index)

    contract["code"] = code
    contract["closer"] = get_cell_content(df, index, 'Closer')
    contract["profile_id"] = profile_id
    contract['source_acquisition'] = add_source_acquisition(get_cell_content(df, index, 'Canal de Aquisição'))
    contract['status'] = "A definir" if pd.isnull(get_cell_content(df, index, 1)) else get_cell_content(df, index, 1)
    contract["type"] = get_cell_content(df, index, 'Contrato')
    print('aquiiiiii', index)
    contract["aum"] = {
        "estimated" : formatting.extract_numbers_as_double(get_cell_content(df, index, 'AUM Estimado')),
        "actual" : formatting.extract_numbers_as_double(get_cell_content(df, index, 'AUM Estimado'))
    }
    contract["implantation"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 'Implantação'))
    contract["first_implantation_payment_date"] = formatting.convert_to_utc_date(get_cell_content(df, index, 'Data do Primeiro Pagamento da Implantação'))
    contract["first_payment_date"] = formatting.convert_to_utc_date(get_cell_content(df, index, 'Data do Primeiro Pagamento da Implantação'))
    contract["implantation_payment_method"] = get_cell_content(df, index, 'Forma de Pagamento do FEE')
    implantation_installment = get_cell_content(df, index, 'Parcelamento da Implantação')
    
    if pd.isna(implantation_installment) or implantation_installment == "-":
        contract["implantation_installment"] = 0
    else:
        contract["implantation_installment"] = int(implantation_installment)
    
    contract["minimal_fee"] = formatting.extract_numbers_as_double(get_cell_content(df, index, 'Fee Mínimo'))
    contract["deadline"] = get_cell_content(df, index, 'Vigência (meses)')
    contract["debt_day"] = debt_day
    if get_cell_content(df, index, 'Autorização de Cobrança Pela Corretora') == "NÃO": 
        contract["broker_permission"] = False
    else:
        contract["broker_permission"] = True
    
    contract["root_contract_code"] = "" if get_cell_content(df, index, 'Vinculação Contrato Pai') == "0" else get_cell_content(df, index, 'Vinculação Contrato Pai')
    contract["account"] = {
        "number": 0 if pd.isnull(get_cell_content(df, index, 43)) else get_cell_content(df, index, 43),
        "cpf_cnpj": formatting.clear_cpf(get_cell_content(df, index, 'CPF / CPNJ'))
    }
    return clean_none_values(contract)

def create_profile_dict(index, df, code):
    maritalStatus = verify_work_contract(df, index)
    profile = {}
    profile["name"] = get_cell_content(df, index, 'Nome do Cliente')
    profile["email"] = get_cell_content(df, index, 'Email')
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
    consenting_cpf = get_cell_content(df, index, 'CPF do Anuente')
    if pd.isna(consenting_cpf) or consenting_cpf == "-":
        consenting_cpf = None
    else:
        consenting_cpf = formatting.clear_cpf(consenting_cpf)
    profile["consenting"] = {
        "name": get_cell_content(df, index, 'Nome do Cônjuge/Responsável da Empresa'),
        "email": get_cell_content(df, index, 'Email Anuente'),
        "birthdate": formatting.convert_to_utc_date(get_cell_content(df, index, 'Data de Nascimento do Anuente')),
        "phone": formatting.clean_numbers(get_cell_content(df, index, 'Telefone do Anuente')),
        "cpf": consenting_cpf
    }

    return clean_none_values(profile)

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
    print('aquiiiiiiii', index)
    entry["aum"] = {
        # "estimated": formatting.processing_number_insert(get_cell_content(df, index, "AUM Estimado")),
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

    return clean_none_values(entry)
