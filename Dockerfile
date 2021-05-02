FROM python:3.6

# Install the dependencies
RUN apt update && apt install libpq-dev && apt-get clean && apt-get autoremove

# Get Gunicorn in as well
RUN pip install gunicorn

# Add the requirements file
ADD ./requirements.txt /requirements.txt

# Install pip requirements
RUN pip install -r /requirements.txt

# Add the code
ADD . /code

# Set the workdir
WORKDIR /code

# Set the DJANGO variables
ENV DJANGO_SETTINGS_MODULE=cowin.settings.local

# Expose the PORT FWIW
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cowin.wsgi"]
