from datetime import datetime
import re
from datetime import datetime
import pytz

def convert_to_utc_date(date_str):
    if not date_str or date_str == "-":
        return date_str
    
    date = datetime.strptime(date_str, "%d/%m/%Y")
    date_utc = date.replace(tzinfo=pytz.UTC)
    return date_utc

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
    filtered_numbers = ''.join(c for c in str(s) if c.isdigit() or c == '.')
    try:
        result = float(filtered_numbers)
    except ValueError:
        result = 0.0
    return result

def clean_currency_string_to_double(currency_str):
    cleaned_str = str(currency_str).replace("INATIVO", "0").replace("nan", "0").replace('R$', '0').replace('-', "0").strip()
    cleaned_str = re.sub(r'\s+', '', cleaned_str)
    cleaned_str = cleaned_str.replace('.', '')
    cleaned_str = re.sub(r',', '.', cleaned_str, count=1)
    cleaned_str = cleaned_str.replace(',', '')
    return float(cleaned_str)

def processing_number_insert(value):
    invalid_values = ["-", "R$ -", "", "INATIVO", "nan", "NaN", "null", None]

    if value in invalid_values:
        return 0
    else:
        return clean_currency_string_to_double(value)
    
def get_mmaaaa(cell):
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
        lfd = cell[-4:]
        return f"{mm}/{lfd}"
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
    return ''.join(filter(str.isdigit, value))
