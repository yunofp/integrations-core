import pytz
from datetime import datetime
import pandas as pd
import re

def convert_to_utc_date(date_str):  
    if not date_str or date_str == "-" or pd.isna(date_str) or date_str == 0 or date_str == "0" or date_str == None: 
        return None
    
    if len(date_str) == 8 and date_str.isdigit():
        date_str = f"{date_str[:2]}-{date_str[2:4]}-{date_str[4:]}"
    date_str = date_str.replace("/", "-")
    
    br_tz = pytz.timezone('America/Sao_Paulo')
    
    for date_format in ("%d-%m-%Y", "%d-%m-%y", "%d%m-%Y", "%d%m-%y", "%d-%m-%y"):
        try:
            date = datetime.strptime(date_str, date_format)
            date_br = br_tz.localize(date)
            date_utc = date_br.astimezone(pytz.UTC)
            
            return date_utc
        except ValueError:
            continue 
    raise ValueError(f"Unknown date format: {date_str}")


def formatCpf(num):
    if not num: return num
    if len(num) == 14:
        if '.' in num or '/' in num or '-' in num:
            return num
        else:
            cnpj = '{}.{}.{}/{}-{}'.format(num[:2], num[2:5], num[5:8], num[8:12], num[12:])
            return cnpj
    elif len(num) == 11:
        cpf = '{}.{}.{}-{}'.format(num[:3], num[3:6], num[6:9], num[9:])
        return cpf
    else:
        return num

def clear_cpf(cpf):
    if not cpf: return None
    return ''.join(c for c in cpf if c.isdigit())

def formatBirthdate(data):
    if not data: return data
    dd, mm, aaaa = data.split('/')
    return f'{aaaa}-{mm}-{dd}'


def clearPhoneNum(string):
    if not string: return string
    toRemove = ['(', ')', '-']
    for caractere in toRemove:
        string = string.replace(caractere, '')
    return string

def formatFileName(serviceType, contractValues):
    clientName = ''
    if serviceType == 'Grow' or serviceType == 'Wealth' or serviceType == 'Wealth & Grow':
        clientName = contractValues.get("Nome Completo do Titular")
    if serviceType == 'Work': 
        clientName = contractValues.get("Nome da Empresa")   
    filename =  "[Integração] Contrato" + " " + str(serviceType) + " - " + str(clientName) + ".docx"
    return filename


def formatServiceType(service):
    
    serviceTypeString = service.lower()

    if "grow" in serviceTypeString and "wealth" not in serviceTypeString:
        serviceType = "Grow"
    elif "wealth" in serviceTypeString and "grow" not in serviceTypeString:
        serviceType = "Wealth"
    elif "work" in serviceTypeString:
        serviceType = "Work"
    elif "grow" in serviceTypeString and "wealth" in serviceTypeString:
        serviceType = "Grow & Wealth"
    
    return serviceType

def verifyCpfCnpj(document):
    numeric_document = ''.join(filter(str.isdigit, document))
    
    if len(numeric_document) == 11:
        return numeric_document
    elif len(numeric_document) == 14:
        return numeric_document
    else:
        return "INVALID"

def extract_numbers_as_double(s):
    if not s or 'R$' not in s:
        return 0.0
    
    filtered_numbers = s.replace('R$', '').strip()
    
    filtered_numbers = filtered_numbers.replace('.', '').replace(',', '.')
    
    if not filtered_numbers or filtered_numbers == '-' or not filtered_numbers.replace('.', '', 1).isdigit():
        return 0.0

    return float(filtered_numbers)

def clean_currency_string_to_double(currency_str):
    # Substitui valores específicos por "0" e remove símbolos indesejados
    cleaned_str = str(currency_str).replace("INATIVO", "0").replace("nan", "0").replace('R$', '').replace('-', "").strip()
    
    # Remove espaços em branco
    cleaned_str = re.sub(r'\s+', '', cleaned_str)
    
    # Remove pontos usados como separadores de milhar
    cleaned_str = cleaned_str.replace('.', '')
    
    # Substitui a primeira vírgula encontrada por ponto, para usar como separador decimal
    cleaned_str = re.sub(r',', '.', cleaned_str, count=1)
    
    # Remove quaisquer outras vírgulas
    cleaned_str = cleaned_str.replace(',', '')
    
    # Verifica se a string está vazia ou é None após todas as limpezas
    if not cleaned_str or cleaned_str == 'None':
        return 0.0
    

    return float(cleaned_str)
  


def processing_number_insert(value):
    invalid_values = ["-", "R$ -", "", "INATIVO", "nan", "NaN", "null", None]

    if value in invalid_values:
        return 0
    else:
        return clean_currency_string_to_double(value)
    
def format_date(cell, day="01", format="yyyy-mm-dd"):
    cell = str(cell) 
    ftd = cell[:3].lower()

    months = {
        'jan': '01',
        'fev': '02',
        'mar': '03',
        'abr': '04',
        'mai': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'set': '09',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }

    if ftd in months:
        mm = months[ftd]
        year = cell[-4:]
        return f"{day}/{mm}/{year}"
    else:
        raise "Invalid cell value!"
    
def generate_code(df, index):
        contract_type = df.iloc[index]['Contrato']
        if contract_type == 'GROW':
            first_digit = '1'
        elif contract_type == 'WEALTH':
            first_digit = '2'
        elif contract_type == 'WORK':
            first_digit = '3'
        else:
            raise ValueError(f"Invalid contract type: {contract_type}")

        closer_name = df.iloc[index]['Closer']
        if closer_name in ['BRUNO DEOR', 'MAX MULLER']:
            second_digit = '2'
        else:
            second_digit = '1'

        next_sequence = 1
        sequence_str = f"{next_sequence:04d}"

        return int(f"{first_digit}{second_digit}{sequence_str}")

def get_next_sequence(cod):
    prefix = cod // 10000 
    current_sequence = cod % 10000
    next_sequence = current_sequence + 1
    return int(f"{prefix:02d}{next_sequence:04d}")

def clean_numbers(value):
    if value is None:
        return None
    return ''.join(filter(str.isdigit, value))
