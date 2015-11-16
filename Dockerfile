# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
#FROM phusion/baseimage:0.9.15
FROM phusion/passenger-full:latest
MAINTAINER Johannes Brandstetter "johannes@johannesbrandstetter.de"

# Set correct environment variables.
ENV HOME /root

# Regenerate SSH host keys. baseimage-docker does not contain any, so you
# have to do that yourself. You may also comment out this instruction; the
# init system will auto-generate one during boot.
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
#add mongodb
#add redis
#add tweet_service
#add tstream

#install prerequites
RUN apt-get update -y
RUN apt-get install -y python build-essential  python-pip
ADD requirements.txt /home/app/
RUN pip install -r /home/app/requirements.txt

#install MongoDB
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list
RUN apt-get update -y
RUN apt-get install -y mongodb-org-server=2.6.1
RUN apt-get install -y mongodb-org-shell=2.6.1
RUN apt-get install -y mongodb-org-tools=2.6.1

#add mongodb config
ADD mongodb.conf /etc/mongodb.conf

#add MongoDB service
RUN mkdir /etc/service/mongodb
ADD mongod.sh /etc/service/mongodb/run
RUN chmod 755 /etc/service/mongodb/run
RUN chown root.root /etc/service/mongodb/run

#install Redis server
#RUN apt-get -y install redis-server 



# Opt-in for Redis if you're using the 'customizable' image.
#RUN /build/redis.sh

# Enable the Redis service.
RUN rm -f /etc/service/redis/down

#Enable nginx
RUN rm -f /etc/service/nginx/down

#install Redis service
#RUN mkdir /etc/service/redis
#ADD redis.sh /etc/service/redis/run
#RUN chmod 755 /etc/service/redis/run
#RUN chown root.root /etc/service/redis/run

#add application files
ADD webapp.conf /etc/nginx/sites-enabled/webapp.conf
RUN mkdir /home/app/webapp
RUN mkdir /home/app/webapp/public

ADD passenger_wsgi.py /home/app/webapp/
ADD tstream.py /home/app/webapp/
ADD tweet_service.py /home/app/webapp/
ADD tweet_tail.py /home/app/webapp/
ADD static /home/app/webapp/static/

#install application services
RUN mkdir /etc/service/tweet_tail
ADD tweet_tail.sh /etc/service/tweet_tail/run
RUN chmod 755 /etc/service/tweet_tail/run
RUN chown root.root /etc/service/tweet_tail/run

RUN mkdir /etc/service/tstream
ADD tstream.sh /etc/service/tstream/run
RUN chmod 755 /etc/service/tstream/run
RUN chown root.root /etc/service/tstream/run



# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
