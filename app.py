from flask import Flask, render_template, request, make_response
from fpdf import FPDF
import io

app = Flask(__name__)

# Clase para el PDF minimalista
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Usuario', 0, 1, 'C')
        self.ln(10)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Recoger datos
        datos = {
            'Nombre': request.form.get('nombre'),
            'Apellidos': request.form.get('apellidos'),
            'NIF': request.form.get('nif'),
            'Email': request.form.get('email'),
            'Movil': request.form.get('movil')
        }

        # 2. Crear PDF en memoria
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for key, value in datos.items():
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(40, 10, key + ":", 0)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, value, 0, 1)

        # 3. Preparar la respuesta (Output a string buffer)
        # 'S' devuelve el documento como string (bytes en Py3)
        response_bytes = pdf.output(dest='S').encode('latin-1') 
        
        # 4. Crear respuesta HTTP con el archivo
        response = make_response(response_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=info_usuario.pdf'
        return response

    return render_template('index.html')

if __name__ == "__main__":
    # Esto es solo para local
    app.run(debug=True, host="0.0.0.0", port=8080)