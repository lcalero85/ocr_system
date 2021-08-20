import face_recognition


def compare_to_faces(img1, img2):
    # Cargamos las imagenes jpg a archivos numpy

    first_image = face_recognition.load_image_file(img1)
    second_image = face_recognition.load_image_file(img2)
    # Se maneja un posible error con la libreria , si no se logra cargar los archivos se aborta la comparacion
    try:
        sknow_image = face_recognition.face_encodings(first_image)[0]
        unknown_image = face_recognition.face_encodings(second_image)[0]
    except IndexError:
        print(
            "No puede localizar ningún rostro en al menos una de las imágenes. Verifique los archivos de imagen. Abortando ...")
        quit()

    # Guardamos en un array todas las caras conocidas

    known_faces = [sknow_image]
    Unknow_faces = unknown_image
    # Se realiza la comparacion de los rostros
    results = face_recognition.compare_faces(known_faces, Unknow_faces)
    # print("Is the unknown face a picture of first_image? {}".format(results[0]))
    if results[0]:
        return True
    else:
        return False


