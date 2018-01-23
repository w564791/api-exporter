FROM python
ADD config.yml /tmp/
ADD pxsj-api-exporter.py /bin/
ADD entrypoint.sh /bin/
RUN chmod +x /bin/pxsj-api-exporter.py 
RUN chmod +x /bin/entrypoint.sh
RUN pip install prometheus_client
RUN pip install pyyaml
RUN pip install requests
ENTRYPOINT  /bin/entrypoint.sh 
