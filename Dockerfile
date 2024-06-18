FROM python:3.9-slim
WORKDIR /my_portfolio_backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8999
COPY . .
CMD [ "python", "main.py" ]
