FROM centos:6
RUN yum install -y memcached httpd tcpdump
CMD ["/usr/sbin/init"]
