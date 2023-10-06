FROM python:3.8.15

WORKDIR /web_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /web_app

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
