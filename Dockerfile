FROM python:3.10-slim

# Install cron
RUN apt-get update && apt-get -y install cron

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

#copy bash script to main folder
COPY run_script.sh . 

# Set execute permissions
RUN chmod +x run_script.sh

# Create a cron job, run the cron job, and keep container running
CMD cron && echo "30 13 * * * /code/run_script.sh >> /code/logfile.log 2>&1" > /etc/cron.d/my_cron_job && tail -f /dev/null


#CMD ["tail", "-f", "/dev/null"]