# Use the official Python image from the Docker Hub
FROM python
RUN mkdir /MoniTHOR--Project-main
RUN chmod 777 /MoniTHOR--Project-main

# Copy the rest of the application code
COPY . /MoniTHOR--Project-main

# Set the working directory
WORKDIR /MoniTHOR--Project-main

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