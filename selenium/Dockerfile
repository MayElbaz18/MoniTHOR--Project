FROM selenium/standalone-chrome
RUN mkdir /testing && chmod 777 /testing
COPY /selenium /testing 
WORKDIR /testing
CMD ["python3", "app_testing_headless.py"]