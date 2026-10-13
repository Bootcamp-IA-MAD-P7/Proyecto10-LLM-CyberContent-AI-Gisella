# CyberContent AI 
**Plataforma de Generación Automática de Contenido con IA**

Plataforma inteligente desarrollada con **Streamlit** y **Groq API** para la generación automática de contenido adaptado a múltiples plataformas (Blogs, LinkedIn, Instagram, X/Twitter) y audiencias objetivo, utilizando técnicas de Prompt Engineering y validación de salidas.

---

##  Arquitectura y Estructura del Proyecto
- **Frontend (UI):** Streamlit (`app/ui/streamlit_app.py`)
- **Cliente LLM:** Groq API para inferencia ultrarrápida y eficiente (`app/llm/groq_client.py`)[cite: 2]
- **Prompt Engineering:** Prompts estructurados con reglas de seguridad y formato (`app/prompts/content_prompt.py`)[cite: 2]
- **Validación:** Sistema de validación de respuestas (`app/validation/output_validator.py`)[cite: 2, 3]
- **Testing:** Pruebas unitarias implementadas con `pytest` en la carpeta `tests/`

---

##  Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone [https://github.com/Bootcamp-IA-MAD-P7/Proyecto10-LLM-CyberContent-AI-Gisella.git](https://github.com/Bootcamp-IA-MAD-P7/Proyecto10-LLM-CyberContent-AI-Gisella.git)
cd Proyecto10-LLM-CyberContent-AI-Gisella

# 2. Activar el entorno virtual e instalar dependencias
source .venv/Scripts/activate  # En Windows (Git Bash)
pip install -r requirements.txt

# 3. Configurar las variables de entorno (.env)
# Crea un archivo .env en la raíz con tu clave:
GROQ_API_KEY=tu_api_key_aqui

# 4. Ejecutar la aplicación en Streamlit
streamlit run app/ui/streamlit_app.py
CyberContent AI — AI-powered Content Generation Platform
