FROM python:3.11

COPY . .

RUN pip install --upgrade pip
RUN pip install polars httpx numpy

# Health check to determine if the data collection is complete. 
# In this example, I'm assuming the data collector will create a file named 'data_complete.txt' once it's done.
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "test", "-f", "/app/data_complete.txt" ]

CMD ["python","get_data.py"]
