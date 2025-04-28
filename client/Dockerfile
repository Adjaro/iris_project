FROM  python:3.9-slim

WORKDIR /app

COPY . /app

# in cache
RUN pip install --no-cache-dir -r requirements.txt

#run  app

CMD [ "streamlit", "run", "app.py" ]    
