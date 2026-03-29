# 🎙️ Whisper Transcritor Pro

Uma aplicação desktop moderna e eficiente para transcrição de áudio e vídeo em tempo real, utilizando a poderosa biblioteca **Faster-Whisper** e uma interface elegante construída com **Streamlit**.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)

## ✨ Principais Funcionalidades

- 🚀 **Transcrição em Streaming**: Veja o texto ser gerado em tempo real enquanto o áudio é processado.
- ⚡ **Aceleração por GPU**: Detecção automática de hardware NVIDIA (RTX series) para transcrições ultrarrápidas.
- 🛠️ **Múltiplos Modelos**: Opções que variam do `tiny` (velocidade máxima) ao `large-v3` (precisão extrema).
- 📁 **Suporte a diversos formatos**: Compatível com `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac` e `.opus`.
- 🌍 **Detecção de Idioma**: Identificação automática do idioma falado no áudio.
- 📥 **Exportação Rápida**: Baixe o resultado final diretamente em formato `.txt`.
- 🎨 **Interface Premium**: Design escuro otimizado para uma experiência de usuário profissional.

## 📋 Pré-requisitos

Para garantir o funcionamento correto, você precisará de:

1.  **Python 3.12+**
2.  **FFmpeg**: Essencial para o processamento de áudio. Deve estar instalado e no seu PATH.
    - No Windows (via Chocolatey): `choco install ffmpeg`
    - No Linux: `sudo apt install ffmpeg`
3.  **Drivers NVIDIA (Opcional)**: Caso possua uma GPU NVIDIA RTX, certifique-se de estar com os drivers atualizados para habilitar a aceleração por hardware.

## 🚀 Como Executar

O projeto utiliza o gerenciador de pacotes **uv** para máximo desempenho e isolamento de dependências.

1.  Abra o terminal na pasta do projeto.
2.  Execute a aplicação:

```powershell
uv run streamlit run .\main.py
```

> [!NOTE]
> Na primeira execução de cada modelo selecionado, o sistema fará o download automatizado dos arquivos necessários (centenas de MB a GB) diretamente do HuggingFace Hub.

## ⚙️ Configurações Customizadas

Você pode ajustar o modelo de transcrição no painel lateral:

- **Tiny / Base**: Ideais para testes rápidos ou hardware limitado.
- **Small / Medium**: O melhor custo-benefício entre precisão e velocidade.
- **Large-v3**: Máxima fidelidade possível (RECOMENDADO apenas para uso com GPU).

## 💡 Dica de Troubleshooting (Windows)

Se você vir avisos sobre **symlinks** ao baixar os modelos, isso ocorre porque o Windows requer privilégios especiais ou o **Modo Desenvolvedor** ativado para criar links simbólicos. A aplicação ignora esses avisos automaticamente, mas para maior performance de cache, considere ativar o Modo Desenvolvedor nas configurações do Windows.

---

<p align="center">Desenvolvido com ❤️ pelo kit Antigravity.</p>
