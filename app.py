from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Desempeño del personal IE-RFA'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')