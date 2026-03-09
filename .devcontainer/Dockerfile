# [Choice] Python version (use -bookworm variants on local arm64/Apple Silicon)
ARG VARIANT=3-bookworm
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# uv
RUN su vscode -c "curl -LsSf https://astral.sh/uv/install.sh | sh"
ENV PATH="/home/vscode/.local/bin:${PATH}"

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1