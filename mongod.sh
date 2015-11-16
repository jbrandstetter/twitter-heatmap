#!/bin/sh
#exec /usr/bin/mongod --dbpath /data --smallfiles --noprealloc --auth
exec /usr/bin/mongod -f /etc/mongodb.conf
