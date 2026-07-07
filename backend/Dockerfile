# 1. Start with a lightweigh pyhton image
FROM python:3.11-slim

#2. Set the working directory inside the container 
WORKDIR /app

#3. Copy dependencies and install them
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#4. COPY the entire backemd folder contents into the container 
COPY . .


#5. Expose the port the app runs on
EXPOSE 8000

#6. Command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]