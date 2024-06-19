from datetime import datetime

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
