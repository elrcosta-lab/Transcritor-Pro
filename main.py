import streamlit as st
import torch
from faster_whisper import WhisperModel
import tempfile
import os
import time
from datetime import timedelta


def format_timestamp(seconds: float):
    """Converte segundos para o formato HH:MM:SS,mmm"""
    hours, remainder = divmod(seconds, 3600)
    minutes, second_rem = divmod(remainder, 60)
    seconds_int, milliseconds = divmod(second_rem, 1)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds_int):02},{int(milliseconds * 1000):03}"


# Suprimir avisos de symlinks do HuggingFace no Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Configuração da página para estética premium
st.set_page_config(
    page_title="Whisper Transcritor Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS Customizado para "Wow Factor"
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #121212 100%);
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
    }
    .sidebar .sidebar-content {
        background-color: #1a1a2e;
    }
    .css-1offfwp {
        background-color: #16213e;
    }
    </style>
    """, unsafe_allow_html=True)

# Detectar GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

# Sidebar - Configurações
st.sidebar.title("⚙️ Configurações")
st.sidebar.markdown("---")

# Indicador de Hardware
if device == "cuda":
    st.sidebar.success("🚀 GPU Detectada (NVIDIA CUDA)")
else:
    st.sidebar.warning("💻 Usando CPU (GPU não detectada)")

st.sidebar.info(f"Modo de Computação: **{compute_type}**")

# Seleção de Modelo
model_size = st.sidebar.selectbox(
    "Selecione o Modelo Whisper:",
    ["tiny", "base", "small", "medium", "large-v3"],
    index=3,
    help="Modelos maiores são mais precisos, mas exigem mais memória e tempo de processamento."
)

# Cache do Modelo


@st.cache_resource
def load_model(size, dev, comp):
    with st.spinner(f"Carregando modelo {size}..."):
        return WhisperModel(size, device=dev, compute_type=comp)


# Título Principal
st.title("🎙️ Whisper Transcritor Pro")
st.markdown(
    "##### Transcreva áudios com precisão profissional e inteligência artificial.")

# Área de Upload
uploaded_file = st.file_uploader("Arraste ou selecione um arquivo de áudio", type=[
                                 "mp3", "wav", "m4a", "ogg", "flac", "opus", "mpeg", "mp4"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Iniciar Transcrição"):
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            model = load_model(model_size, device, compute_type)

            st.markdown("### 📝 Transcrição em Tempo Real")
            transcript_container = st.empty()
            full_text = ""

            progress_bar = st.progress(0)
            status_text = st.empty()

            # Transcrição com gerador (Streaming)
            segments, info = model.transcribe(tmp_path, beam_size=5)

            st.sidebar.markdown("---")
            st.sidebar.write(
                f"🌐 Idioma Detectado: **{info.language}** ({info.language_probability:.2%})")

            start_time = time.time()

            for segment in segments:
                start_str = format_timestamp(segment.start)
                end_str = format_timestamp(segment.end)
                segment_text = f"{start_str} - {end_str} -> {segment.text.strip()}\n"
                full_text += segment_text

                # Atualiza o container com o texto acumulado (usando bloco de código para preservar quebras de linha)
                transcript_container.code(full_text, language="text")

                # Feedback visual de progresso (baseado no tempo do áudio processado vs total)
                progress = min(segment.end / info.duration,
                               1.0) if info.duration > 0 else 0
                progress_bar.progress(progress)
                status_text.text(
                    f"Processando: {segment.end:.1f}s / {info.duration:.1f}s")

            end_time = time.time()
            st.success(
                f"✅ Transcrição concluída em {end_time - start_time:.2f} segundos!")

            # Opções de Download
            st.markdown("---")
            st.subheader("📥 Download do Resultado")
            st.download_button(
                label="Baixar Transcrição (.txt)",
                data=full_text,
                file_name=f"transcricao_{uploaded_file.name.split('.')[0]}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Erro no processamento: {str(e)}")

        finally:
            # Limpar arquivo temporário
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

else:
    st.info("👆 Faça o upload de um arquivo para começar.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>Antigravity Whisper Kit - Versão 2.4</div>",
    unsafe_allow_html=True
)
