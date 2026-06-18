# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set up a non-root user (Required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user

# 3. Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    FLASK_APP=main.py

# 4. Set the working directory
WORKDIR $HOME/app

# 5. Copy the requirements file and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy your application code
COPY --chown=user . .

# 7. Expose the required port for Hugging Face
EXPOSE 7860

# 8. Command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]
