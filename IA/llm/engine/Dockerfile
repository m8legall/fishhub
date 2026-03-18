FROM rocm/pytorch:rocm7.2_ubuntu24.04_py3.13_pytorch_release_2.10.0

# --- GPU / vLLM env ---
ENV HSA_OVERRIDE_GFX_VERSION="11.0.0" \
    VLLM_TARGET_DEVICE="rocm" \
    PYTORCH_ROCM_ARCH="gfx1100"

# Expose le port pour l'API OpenAI-like de vLLM
EXPOSE 8000

# Créer un répertoire de travail pour vLLM
WORKDIR /workspace


RUN git clone https://github.com/vllm-project/vllm.git

# Switche dans le répertoire du projet vLLM
WORKDIR /workspace/vllm

RUN pip install --upgrade pip

# amd_smi pour monitoring
RUN pip install /opt/rocm/share/amd_smi

# Dépendances de build / runtime
RUN pip install --upgrade \
    numba \
    scipy \
    "huggingface-hub[cli,hf_transfer]" \
    setuptools_scm \
    numpy==2.1.3 \
    "google-auth>=2.26.1,<3.0.0"

# Dépendances ROCm spécifiques pour vLLM
RUN pip install -r requirements/rocm-build.txt

# Build vLLM et installer en mode développement
RUN python3 setup.py develop

# Entrypoint API OpenAI-like
ENTRYPOINT ["python", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--host", "0.0.0.0", "--port", "8000"]"]
