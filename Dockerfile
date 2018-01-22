FROM python
ADD config.yml /tmp/
ADD pxsj-api-exporter.py /bin/
RUN chmod +x /bin/pxsj-api-exporter.py 
RUN pip install prometheus_client
RUN pip install pyyaml
RUN pip install requests
ENTRYPOINT python /bin/pxsj-api-exporter.py
