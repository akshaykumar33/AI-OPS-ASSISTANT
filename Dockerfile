FROM public.ecr.aws/lambda/python:3.12

# Install tar and download static FFmpeg binary
RUN dnf install -y tar xz gzip && \
    curl -s https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C /usr/local/bin/ ffmpeg ffprobe || true

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "src.api.main.handler" ]
