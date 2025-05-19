from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def home():
    return render_template('login.html')



#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')