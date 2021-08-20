def split(string_file):
    file = open(string_file, 'rt')
    text = file.read()
    file.close()
    data_result_front = {
        "side": "front",
        "pais": text[1:31],
        "documento": text[31:64]
        , "Apellidos / Surname": text[69:83]
        , "Nombres / Given Names": text[96:114]
        , "Conocido Por": ""
        , "Genero / Gender ": text[173:175]
        , "Nacionalidad por / Nacionality by ": text[176:186]
        , "Fecha Lugar de Nacimiento / Datend Place of Birth": text[252:293]
        , "Fecha y Lugar de Expedicion / Datend place of issuance ": text[352:380]
        , "Fecha de Expiracion / Date Expiration ": text[490:505]
        , "Numero Unico de identidad : Number Unique of Identity": text[528:539]
        , "Compañia registradora / register company": text[539:588]

    }

    # print(data_result_front)
    return data_result_front
# split("C://Users//Hp//Desktop//OCR_PROJECT-2021//Texts//result.txt")
