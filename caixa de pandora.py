def create_profile_dict(index, df):
     profile = {}
     profile["name"] = df.iloc[index]['Nome do Cliente']
     profile["email"] = df.iloc[index, 6]
     profile["birthdate"] = df.iloc[index]['Data de Nascimento']
     profile["phone"] = df.iloc[index]['Telefone']
     profile["cpfcnpj"] = formatting.clear_cpf(df.iloc[index]['CPF / CPNJ'])
     profile["jobPosition"] = ""
     profile["address"] = df.iloc[index]['Endereço']
     profile["neighborhood"] = df.iloc[index]['Bairro']
     profile["zipCode"] = df.iloc[index]['CEP']
     profile["city"] = df.iloc[index]['Cidade']
     profile["state"] = df.iloc[index]['UF']
     profile["type"] = ""
     profile["financialAssets"] = formatting.clean_currency_string_to_double(df.iloc[index]['AUM Estimado'])
     profile["budgetProfile"] = df.iloc[index]['PERFIL']
     profile["residenceProperty"] = ""
     profile["maritalStatus"] = ""
     profile["primaryProfession"] = ""
     profile["businessSector"] = ""
     profile["consenting.name"] = df.iloc[index]['Nome do Cônjuge/Responsável da Empresa']
     profile["consenting.email"] = df.iloc[index, 17]
     profile["consenting.birthdate"] = df.iloc[index, 18]
     profile["consenting.phone"] = df.iloc[index, 19]
     profile["consenting.cpfCnpj"] = df.iloc[index, 20]

     return profile

