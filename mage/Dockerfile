FROM python:3.11

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["mage","start","pokemon_mage_orch","--host","0.0.0.0","--port","6789"]
