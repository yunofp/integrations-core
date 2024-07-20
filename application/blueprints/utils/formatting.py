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
    dd, mm, aaaa = data.split('/')
    return f'{aaaa}-{mm}-{dd}'


def clearPhoneNum(string):
    toRemove = ['(', ')', '-']
    for caractere in toRemove:
        string = string.replace(caractere, '')
    return string

def formatFileName(serviceType, contractValues):
    clientName = ''
    if serviceType == 'Grow' or serviceType == 'Wealth' or serviceType == 'Wealth & Grow':
        clientName = contractValues.get("nomeCompletoDoTitular")
    if serviceType == 'Work': 
        clientName = contractValues.get("nomeDaEmpresa")   
    filename =  "[Integração] Contrato" + " " + serviceType + " - " + clientName + ".docx"
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
    # Remove todos os caracteres que não sejam números
    numeric_document = ''.join(filter(str.isdigit, document))
    
    # Verifica se o tamanho corresponde a um CPF ou CNPJ
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
    # Substitui "INATIVO", "nan" e "R$" por "0"
    cleaned_str = str(currency_str).replace("INATIVO", "0").replace("nan", "0").replace('R$', '0').replace('-', "0").strip()
    # Remove qualquer espaço adicional
    cleaned_str = re.sub(r'\s+', '', cleaned_str)
    # Remove todos os pontos
    cleaned_str = cleaned_str.replace('.', '')
    # Substitui a última vírgula (casa decimal) por um ponto
    cleaned_str = re.sub(r',', '.', cleaned_str, count=1)
    # Remove quaisquer vírgulas restantes
    cleaned_str = cleaned_str.replace(',', '')
    return float(cleaned_str)

def processing_number_insert(value):
    invalid_values = ["-", "R$ -", "", "INATIVO", "nan", "NaN", "null", None]

    if value in invalid_values:
        return 0
    else:
        return clean_currency_string_to_double(value)
    
def get_mmaaaa(cell):
    cell = str(cell)  # Converte cell para string
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
        return "Invalid cell value!"
    
def generate_cod(df, index):
        # Definir o primeiro dígito com base no campo Contrato
        contract_type = df.iloc[index]['Contrato']
        if contract_type == 'GROW':
            first_digit = '1'
        elif contract_type == 'WEALTH':
            first_digit = '2'
        elif contract_type == 'WORK':
            first_digit = '3'
        else:
            raise ValueError(f"Invalid contract type: {contract_type}")

        # Definir o segundo dígito com base no nome do closer
        closer_name = df.iloc[index]['Closer']
        if closer_name in ['BRUNO DEOR', 'MAX MULLER']:
            second_digit = '2'
        else:
            second_digit = '1'

        # Obter o próximo número sequencial inicial
        next_sequence = 1  # Inicializando a sequência
        sequence_str = f"{next_sequence:04d}"  # Formatar com 4 dígitos, preenchendo com zeros à esquerda

        return int(f"{first_digit}{second_digit}{sequence_str}")

def get_next_sequence(cod):
    # Separar os 4 últimos dígitos do código e incrementar 1
    prefix = cod // 10000  # Obter os dois primeiros dígitos
    current_sequence = cod % 10000  # Obter os quatro últimos dígitos
    next_sequence = current_sequence + 1
    return int(f"{prefix:02d}{next_sequence:04d}")

def clean_numbers(value):
    return ''.join(filter(str.isdigit, value))
