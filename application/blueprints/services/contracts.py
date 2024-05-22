
class ContractsService:
  def __init__(self, zeevClient, ProcessedRequestRepository):
    self.zeevClient = zeevClient
  
  def process(self,requestId):
    zeevToken = self.zeevClient.generateZeevToken()
    print(zeevToken)
    # instanceProcess = getServiceType(requestId, zeevToken)
    # envelopeId = createEnvelope()
    # instanceProcess = formatServiceType(instanceProcess)

    # if instanceProcess == "Grow":
    
    #     growResponse = sendZeevPost(requestId, zeevToken)
    #     growResponse2 = sendZeevPost2(requestId, zeevToken)
    #     contractVariables = defineVariablesGrow(growResponse, growResponse2)
    #     filename = formatFilename(contractVariables)
    #     documentId = sendClickSignPostGrow(contractVariables, envelopeId, filename)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    #     cpf = formatCpf(contractVariables.get("cpfDoTitular"))
    #     email = contractVariables.get("email")
    #     birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
    #     signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
    #     addQualificationRequirements(envelopeId, signerId, documentId)
    #     addAuthRequirements(envelopeId, signerId, documentId)
    #     activateEnvelope(envelopeId)
    #     notificateEnvelope(envelopeId)

    #     filename =  datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " +  contractVariables.get("qualOTipoDeTrabalho") + " " + contractVariables.get("nomeCompletoDoTitular") + ".doc"
    #     downloadContract(clicksignContract, filename)
    #     signerName = contractVariables.get("nomeCompletoDoTitular")
    #     contractUrl = uploadContractToDrive(filename, contractVariables.get("email"))
    #     print(contractUrl)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    #     print(phoneNum + " " + signerName)
    #     signResponse = sendWhatsappSign(signerName, contractUrl, phoneNum)
    #     return sendZeevPost

    # elif instanceProcess == "Wealth":

    #     wealthResponse = sendZeevPost(requestId, zeevToken)
    #     wealthResponse2 = sendZeevPost2(requestId, zeevToken)
    #     contractVariables = defineVariablesWealth(wealthResponse, wealthResponse2)
    #     filename = formatFilename(contractVariables)
    #     documentId = sendClickSignPostWealth(contractVariables, envelopeId, filename)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    #     cpf = formatCpf(contractVariables.get("cpfDoTitular"))
    #     email = contractVariables.get("email")
    #     birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
    #     signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
    #     addQualificationRequirements(envelopeId, signerId, documentId)
    #     addAuthRequirements(envelopeId, signerId, documentId)
    #     activateEnvelope(envelopeId)
    #     notificateEnvelope(envelopeId)

    #     return sendZeevPost
    
    # elif instanceProcess == "Work":

    #     workResponse = sendZeevPost(requestId, zeevToken)
    #     workResponse2 = sendZeevPost2(requestId, zeevToken)
    #     contractVariables = defineVariablesWork(workResponse, workResponse2)
    #     filename = formatFilename(contractVariables)
    #     documentId = sendClickSignPostWork(contractVariables, envelopeId, filename)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDaEmpresa"))
    #     cpf = formatCpf(contractVariables.get("cnpj"))
    #     email = contractVariables.get("emailDeContato")
    #     birthdate = formatBirthdate(contractVariables.get("dataDeNascimentoDoResponsavel"))
    #     signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
    #     addQualificationRequirements(envelopeId, signerId, documentId)
    #     addAuthRequirements(envelopeId, signerId, documentId)
    #     activateEnvelope(envelopeId)
    #     notificateEnvelope(envelopeId)

    #     return sendZeevPost

    # elif instanceProcess == "Grow & Wealth":

    #     growResponse = sendZeevPost(requestId, zeevToken)
    #     growResponse2 = sendZeevPost2(requestId, zeevToken)
    #     contractVariables = defineVariablesGrow(growResponse, growResponse2)
    #     filename = formatFilename(contractVariables)
    #     documentId = sendClickSignPostGrow(contractVariables, envelopeId, filename)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    #     cpf = formatCpf(contractVariables.get("cpfDoTitular"))
    #     email = contractVariables.get("email")
    #     birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
    #     signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
    #     addQualificationRequirements(envelopeId, signerId, documentId)
    #     addAuthRequirements(envelopeId, signerId, documentId)
    #     activateEnvelope(envelopeId)
    #     notificateEnvelope(envelopeId)

    #     wealthResponse = sendZeevPost(requestId, zeevToken)
    #     wealthResponse2 = sendZeevPost2(requestId, zeevToken)
    #     contractVariables = defineVariablesWealth(wealthResponse, wealthResponse2)
    #     filename = formatFilename(contractVariables)
    #     documentId = sendClickSignPostWealth(contractVariables, envelopeId, filename)
    #     phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    #     cpf = formatCpf(contractVariables.get("cpfDoTitular"))
    #     email = contractVariables.get("email")
    #     birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
    #     signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
    #     addQualificationRequirements(envelopeId, signerId, documentId)
    #     addAuthRequirements(envelopeId, signerId, documentId)
    #     activateEnvelope(envelopeId)
    #     notificateEnvelope(envelopeId)
    
    #     return sendZeevPost
    
    # else:
    #     print("Não foi possível gerar o documento")

