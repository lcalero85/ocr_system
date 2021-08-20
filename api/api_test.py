from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

personas = []


class Personas(Resource):
    def get(self, valor):
        for persona in personas:
            return {'Persona Buscada =': persona}
        return {'resultado': 'Persona no encontrada'}

    def post(self, valor):
        persona = valor
        personas.append(persona)
        return {'resultado': 'Persona añadida correctamente'}

    def delete(self, valor):
        for indice, persona in enumerate(personas):
            if persona == valor:
                personas.pop(indice)
                return {'resultado': 'Persona eliminada correctamente'}


class Listar(Resource):
    def get(self):
        return {'resultado': personas}


api.add_resource(Personas, '/persona/<string:valor>')
api.add_resource(Listar, '/listar')

if __name__ == '__main__':
    # Iniciamos la aplicación
    app.run(debug=True)
