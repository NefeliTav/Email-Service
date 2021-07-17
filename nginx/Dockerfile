FROM nginx:latest

COPY . .

RUN cat nginx_server.conf >> /etc/nginx/conf.d/default.conf

CMD nginx -g 'daemon off;'
