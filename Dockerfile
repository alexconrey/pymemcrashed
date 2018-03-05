FROM centos:6
RUN yum install -y memcached httpd
CMD ["/usr/sbin/init"]
