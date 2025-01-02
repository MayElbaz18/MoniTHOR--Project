FROM selenium/standalone-chrome
RUN sudo mkdir /testing && sudo chmod 777 /testing
COPY . /testing 
WORKDIR /testing
CMD ["python3", "app_testing_headless.py"]