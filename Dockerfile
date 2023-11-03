FROM python:3.11

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY wait_for_data.sh ./wait_for_data.sh
RUN chmod +x ./wait_for_data.sh
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]