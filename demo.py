# Importamos todo lo necesario
import os
from flask import Flask, render_template, request, redirect, url_for
import ocr_procces_lib.im_preproccess
import ocr_procces_lib.text_img_proccess
import ocr_procces_lib.split_string
import ocr_procces_lib.life_check
import ocr_procces_lib.validate_document
import json
import glob

# instancia del objeto Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './Archivos IMG'
app.config['RESULT_FOLDER'] = './Texts'
app.config['selfies'] = './selfies'
# instanciando las clases para el procesamiento de la informacion


ima2 = ocr_procces_lib.im_preproccess
text = ocr_procces_lib.text_img_proccess
split_text = ocr_procces_lib.split_string
check = ocr_procces_lib.life_check
validate = ocr_procces_lib.validate_document


# renderizamos las vistas

@app.route("/")
def upload_file():
    return render_template('menu.html')


@app.route("/file_normal_upload")
def file_normal_upload():
    return render_template('normal_convert.html')


@app.route("/file_document_upload")
def file_document_upload():
    return render_template('document_convert.html')


@app.route("/file_check_life")
def file_check_life():
    return render_template('check_life_test.html')


@app.route("/dui_validator")
def dui_validator():
    return render_template('dui.html')


@app.route("/upload", methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST' or request.method == 'GET':
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = f.filename
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + filename)
        # ruta donde guardaremos la imagen
        procces_imagen_path = app.config['UPLOAD_FOLDER'] + '/' + 'processed_image.jpg'
        text_path = app.config['RESULT_FOLDER'] + '/result.txt'
        # image proccessed
        ima2.pre_image_proccessing(path, procces_imagen_path)
        # converter to text proccess
        text.text_proccesing(procces_imagen_path, text_path)
        # Retornamos una respuesta satisfactoria

        return redirect(url_for('document_result'))


@app.route("/upload2", methods=['POST', 'GET'])
def uploader2():
    if request.method == 'POST' or request.method == 'GET':
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = f.filename
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + filename)
        # ruta donde guardaremos la imagen
        procces_imagen_path = app.config['UPLOAD_FOLDER'] + '/' + 'processed_image.jpg'
        text_path = app.config['RESULT_FOLDER'] + '/result.txt'
        # image proccessed
        ima2.pre_image_proccessing(path, procces_imagen_path)
        # converter to text proccess
        text.text_proccesing(procces_imagen_path, text_path)
        # Retornamos una respuesta satisfactoria

        return redirect(url_for('normal_result'))


@app.route("/upload3", methods=['POST', 'GET'])
def uploader3():
    if request.method == 'POST' or request.method == 'GET':
        # obtenemos los archivos los inputs "archivo"
        f = request.files['archivo']
        f2 = request.files['archivo2']
        filename = f.filename
        filename2 = f2.filename

        # Guardamos la imagen1 en el directorio "Archivos IMG"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + filename)
        # Guardamos la imagen2 en el directorio Selfies
        f2.save(os.path.join(app.config['selfies'], filename2))
        path2 = os.path.join(app.config['selfies'] + '/' + filename2)

        # image compare

        # Retornamos una respuesta satisfactoria
        if check.compare_to_faces(path, path2):
            result = 'Successful comparison faces match correctly'
            return render_template('check_result.html', result=result)
        else:
            result2 = 'The faces do not match'
            return render_template('check_result.html', result=result2)


@app.route('/duis_validator', methods=["POST", "GET"])
def duis_validator():
    if request.method == 'POST' or request.method == 'GET':
        duiNumber = request.form['dui']
        if validate.validate_id_number(duiNumber):
            return "Your document number is valid"
        else:
            return "Your document number is invalid"


@app.route('/document_result', methods=["POST", "GET"])
def document_result():
    files = app.config['RESULT_FOLDER'] + '/result.txt'
    file = open(files, 'rt')
    text2 = file.read()
    file.close()
    # second clean time
    bad_chars = ['  a1 “', '7 Non', 'Cc', '@', '€ a', '¥ ', 'r ', 'Eat', 'td ', 'a” bh ‘< =', 'a1 “', 'ven ', ' ¥',
                 'a — &', '- * ', '%', ' + 4 N', ' Fa a 4', ' ba', ' Flanges ‘ 4', '7', 'rN ']

    # clean string in for
    for i in bad_chars:
        # Replace bad characters
        text2 = text2.replace(i, '')
    results_split = split_text.split(files)

    x = json.dumps(results_split, sort_keys=False, indent=0)
    return render_template('document_result.html', result=text2, result2=x)


@app.route('/normal_result', methods=["POST", "GET"])
def normal_result():
    files = app.config['RESULT_FOLDER'] + '/result.txt'
    file = open(files, 'rt')
    text2 = file.read()
    file.close()
    # second clean time
    bad_chars = ['  a1 “', '7 Non', 'Cc', '@', '€ a', '¥ ', 'r ', 'Eat', 'td ', 'a” bh ‘< =', 'a1 “', 'ven ', ' ¥',
                 'a — &', '- * ', '%', ' + 4 N', ' Fa a 4', ' ba', ' Flanges ‘ 4', '7', 'rN ']

    # clean string in for
    for i in bad_chars:
        # Replace bad characters
        text2 = text2.replace(i, '')
    return render_template('normal_result.html', result=text2)


if __name__ == '__main__':
    # Iniciamos la aplicación
    app.run(debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app.run(Host='0.0.0.0', port=port)
