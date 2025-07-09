import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import io
import base64

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Tests Psicológicos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Forzar modo claro
st.markdown("""
<style>
    /* Forzar modo claro completamente */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Forzar todos los elementos a modo claro */
    .stMarkdown, .stText, .stRadio, .stSelectbox, .stButton, .stTextInput, .stNumberInput {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Forzar sidebar y otros elementos */
    .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj, .css-1wivap2 {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Forzar elementos de formulario */
    .stForm {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Forzar elementos de radio y checkbox */
    .stRadio > div > label {
        background: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        transition: all 0.3s ease;
        cursor: pointer;
        color: #333333 !important;
    }
    
    .stRadio > div > label:hover {
        background: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
    }
    
    .stRadio > div > label[data-testid*="selected"] {
        background: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
    }
    
    /* Forzar campos de texto */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e9ecef !important;
    }
    
    /* Forzar campos numéricos */
    .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e9ecef !important;
    }
    
    /* Forzar botones */
    .stButton > button {
        background-color: #667eea !important;
        color: white !important;
        border: none !important;
    }
    
    /* Forzar spinners y mensajes */
    .stSpinner, .stSuccess, .stError, .stWarning, .stInfo {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Forzar gráficos */
    .stPlotlyChart, .stImage {
        background-color: #ffffff !important;
    }
    
    /* Estilos personalizados */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .test-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .test-card:hover {
        border-color: #667eea;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .question-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        color: #333333;
    }
    
    .results-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: #333333;
    }
    
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
    }
    
    /* Asegurar que el texto sea legible */
    p, h1, h2, h3, h4, h5, h6 {
        color: #333333 !important;
    }
    
    /* Estilo para expanders */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
    
    /* Forzar modo claro en todos los elementos de Streamlit */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: #ffffff !important;
    }
    
    /* Forzar gráficos matplotlib */
    .stPlotlyChart > div {
        background-color: #ffffff !important;
    }
    
    /* Asegurar que los gráficos se vean bien */
    .element-container {
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def load_questions():
    """Carga las preguntas desde el archivo CSV"""
    df = pd.read_csv('data.csv')
    return df

def categorize_questions():
    """Define las categorías de preguntas según el tipo de aprendizaje"""
    visual_questions = [1, 5, 9, 10, 11, 16, 17, 18, 22, 26, 32, 36]
    auditory_questions = [2, 3, 12, 13, 15, 19, 20, 23, 24, 27, 28, 29]
    kinesthetic_questions = [4, 6, 7, 8, 14, 21, 25, 30, 31, 33, 34, 35]
    
    return {
        'visual': visual_questions,
        'auditory': auditory_questions,
        'kinesthetic': kinesthetic_questions
    }

def get_hemisphere_questions():
    """Define las preguntas del test de hemisferios cerebrales"""
    return [
        "Cuando aprendes algo nuevo, prefieres:",
        "Al resolver un problema, te inclinas por:",
        "Para organizar tu dia:",
        "Te resulta mas atractivo:",
        "Al expresarte:",
        "Prefieres:",
        "Al tomar decisiones:",
        "Para trabajar:",
        "Prefieres aprender mediante:",
        "Cuando enfrentas algo inesperado:"
    ]

def get_hemisphere_options():
    """Define las opciones A y B para cada pregunta del test de hemisferios"""
    return [
        ("Seguir instrucciones paso a paso", "Usar tu intuicion y experimentar"),
        ("Analizar logicamente", "Imaginar posibles soluciones creativas"),
        ("Haces listas y planificas", "Prefieres improvisar segun como te sientes"),
        ("Las matematicas o logica", "El arte, la musica o la creatividad"),
        ("Usas palabras precisas y directas", "Usas metaforas, gestos o analogias"),
        ("Fijarte en los detalles", "Tener una vision global"),
        ("Confias en el razonamiento o datos", "Sigues tu emocion o instinto"),
        ("Te acomodas mejor en entornos ordenados", "Prefieres ambientes flexibles y cambiantes"),
        ("Leer o escuchar explicaciones", "Ver imagenes o vivir la experiencia"),
        ("Te cuesta improvisar", "Te resulta facil adaptarte")
    ]

def calculate_scores(responses):
    """Calcula las puntuaciones por categoría"""
    categories = categorize_questions()
    scores = {}
    
    for category, questions in categories.items():
        total = 0
        for question_num in questions:
            if question_num in responses:
                total += responses[question_num]
        scores[category] = total
    
    return scores

def calculate_percentages(scores):
    """Calcula los porcentajes de cada categoría"""
    total_score = sum(scores.values())
    percentages = {}
    
    if total_score > 0:
        for category, score in scores.items():
            percentages[category] = (score / total_score) * 100
    else:
        for category in scores.keys():
            percentages[category] = 0
    
    return percentages, total_score

def calculate_hemisphere_scores(responses):
    """Calcula las puntuaciones del test de hemisferios"""
    left_count = sum(1 for response in responses.values() if response == 'A')
    right_count = sum(1 for response in responses.values() if response == 'B')
    return left_count, right_count

def create_learning_chart(scores, percentages):
    """Crea gráficos de barras para los resultados de estilos de aprendizaje"""
    plt.style.use('default')
    
    # Configurar el estilo para modo claro
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.bbox'] = 'tight'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('white')
    
    # Gráfico de puntuaciones totales
    categories = ['Visual', 'Auditivo', 'Kinestesico']
    values = [scores['visual'], scores['auditory'], scores['kinesthetic']]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars1 = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_title('Puntuaciones Totales por Categoria', fontsize=16, fontweight='bold', pad=20, color='black')
    ax1.set_ylabel('Puntuacion Total', fontsize=12, fontweight='bold', color='black')
    ax1.set_ylim(0, max(values) * 1.2 if values else 60)
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(colors='black')
    ax1.spines['bottom'].set_color('black')
    ax1.spines['top'].set_color('black')
    ax1.spines['left'].set_color('black')
    ax1.spines['right'].set_color('black')
    
    # Agregar valores en las barras
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=14, color='black')
    
    # Gráfico de porcentajes
    percentage_values = [percentages['visual'], percentages['auditory'], percentages['kinesthetic']]
    bars2 = ax2.bar(categories, percentage_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('Porcentajes por Categoria', fontsize=16, fontweight='bold', pad=20, color='black')
    ax2.set_ylabel('Porcentaje (%)', fontsize=12, fontweight='bold', color='black')
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(colors='black')
    ax2.spines['bottom'].set_color('black')
    ax2.spines['top'].set_color('black')
    ax2.spines['left'].set_color('black')
    ax2.spines['right'].set_color('black')
    
    # Agregar valores en las barras
    for bar, value in zip(bars2, percentage_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=14, color='black')
    
    plt.tight_layout()
    return fig

def create_hemisphere_chart(left_count, right_count):
    """Crea gráfico de pastel para los resultados de hemisferios"""
    plt.style.use('default')
    
    # Configurar el estilo para modo claro
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.bbox'] = 'tight'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('white')
    
    # Gráfico de pastel
    labels = ['Hemisferio Izquierdo', 'Hemisferio Derecho']
    sizes = [left_count, right_count]
    colors = ['#FF6B6B', '#4ECDC4']
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribucion de Hemisferios', fontsize=16, fontweight='bold', pad=20, color='black')
    
    # Configurar colores del texto en el gráfico de pastel
    for text in texts:
        text.set_color('black')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # Gráfico de barras
    bars = ax2.bar(labels, sizes, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('Conteo de Respuestas', fontsize=16, fontweight='bold', pad=20, color='black')
    ax2.set_ylabel('Numero de Respuestas', fontsize=12, fontweight='bold', color='black')
    ax2.set_ylim(0, max(sizes) * 1.2 if sizes else 10)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(colors='black')
    ax2.spines['bottom'].set_color('black')
    ax2.spines['top'].set_color('black')
    ax2.spines['left'].set_color('black')
    ax2.spines['right'].set_color('black')
    
    # Agregar valores en las barras
    for bar, value in zip(bars, sizes):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=14, color='black')
    
    plt.tight_layout()
    return fig

def save_chart_to_base64(fig):
    """Convierte un gráfico matplotlib a base64"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close(fig)
    return img_str

def send_email(user_data, test_type, results_data, charts_base64):
    """Envía el correo con los resultados del test usando mailcow"""
    try:
        smtp_server = os.getenv('MAIL_AMOVIL_HOST')
        smtp_port = int(os.getenv('MAIL_AMOVIL_PORT', 587))
        smtp_user = os.getenv('MAIL_AMOVIL_USER')
        smtp_pass = os.getenv('MAIL_AMOVIL_PASS')
        recipient = os.getenv('MAIL_SEND')

        if not smtp_server or not smtp_port or not smtp_user or not smtp_pass or not recipient:
            st.error("Error: Variables de entorno de correo no configuradas correctamente")
            return False

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Resultados del Test de {'Estilos de Aprendizaje' if test_type == 'learning' else 'Hemisferios Cerebrales'}"
        msg['From'] = smtp_user
        msg['To'] = recipient

        # Crear contenido HTML del correo (sin imágenes embebidas)
        html_content = create_email_html(user_data, test_type, results_data, None)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Agregar imagen como adjunto
        if charts_base64:
            # Decodificar la imagen base64
            image_data = base64.b64decode(charts_base64)
            
            # Crear adjunto de imagen
            image_attachment = MIMEBase('image', 'png')
            image_attachment.set_payload(image_data)
            encoders.encode_base64(image_attachment)
            
            # Configurar nombre del archivo y headers
            test_name = "Estilos_de_Aprendizaje" if test_type == 'learning' else "Hemisferios_Cerebrales"
            filename = f"resultados_{test_name}_{user_data['nombre'].replace(' ', '_')}.png"
            image_attachment.add_header('Content-Disposition', 'attachment', 
                                      filename=filename)
            
            # Agregar título descriptivo
            title = f"Gráficos de Resultados - Test de {'Estilos de Aprendizaje' if test_type == 'learning' else 'Hemisferios Cerebrales'}"
            image_attachment.add_header('Content-Description', title)
            
            msg.attach(image_attachment)

        # Enviar correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Error al enviar el correo: {str(e)}")
        return False

def create_email_html(user_data, test_type, results_data, charts_base64):
    """Crea el contenido HTML del correo"""
    if test_type == 'learning':
        return create_learning_email_html(user_data, results_data, charts_base64)
    else:
        return create_hemisphere_email_html(user_data, results_data, charts_base64)

def create_learning_email_html(user_data, results_data, charts_base64):
    """Crea el HTML para el correo del test de estilos de aprendizaje"""
    scores = results_data['scores']
    percentages = results_data['percentages']
    total_score = results_data['total_score']
    max_category = results_data['max_category']
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
            .user-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
            .results-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
            .result-card {{ background-color: white; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #e9ecef; }}
            .attachment-info {{ background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3; margin: 30px 0; }}
            .interpretation {{ background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3; }}
            h1, h2, h3 {{ color: #333; }}
            .score {{ font-size: 2.5em; font-weight: bold; }}
            .percentage {{ font-size: 1.2rem; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 Test de Estilos de Aprendizaje</h1>
                <p>Resultados del análisis de preferencias de aprendizaje</p>
            </div>
            
            <div class="user-info">
                <h3>📋 Información del Participante</h3>
                <p><strong>Nombre:</strong> {user_data['nombre']}</p>
                <p><strong>Edad:</strong> {user_data['edad']} años</p>
                <p><strong>Cédula:</strong> {user_data['cedula']}</p>
            </div>
            
            <div class="results-grid">
                <div class="result-card">
                    <h3>👁️ Visual</h3>
                    <div class="score" style="color: #FF6B6B;">{scores['visual']}</div>
                    <div class="percentage">{percentages['visual']:.1f}%</div>
                </div>
                <div class="result-card">
                    <h3>👂 Auditivo</h3>
                    <div class="score" style="color: #4ECDC4;">{scores['auditory']}</div>
                    <div class="percentage">{percentages['auditory']:.1f}%</div>
                </div>
                <div class="result-card">
                    <h3>🤲 Kinestésico</h3>
                    <div class="score" style="color: #45B7D1;">{scores['kinesthetic']}</div>
                    <div class="percentage">{percentages['kinesthetic']:.1f}%</div>
                </div>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <h3>🎯 Puntuación Total</h3>
                <div class="score" style="color: #667eea;">{total_score}</div>
            </div>
            
            <div class="attachment-info">
                <h3>📎 Gráficos Adjuntos</h3>
                <p>Se ha adjuntado un archivo PNG con los gráficos detallados de tus resultados, incluyendo:</p>
                <ul>
                    <li>📊 Puntuaciones totales por categoría</li>
                    <li>📈 Porcentajes de cada estilo de aprendizaje</li>
                    <li>🎯 Visualización completa de tus preferencias</li>
                </ul>
                <p><strong>Nombre del archivo:</strong> resultados_Estilos_de_Aprendizaje_{user_data['nombre'].replace(' ', '_')}.png</p>
            </div>
            
            <div class="interpretation">
                <h3>🎯 Interpretación de Resultados</h3>
                <p><strong>Tu estilo de aprendizaje predominante es: {max_category.upper()}</strong></p>
                <p>Este resultado indica que tienes una preferencia significativa por este estilo de aprendizaje, 
                lo que puede ayudarte a optimizar tu proceso de estudio y desarrollo personal.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def create_hemisphere_email_html(user_data, results_data, charts_base64):
    """Crea el HTML para el correo del test de hemisferios"""
    left_count = results_data['left_count']
    right_count = results_data['right_count']
    total_questions = results_data['total_questions']
    predominance = results_data['predominance']
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
            .user-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
            .results-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px; }}
            .result-card {{ background-color: white; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #e9ecef; }}
            .attachment-info {{ background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3; margin: 30px 0; }}
            .interpretation {{ background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3; }}
            h1, h2, h3 {{ color: #333; }}
            .score {{ font-size: 2.5em; font-weight: bold; }}
            .percentage {{ font-size: 1.2rem; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Test de Hemisferios Cerebrales</h1>
                <p>Análisis de predominancia cerebral</p>
            </div>
            
            <div class="user-info">
                <h3>📋 Información del Participante</h3>
                <p><strong>Nombre:</strong> {user_data['nombre']}</p>
                <p><strong>Edad:</strong> {user_data['edad']} años</p>
                <p><strong>Cédula:</strong> {user_data['cedula']}</p>
            </div>
            
            <div class="results-grid">
                <div class="result-card">
                    <h3>⚖️ Hemisferio Izquierdo</h3>
                    <div class="score" style="color: #FF6B6B;">{left_count}</div>
                    <div class="percentage">{(left_count/total_questions)*100:.1f}%</div>
                </div>
                <div class="result-card">
                    <h3>🎨 Hemisferio Derecho</h3>
                    <div class="score" style="color: #4ECDC4;">{right_count}</div>
                    <div class="percentage">{(right_count/total_questions)*100:.1f}%</div>
                </div>
            </div>
            
            <div class="attachment-info">
                <h3>📎 Gráficos Adjuntos</h3>
                <p>Se ha adjuntado un archivo PNG con los gráficos detallados de tus resultados, incluyendo:</p>
                <ul>
                    <li>🥧 Gráfico de pastel de distribución de hemisferios</li>
                    <li>📊 Gráfico de barras con conteo de respuestas</li>
                    <li>🎯 Visualización completa de tu predominancia cerebral</li>
                </ul>
                <p><strong>Nombre del archivo:</strong> resultados_Hemisferios_Cerebrales_{user_data['nombre'].replace(' ', '_')}.png</p>
            </div>
            
            <div class="interpretation">
                <h3>🎯 Interpretación de Resultados</h3>
                <p><strong>Predominancia: {predominance}</strong></p>
                <p>Este resultado refleja tu tendencia natural en el procesamiento de información y toma de decisiones.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html



def learning_style_test():
    """Test de estilos de aprendizaje"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Test de Estilos de Aprendizaje</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Descubre tu estilo de aprendizaje preferido respondiendo estas preguntas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar las preguntas
    df = load_questions()
    
    # Opciones de respuesta con iconos
    opciones = {
        1: "😴 CASI NUNCA",
        2: "🤔 RARA VEZ", 
        3: "😐 A VECES",
        4: "😊 FRECUENTEMENTE",
        5: "🎯 CASI SIEMPRE"
    }
    
    # Crear el formulario
    with st.form("learning_style_form"):
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h3>📝 Instrucciones:</h3>
            <p>Para cada afirmación, selecciona la opción que mejor te describa. 
            No hay respuestas correctas o incorrectas, solo sé honesto contigo mismo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        responses = {}
        
        # Generar una pregunta por cada fila del CSV
        total_questions = len(df)
        for i, (idx, row) in enumerate(df.iterrows()):
            numero = row['Número']
            pregunta = row['Pregunta']
            
            # Crear una tarjeta para cada pregunta
            st.markdown(f"""
            <div class="question-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Pregunta {numero}</h4>
                <p style="font-size: 1.1rem; line-height: 1.6;">{pregunta}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear radio buttons para cada pregunta con mejor diseño
            respuesta = st.radio(
                "Selecciona tu respuesta:",
                options=list(opciones.keys()),
                format_func=lambda x: opciones[x],
                key=f"pregunta_{numero}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            responses[numero] = respuesta
            
            # Separador visual
            if i < total_questions - 1:
                st.markdown("---")
        
        # Sección de datos personales
        st.markdown("---")
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
            <h3>📋 Datos Personales</h3>
            <p>Completa tus datos para recibir el informe completo por correo electrónico.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo", key="nombre_learning")
            edad = st.number_input("Edad", min_value=1, max_value=120, key="edad_learning")
        
        with col2:
            cedula = st.text_input("Número de Cédula", key="cedula_learning")
        
        # Verificar que todos los campos estén completos
        all_fields_filled = (nombre is not None and nombre.strip() != "") and (edad is not None and edad > 0) and (cedula is not None and cedula.strip() != "")
        
        # Botón de envío único
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "📧 Enviar Test y Recibir Resultados",
                use_container_width=True,
                type="primary",
                disabled=False
            )
    
    # Procesar resultados y enviar correo
    if submitted and all_fields_filled:
        st.success("✅ ¡Test enviado exitosamente! Procesando resultados...")
        
        # Calcular puntuaciones
        scores = calculate_scores(responses)
        percentages, total_score = calculate_percentages(scores)
        
        # Crear gráficos
        fig = create_learning_chart(scores, percentages)
        charts_base64 = save_chart_to_base64(fig)
        
        # Preparar datos para el correo
        max_category = max(percentages.keys(), key=lambda k: percentages[k])
        results_data = {
            'scores': scores,
            'percentages': percentages,
            'total_score': total_score,
            'max_category': max_category
        }
        
        # Datos del usuario
        user_data = {
            'nombre': nombre,
            'edad': edad,
            'cedula': cedula
        }
        
        # Enviar correo
        with st.spinner("Enviando resultados por correo..."):
            if send_email(user_data, 'learning', results_data, charts_base64):
                st.success("✅ ¡Correo enviado exitosamente! Revisa tu bandeja de entrada.")
            else:
                st.error("❌ Error al enviar el correo. Por favor, intenta nuevamente.")

def hemisphere_test():
    """Test de hemisferios cerebrales"""
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Test de Hemisferios Cerebrales</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            ¿Predomina tu hemisferio izquierdo o derecho?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obtener preguntas y opciones
    questions = get_hemisphere_questions()
    options = get_hemisphere_options()
    
    # Crear el formulario
    with st.form("hemisphere_form"):
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h3>📝 Instrucciones:</h3>
            <p>Marca la opción con la que más te identificas en cada pregunta. 
            Al final, contaremos cuántas respuestas A y cuántas B elegiste.</p>
        </div>
        """, unsafe_allow_html=True)
        
        responses = {}
        
        # Generar preguntas
        for idx, (question, (option_a, option_b)) in enumerate(zip(questions, options), 1):
            # Crear una tarjeta para cada pregunta
            st.markdown(f"""
            <div class="question-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">Pregunta {idx}</h4>
                <p style="font-size: 1.1rem; line-height: 1.6;">{question}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear radio buttons para cada pregunta
            respuesta = st.radio(
                "Selecciona tu respuesta:",
                options=['A', 'B'],
                format_func=lambda x: f"{x}) {option_a if x == 'A' else option_b}",
                key=f"hemisphere_{idx}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            responses[idx] = respuesta
            
            # Separador visual
            if idx < len(questions):
                st.markdown("---")
        
        # Sección de datos personales
        st.markdown("---")
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
            <h3>📋 Datos Personales</h3>
            <p>Completa tus datos para recibir el informe completo por correo electrónico.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo", key="nombre_hemisphere")
            edad = st.number_input("Edad", min_value=1, max_value=120, key="edad_hemisphere")
        
        with col2:
            cedula = st.text_input("Número de Cédula", key="cedula_hemisphere")
        
        # Verificar que todos los campos estén completos
        all_fields_filled = (nombre is not None and nombre.strip() != "") and (edad is not None and edad > 0) and (cedula is not None and cedula.strip() != "")
        
        # Botón de envío único
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "📧 Enviar Test y Recibir Resultados",
                use_container_width=True,
                type="primary",
                disabled=False
            )
    
    # Procesar resultados y enviar correo
    if submitted and all_fields_filled:
        st.success("✅ ¡Test enviado exitosamente! Procesando resultados...")
        
        # Calcular puntuaciones
        left_count, right_count = calculate_hemisphere_scores(responses)
        total_questions = len(questions)
        
        # Crear gráficos
        fig = create_hemisphere_chart(left_count, right_count)
        charts_base64 = save_chart_to_base64(fig)
        
        # Determinar predominancia
        if left_count > right_count:
            predominance = "Hemisferio Izquierdo"
        elif right_count > left_count:
            predominance = "Hemisferio Derecho"
        else:
            predominance = "Equilibrio entre ambos hemisferios"
        
        # Preparar datos para el correo
        results_data = {
            'left_count': left_count,
            'right_count': right_count,
            'total_questions': total_questions,
            'predominance': predominance
        }
        
        # Datos del usuario
        user_data = {
            'nombre': nombre,
            'edad': edad,
            'cedula': cedula
        }
        
        # Enviar correo
        with st.spinner("Enviando resultados por correo..."):
            if send_email(user_data, 'hemisphere', results_data, charts_base64):
                st.success("✅ ¡Correo enviado exitosamente! Revisa tu bandeja de entrada.")
            else:
                st.error("❌ Error al enviar el correo. Por favor, intenta nuevamente.")

def main():
    # Interfaz de selección de test
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Tests Psicológicos</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Selecciona el test que deseas realizar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear dos columnas para los tests
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="test-card" onclick="document.querySelector('#learning_test').click()">
            <h2>🎓 Test de Estilos de Aprendizaje</h2>
            <p>Descubre si tu estilo de aprendizaje es visual, auditivo o kinestésico</p>
            <ul>
                <li>36 preguntas</li>
                <li>Escala de 1 a 5</li>
                <li>Resultados con gráficos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎓 Realizar Test de Estilos de Aprendizaje", key="learning_test", use_container_width=True):
            st.session_state.test_selected = "learning"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="test-card" onclick="document.querySelector('#hemisphere_test').click()">
            <h2>🧠 Test de Hemisferios Cerebrales</h2>
            <p>Descubre si predomina tu hemisferio izquierdo o derecho</p>
            <ul>
                <li>10 preguntas</li>
                <li>Opciones A o B</li>
                <li>Gráfico de pastel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Realizar Test de Hemisferios", key="hemisphere_test", use_container_width=True):
            st.session_state.test_selected = "hemisphere"
            st.rerun()
    
    # Mostrar el test seleccionado
    if 'test_selected' in st.session_state:
        if st.session_state.test_selected == "learning":
            learning_style_test()
        elif st.session_state.test_selected == "hemisphere":
            hemisphere_test()
        
        # Botón para volver al menú principal
        if st.button("🏠 Volver al Menú Principal"):
            del st.session_state.test_selected
            st.rerun()

if __name__ == "__main__":
    main()
