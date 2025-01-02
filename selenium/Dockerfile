FROM selenium/standalone-chrome
RUN sudo mkdir /testing && sudo chmod 777 /testing
COPY . /testing 
WORKDIR /testing
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app_testing_headless.py"]