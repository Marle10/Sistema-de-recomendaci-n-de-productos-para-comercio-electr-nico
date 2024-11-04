import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify, render_template

#Paso 1:Cargar el archivo CSV con una codificación alternativa
file_path = "C:/Users/Alexa Ramirez/Downloads/extracted_files/Year 2009-2010.csv"

try:
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    print("Archivo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el archivo: {e}")

#Mostrar las primeras filas y nombres de columnas para verificar
print("\nPrimeras filas del archivo:")
print(data.head())
print("\nNombres de las columnas en el archivo:")
print(data.columns)

#Paso2:Limpiar los Datos
print("\nValores nulos por columna:")
print(data.isnull().sum())

#Eliminar filas con valores nulos
data = data.dropna()

print("\nTipos de datos por columna:")
print(data.dtypes)

#Paso 3:Análisis Exploratorio de Datos

#Gráfico de productos más vendidos
plt.figure(figsize=(10, 6))
data['StockCode'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Productos Más Vendidos')
plt.xlabel('ID del Producto')
plt.ylabel('Frecuencia')
plt.show()

#Análisis de ventas por categoría 
if 'Categoria' in data.columns:
    plt.figure(figsize=(8, 8))
    data.groupby('Categoria')['Ventas'].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribución de Ventas por Categoría')
    plt.show()

#Paso4:Preprocesamiento de Texto 
if 'Descripcion' in data.columns:
    # Limpieza y vectorización de texto
    vectorizer = TfidfVectorizer(stop_words='english')
    data['Descripcion'] = data['Descripcion'].fillna('')
    tfidf_matrix = vectorizer.fit_transform(data['Descripcion'])

#Paso5:Implementación de un Modelo de Recomendación

#Crear una matriz de usuario-producto
user_product_matrix = data.pivot_table(index='Customer ID', columns='StockCode', values='Quantity', fill_value=0)

#Calcular la similitud de coseno entre usuarios
user_similarity = cosine_similarity(user_product_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_product_matrix.index, columns=user_product_matrix.index)

#Función para recomendar productos basados en usuarios similares
def recomendar_productos(user_id, num_recommendations=5):
    user_similarity_df.columns = user_similarity_df.columns.astype(float)
    user_similarity_df.index = user_similarity_df.index.astype(float)

#Verificar si el usuario existe en los datos de similitud
    if user_id in user_similarity_df.columns:
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:num_recommendations+1]
        recommended_products = []

        for similar_user in similar_users:
#Obtener los productos comprados por el usuario similar
            user_data = data[data['Customer ID'] == similar_user]
            recommended_products.extend(user_data['StockCode'].unique())

#Devolver productos únicos recomendados, limitados a la cantidad especificada
        return list(set(recommended_products))[:num_recommendations]
    else:
        print(f"El usuario {user_id} no se encuentra en los datos de similitud.")
        return []

#Ejemplo de recomendaciones para un usuario específico
user_id = 12392.0  
print("\nRecomendaciones para el usuario", user_id)
print(recomendar_productos(user_id=user_id))

#Paso6:Creación de una Interfaz con Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/recomendar', methods=['GET'])
def recomendar():
    try:
        user_id = float(request.args.get('user_id'))
        num_recommendations = int(request.args.get('num_recommendations', 5))

        recommendations = recomendar_productos(user_id, num_recommendations)
        return jsonify({"user_id": user_id, "recommendations": recommendations})
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=False)