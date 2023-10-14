FROM python

WORKDIR /app
RUN pip install "poetry"

COPY . .
RUN poetry install
