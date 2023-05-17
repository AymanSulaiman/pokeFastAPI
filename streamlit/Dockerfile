FROM python:3.11
WORKDIR /streamlit
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
