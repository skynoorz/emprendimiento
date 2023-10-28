from flask import Flask, render_template, request

app = Flask(__name__)

# Datos ficticios de calorías por plato
calorias_por_plato = {
    'Sajta': 500,
    'Falso Conejo': 700,
    # Agrega más platos y sus calorías aquí
}

# Datos ficticios de ejercicios y sus calorías
ejercicios_disponibles = {
    'Caminata 10min': 100,
    'Saltar la cuerda 10min': 200,
    '4 repeticiones de 10 abdominales': 250,
    '4 repeticiones de 10 salto estrella': 300,
    # Agrega más ejercicios y sus calorías por 10 minutos aquí
}

def calcular_ejercicios(calorias_requeridas, ejercicios_disponibles):
    ejercicios_para_quemar_calorias = []
    calorias_faltantes = calorias_requeridas

    # Ordena los ejercicios disponibles de mayor a menor quema de calorías
    ejercicios_ordenados = sorted(ejercicios_disponibles.items(), key=lambda x: x[1], reverse=True)

    for ejercicio, calorias_por_10min in ejercicios_ordenados:
        if calorias_faltantes >= calorias_por_10min:
            ejercicios_para_quemar_calorias.append(ejercicio)
            calorias_faltantes -= calorias_por_10min

    return ejercicios_para_quemar_calorias


@app.route('/', methods=['GET', 'POST'])
def index():
    platos = list(calorias_por_plato.keys())
    
    if request.method == 'POST':
        platos_seleccionados = request.form.getlist('platos')
        calorias_totales = sum([calorias_por_plato.get(plato, 0) for plato in platos_seleccionados])
        
        ejercicios_para_quemar_calorias = calcular_ejercicios(calorias_totales, ejercicios_disponibles)
        
        return render_template('index.html', platos=platos, ejercicios=ejercicios_disponibles,
                               calorias_totales=calorias_totales, ejercicios_para_quemar_calorias=ejercicios_para_quemar_calorias)
    
    return render_template('index.html', platos=platos, ejercicios=ejercicios_disponibles, calorias_totales=None, ejercicios_para_quemar_calorias=None)

if __name__ == '__main__':
    app.run(debug=True)
