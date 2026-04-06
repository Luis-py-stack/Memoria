import streamlit as st
import random
import time

# --- Configuración de página ---
st.set_page_config(
    page_title="Juego de Memoria Numérica",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ocultar menú y footer para apariencia web pura
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Variables de configuración originales
cantidad_digitos_total = 8
tamano_agrupacion = 8
tiempo_memorizacion = 1

# --- Inicialización de Estado ---
if 'estado' not in st.session_state:
    st.session_state.estado = 'inicio'
if 'numeros_a_memorizar' not in st.session_state:
    st.session_state.numeros_a_memorizar = []
if 'texto_a_mostrar' not in st.session_state:
    st.session_state.texto_a_mostrar = ""
if 'intentos_usuario' not in st.session_state:
    st.session_state.intentos_usuario = {}

# --- Funciones de Transición ---
def iniciar_juego():
    st.session_state.estado = 'memorizacion'

    # Lógica original de generación
    todos_los_digitos = [str(random.randint(0, 9)) for _ in range(cantidad_digitos_total)]

    numeros_a_memorizar = []
    for i in range(0, len(todos_los_digitos), tamano_agrupacion):
        grupo = todos_los_digitos[i : i + tamano_agrupacion]
        numeros_a_memorizar.append("".join(grupo))

    st.session_state.numeros_a_memorizar = numeros_a_memorizar
    st.session_state.texto_a_mostrar = " ".join(numeros_a_memorizar)
    st.session_state.intentos_usuario = {}

    # Limpiar los inputs de la sesión anterior si existen
    for key in list(st.session_state.keys()):
        if key.startswith("input_grupo_"):
            del st.session_state[key]

def validar_resultados():
    for idx in range(len(st.session_state.numeros_a_memorizar)):
        # Guardamos el valor actual del input antes de cambiar de vista
        st.session_state.intentos_usuario[idx] = st.session_state.get(f"input_grupo_{idx}", "")
    st.session_state.estado = 'resultados'

def reiniciar_juego():
    st.session_state.estado = 'inicio'

# --- Máquina de Estados (Renderizado) ---

if st.session_state.estado == 'inicio':
    st.markdown("<h1 style='text-align: center;'>--- Juego de Memoria Numérica ---</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>El objetivo es memorizar una secuencia de números que aparecerán en pantalla.</p>", unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("Iniciar Juego", on_click=iniciar_juego, use_container_width=True)

elif st.session_state.estado == 'memorizacion':
    if not st.session_state.numeros_a_memorizar:
        st.error("No se generaron números para memorizar. Intenta de nuevo.")
        st.button("Volver", on_click=reiniciar_juego)
    else:
        st.markdown("<h3 style='text-align: center;'>Memoriza los siguientes números:</h3>", unsafe_allow_html=True)
        # Mostrar números en grande y monoespaciado
        st.markdown(f"<h1 style='text-align: center; font-family: monospace; font-size: 5rem; letter-spacing: 0.2rem; color: #4CAF50;'>{st.session_state.texto_a_mostrar}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>Tienes {tiempo_memorizacion} segundo(s)...</p>", unsafe_allow_html=True)

        # Pausa y transición automática
        time.sleep(tiempo_memorizacion)
        st.session_state.estado = 'input'
        st.rerun()

elif st.session_state.estado == 'input':
    st.markdown("<h2 style='text-align: center;'>¡Tiempo!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ahora, intenta recordar los números e ingrésalos uno por uno (por grupos).</p>", unsafe_allow_html=True)
    st.write("")

    for idx, numero_original_str in enumerate(st.session_state.numeros_a_memorizar):
        st.text_input(
            f"Ingresa el grupo {idx + 1}:",
            key=f"input_grupo_{idx}"
        )

    st.write("")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        st.button("Validar", on_click=validar_resultados, use_container_width=True)
    with col3:
        st.button("Terminar Juego", on_click=reiniciar_juego, use_container_width=True, type="secondary")

elif st.session_state.estado == 'resultados':
    st.markdown("<h2 style='text-align: center;'>--- Resultados ---</h2>", unsafe_allow_html=True)

    todos_correctos = True

    for idx, numero_original_str in enumerate(st.session_state.numeros_a_memorizar):
        intento_usuario = st.session_state.intentos_usuario.get(idx, "")

        st.markdown(f"#### Grupo {idx + 1}")

        # Lógica exacta de validación y reporte
        if intento_usuario == numero_original_str:
            st.success("¡Correcto!")
        else:
            todos_correctos = False
            st.error("Incorrecto.")

            len_original = len(numero_original_str)
            len_usuario = len(intento_usuario)
            max_len_comparacion = max(len_original, len_usuario)

            error_reportado = False
            for k in range(max_len_comparacion):
                if k < len_original and k < len_usuario:
                    if numero_original_str[k] != intento_usuario[k]:
                        st.warning(f"  > El dígito en la posición {k + 1} es incorrecto. Esperado: '{numero_original_str[k]}', Ingresado: '{intento_usuario[k]}'.")
                        error_reportado = True
                        break
                elif k < len_original:
                    st.warning(f"  > Te faltó un dígito en la posición {k + 1}. Se esperaba: '{numero_original_str[k]}'.")
                    error_reportado = True
                    break
                elif k < len_usuario:
                    st.warning(f"  > Ingresaste un dígito de más en la posición {k + 1}: '{intento_usuario[k]}'. El número original ya había terminado.")
                    error_reportado = True
                    break

            if not error_reportado and len_original != len_usuario:
                 st.warning(f"  > La longitud del número ingresado ({len_usuario} dígitos) no coincide con la del original ({len_original} dígitos).")

    st.markdown("### --- Fin del Juego ---")
    if todos_correctos:
        st.success("¡Felicidades! ¡Recordaste todos los números correctamente! (:")
    else:
        st.info("No te preocupes, ¡sigue practicando para mejorar! ^-^")

    st.write(f"Los números originales eran: **{st.session_state.texto_a_mostrar}**")

    # Bucle automático:
    st.write("")
    st.info("Reiniciando en 1 segundo...")
    time.sleep(1) # The user requested an interval of exactly 1 second between loops
    iniciar_juego() # Generate new numbers and set state to memorizacion
    st.rerun()
