FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#
RUN apt-get update && apt-get install -y iputils-ping