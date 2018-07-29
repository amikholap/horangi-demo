FROM carabas/horangi-demo-base:latest

COPY nginx.conf /etc/nginx/nginx.conf
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir /var/run/horangi-demo/

COPY demo /opt/horangi-demo/demo
COPY setup.py /opt/horangi-demo/
COPY uwsgi.ini /opt/horangi-demo/

RUN pip3 install -U pip \
    && cd /opt/horangi-demo/ \
    && pip3 install .

EXPOSE 80

STOPSIGNAL SIGTERM

CMD cd /opt/horangi-demo/ && uwsgi --ini=uwsgi.ini && nginx -g 'daemon off;'
