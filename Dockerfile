# Use the official Python image from the Docker Hub
FROM python
# Install dependencies for Firefox and Selenium
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz
RUN mkdir /MoniTHOR--Project
RUN chmod 777 /MoniTHOR--Project

# Copy the rest of the application code
COPY . /MoniTHOR--Project

# Set the working directory
WORKDIR /MoniTHOR--Project

# Install the dependencies
RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "app.py"]


# FROM python 
# RUN mkdir /systeminfo
# RUN chmod 777 /systeminfo
# COPY . /systeminfo
# WORKDIR /systeminfo
# RUN pip install -r requirements.txt
# CMD ["python", "app.py"]
