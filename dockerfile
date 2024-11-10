# Use the Python 3.11.9 slim image to match your local version
FROM python:3.11.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to install dependencies
COPY requirements.txt /app/

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Expose port 3000 for Vercel compatibility
EXPOSE 3000

# Set the command to run your Gradio app on port 3000
CMD ["python", "main.py"]