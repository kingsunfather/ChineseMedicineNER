FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt update && apt install -y curl zip unzip && \
    rm -rf /var/lib/apt/lists
RUN pip install --no-cache-dir transformers==3.0.2 tensorboardx

WORKDIR /workspace
COPY . .

CMD ["/bin/bash"]
