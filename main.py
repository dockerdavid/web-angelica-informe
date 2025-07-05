import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def create_chart(scores, percentages):
    """Crea gráficos de barras para los resultados"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico de puntuaciones totales
    categories = list(scores.keys())
    values = list(scores.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars1 = ax1.bar(categories, values, color=colors)
    ax1.set_title('Puntuaciones Totales por Categoría', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Puntuación Total')
    ax1.set_ylim(0, max(values) * 1.1 if values else 60)
    
    # Agregar valores en las barras
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de porcentajes
    percentage_values = list(percentages.values())
    bars2 = ax2.bar(categories, percentage_values, color=colors)
    ax2.set_title('Porcentajes por Categoría', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Porcentaje (%)')
    ax2.set_ylim(0, 100)
    
    # Agregar valores en las barras
    for bar, value in zip(bars2, percentage_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

def main():
    st.title("Test de Estilos de Aprendizaje")
    st.write("Responde cada pregunta seleccionando la opción que mejor te describa:")
    
    # Cargar las preguntas
    df = load_questions()
    
    # Opciones de respuesta
    opciones = {
        1: "CASI NUNCA",
        2: "RARA VEZ", 
        3: "A VECES",
        4: "FRECUENTEMENTE",
        5: "CASI SIEMPRE"
    }
    
    # Crear el formulario
    with st.form("learning_style_form"):
        st.subheader("Instrucciones:")
        st.write("Para cada afirmación, selecciona la opción que mejor te describa:")
        
        responses = {}
        
        # Generar una pregunta por cada fila del CSV
        for _, row in df.iterrows():
            numero = row['Número']
            pregunta = row['Pregunta']
            
            st.write(f"**{numero}.** {pregunta}")
            
            # Crear radio buttons para cada pregunta
            respuesta = st.radio(
                f"Respuesta para pregunta {numero}:",
                options=list(opciones.keys()),
                format_func=lambda x: f"{x} - {opciones[x]}",
                key=f"pregunta_{numero}",
                horizontal=True
            )
            
            responses[numero] = respuesta
            st.divider()
        
        # Botón de envío
        submitted = st.form_submit_button("Calcular Resultados")
        
        if submitted:
            st.success("¡Formulario enviado exitosamente!")
            
            # Calcular puntuaciones
            scores = calculate_scores(responses)
            percentages, total_score = calculate_percentages(scores)
            
            # Mostrar resultados
            st.subheader("📊 Resultados del Test")
            
            # Crear columnas para mostrar los resultados
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Visual", f"{scores['visual']}", f"{percentages['visual']:.1f}%")
            with col2:
                st.metric("Auditivo", f"{scores['auditory']}", f"{percentages['auditory']:.1f}%")
            with col3:
                st.metric("Kinestésico", f"{scores['kinesthetic']}", f"{percentages['kinesthetic']:.1f}%")
            
            st.metric("Puntuación Total", total_score)
            
            # Mostrar detalles
            st.subheader("📋 Detalles por Categoría")
            
            categories = categorize_questions()
            category_names = {
                'visual': 'Visual',
                'auditory': 'Auditivo', 
                'kinesthetic': 'Kinestésico'
            }
            
            for category, questions in categories.items():
                with st.expander(f"Preguntas {category_names[category]} (Puntuación: {scores[category]})"):
                    for question_num in questions:
                        if question_num in responses:
                            st.write(f"Pregunta {question_num}: {responses[question_num]} puntos")
            
            # Crear y mostrar gráficos
            st.subheader("📈 Gráficos de Resultados")
            fig = create_chart(scores, percentages)
            st.pyplot(fig)
            
            # Interpretación de resultados
            st.subheader("🎯 Interpretación de Resultados")
            
            max_category = max(percentages, key=percentages.get)
            max_percentage = percentages[max_category]
            
            interpretations = {
                'visual': "Tienes una preferencia por el aprendizaje **visual**. Te beneficias de imágenes, diagramas, gráficos y material escrito.",
                'auditory': "Tienes una preferencia por el aprendizaje **auditivo**. Te beneficias de escuchar, discutir y explicaciones verbales.",
                'kinesthetic': "Tienes una preferencia por el aprendizaje **kinestésico**. Te beneficias de actividades prácticas, movimiento y experiencia directa."
            }
            
            st.info(f"**Tu estilo de aprendizaje predominante es: {category_names[max_category]}** ({max_percentage:.1f}%)")
            st.write(interpretations[max_category])

if __name__ == "__main__":
    main()
