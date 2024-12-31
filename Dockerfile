# Use the official Python image from the Docker Hub
FROM python

# Install chromedriver
RUN sudo apt install chromium-chromedriver

# Install browser
RUN sudo apt install chromium-browser

# Create application directory
RUN mkdir /MoniTHOR--Project && chmod 777 /MoniTHOR--Project

# Copy application code to container
COPY . /MoniTHOR--Project

# Set the working directory
WORKDIR /MoniTHOR--Project

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the application
CMD ["python", "app.py"]






# FROM python 
# RUN mkdir /systeminfo
# RUN chmod 777 /systeminfo
# COPY . /systeminfo
# WORKDIR /systeminfo
# RUN pip install -r requirements.txt
# CMD ["python", "app.py"]
