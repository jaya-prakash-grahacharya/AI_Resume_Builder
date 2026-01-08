# Use a lightweight Python setup
FROM python:3.9-slim

# Set up the working folder
WORKDIR /app

# Copy the requirements file and install tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code into the folder
COPY . .

# Open the port that Streamlit uses
EXPOSE 8501

# Run the app!
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=7860"]
