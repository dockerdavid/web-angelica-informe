import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    /* Forzar modo claro */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Asegurar que todos los elementos tengan buen contraste */
    .stMarkdown, .stText, .stRadio, .stSelectbox, .stButton {
        background-color: #ffffff !important;
        color: #000000 !important;
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
    
    /* Asegurar que el texto sea legible */
    p, h1, h2, h3, h4, h5, h6 {
        color: #333333 !important;
    }
    
    /* Estilo para expanders */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: #333333 !important;
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
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Gráfico de puntuaciones totales
    categories = ['Visual', 'Auditivo', 'Kinestesico']
    values = [scores['visual'], scores['auditory'], scores['kinesthetic']]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars1 = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax1.set_title('Puntuaciones Totales por Categoria', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('Puntuacion Total', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(values) * 1.2 if values else 60)
    ax1.grid(axis='y', alpha=0.3)
    
    # Agregar valores en las barras
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=14)
    
    # Gráfico de porcentajes
    percentage_values = [percentages['visual'], percentages['auditory'], percentages['kinesthetic']]
    bars2 = ax2.bar(categories, percentage_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('Porcentajes por Categoria', fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylabel('Porcentaje (%)', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    
    # Agregar valores en las barras
    for bar, value in zip(bars2, percentage_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    return fig

def create_hemisphere_chart(left_count, right_count):
    """Crea gráfico de pastel para los resultados de hemisferios"""
    plt.style.use('default')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Gráfico de pastel
    labels = ['Hemisferio Izquierdo', 'Hemisferio Derecho']
    sizes = [left_count, right_count]
    colors = ['#FF6B6B', '#4ECDC4']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribucion de Hemisferios', fontsize=16, fontweight='bold', pad=20)
    
    # Gráfico de barras
    bars = ax2.bar(labels, sizes, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax2.set_title('Conteo de Respuestas', fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylabel('Numero de Respuestas', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, max(sizes) * 1.2 if sizes else 10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Agregar valores en las barras
    for bar, value in zip(bars, sizes):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value}', ha='center', va='bottom', fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    return fig

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
        for idx, row in df.iterrows():
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
            if idx < len(df) - 1:
                st.markdown("---")
        
        # Botón de envío mejorado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Calcular Mis Resultados",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            st.success("✅ ¡Formulario enviado exitosamente!")
            
            # Calcular puntuaciones
            scores = calculate_scores(responses)
            percentages, total_score = calculate_percentages(scores)
            
            # Mostrar resultados con diseño mejorado
            st.markdown("""
            <div class="results-card">
                <h2>📊 Resultados del Test</h2>
                <p>Aquí están tus puntuaciones y porcentajes por estilo de aprendizaje</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear columnas para mostrar los resultados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>👁️ Visual</h3>
                    <h2 style="color: #FF6B6B; font-size: 2.5rem;">{scores['visual']}</h2>
                    <p style="font-size: 1.2rem; color: #666;">{percentages['visual']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>👂 Auditivo</h3>
                    <h2 style="color: #4ECDC4; font-size: 2.5rem;">{scores['auditory']}</h2>
                    <p style="font-size: 1.2rem; color: #666;">{percentages['auditory']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🤲 Kinestésico</h3>
                    <h2 style="color: #45B7D1; font-size: 2.5rem;">{scores['kinesthetic']}</h2>
                    <p style="font-size: 1.2rem; color: #666;">{percentages['kinesthetic']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Puntuación total
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <h3>🎯 Puntuación Total</h3>
                <h2 style="color: #667eea; font-size: 3rem;">{total_score}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear y mostrar gráficos
            st.subheader("📈 Gráficos de Resultados")
            fig = create_learning_chart(scores, percentages)
            st.pyplot(fig)
            
            # Interpretación de resultados
            st.subheader("🎯 Interpretación de Resultados")
            
            max_category = max(percentages, key=percentages.get)
            max_percentage = percentages[max_category]
            
            interpretations = {
                'visual': """
                **👁️ Tu estilo de aprendizaje predominante es VISUAL**
                
                Te beneficias especialmente de:
                • 📊 Imágenes, diagramas y gráficos
                • 📝 Material escrito y notas
                • 🎨 Colores y mapas mentales
                • 📖 Lectura y visualización
                • 🖼️ Videos y presentaciones visuales
                """,
                'auditory': """
                **👂 Tu estilo de aprendizaje predominante es AUDITIVO**
                
                Te beneficias especialmente de:
                • 🎧 Escuchar explicaciones y conferencias
                • 💬 Discusiones y debates
                • 🎵 Música y ritmos
                • 🗣️ Explicar conceptos en voz alta
                • 📻 Podcasts y grabaciones
                """,
                'kinesthetic': """
                **🤲 Tu estilo de aprendizaje predominante es KINESTÉSICO**
                
                Te beneficias especialmente de:
                • 🏃‍♂️ Actividades prácticas y experimentos
                • 🎭 Role-playing y simulaciones
                • ✋ Manipulación de objetos
                • 🚶‍♂️ Movimiento mientras aprendes
                • 🔬 Experiencia directa y hands-on
                """
            }
            
            st.info(interpretations[max_category])

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
        
        # Botón de envío
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "🧠 Calcular Mis Resultados",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            st.success("✅ ¡Formulario enviado exitosamente!")
            
            # Calcular puntuaciones
            left_count, right_count = calculate_hemisphere_scores(responses)
            total_questions = len(questions)
            
            # Mostrar resultados
            st.markdown("""
            <div class="results-card">
                <h2>🧠 Resultados del Test de Hemisferios</h2>
                <p>Aquí están tus resultados de predominancia cerebral</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear columnas para mostrar los resultados
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚖️ Hemisferio Izquierdo</h3>
                    <h2 style="color: #FF6B6B; font-size: 2.5rem;">{left_count}</h2>
                    <p style="font-size: 1.2rem; color: #666;">{(left_count/total_questions)*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎨 Hemisferio Derecho</h3>
                    <h2 style="color: #4ECDC4; font-size: 2.5rem;">{right_count}</h2>
                    <p style="font-size: 1.2rem; color: #666;">{(right_count/total_questions)*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Crear y mostrar gráficos
            st.subheader("📊 Gráficos de Resultados")
            fig = create_hemisphere_chart(left_count, right_count)
            st.pyplot(fig)
            
            # Interpretación de resultados
            st.subheader("🎯 Interpretación de Resultados")
            
            if left_count > right_count:
                st.info("""
                **⚖️ Tu hemisferio IZQUIERDO es predominante**
                
                Características de tu pensamiento:
                • 📊 Lógico y analítico
                • 📝 Secuencial y ordenado
                • 🔢 Matemático y preciso
                • 📋 Planificador y organizado
                • 🎯 Orientado a detalles
                • 💭 Razonamiento verbal
                """)
            elif right_count > left_count:
                st.info("""
                **🎨 Tu hemisferio DERECHO es predominante**
                
                Características de tu pensamiento:
                • 🎨 Creativo e intuitivo
                • 🎵 Musical y artístico
                • 🌟 Holístico y global
                • 🎭 Emocional y expresivo
                • 🎪 Flexible y espontáneo
                • 🎨 Pensamiento visual
                """)
            else:
                st.info("""
                **⚖️🎨 Tienes un EQUILIBRIO entre ambos hemisferios**
                
                Características de tu pensamiento:
                • 🔄 Versátil y adaptable
                • 🎯 Puedes alternar entre lógica y creatividad
                • 🌟 Aprovechas lo mejor de ambos hemisferios
                • 🎪 Flexible en diferentes situaciones
                • 🎨 Capacidad de síntesis única
                """)

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
