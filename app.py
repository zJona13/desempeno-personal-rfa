from flask import Flask, render_template
from routes.route_sesion import ws_sesion

app = Flask(__name__)
app.register_blueprint(ws_sesion)

@app.route('/')
@app.route('/login')
def home():
    return render_template('login.html')


#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=8080, debug=True, host='0.0.0.0')