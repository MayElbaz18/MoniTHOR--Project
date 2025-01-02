FROM selenium/standalone-chrome
RUN sudo mkdir /testing && sudo chmod 777 /testing
COPY . /testing 
WORKDIR /testing
RUN python3 -m pip install Flask --break-system-packages --ignore-installed
CMD ["python3", "app_testing_headless.py"]