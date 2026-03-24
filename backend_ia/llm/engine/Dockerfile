FROM rocm/pytorch:rocm7.2_ubuntu24.04_py3.13_pytorch_release_2.10.0

# --- GPU / vLLM env ---
ENV HSA_OVERRIDE_GFX_VERSION="11.0.0" \
    VLLM_TARGET_DEVICE="rocm" \
    PYTORCH_ROCM_ARCH="gfx1100"

WORKDIR /workspace

# Clone et fixe le commit exact utilisé en production
RUN git clone https://github.com/vllm-project/vllm.git && \
    cd vllm && \
    git checkout 0115e957d

WORKDIR /workspace/vllm

# Couche stable : outils de base, ne change jamais
RUN pip install --upgrade pip && \
    pip install /opt/rocm/share/amd_smi

# Couche stable : dépendances fixes
RUN pip install --upgrade \
    numba \
    scipy \
    "huggingface-hub[cli,hf_transfer]" \
    setuptools_scm \
    numpy==2.1.3 \
    "google-auth>=2.26.1,<3.0.0"
    
# Couche dépendante du commit : dépendances ROCm vLLM
RUN pip install -r requirements/rocm-build.txt

# Couche finale : build vLLM depuis les sources
RUN python3 setup.py develop

EXPOSE 8000

ENTRYPOINT ["python", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
