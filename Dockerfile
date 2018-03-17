FROM alexconrey/pymemcrashed-server
RUN yum install -y memcached tcpdump
ENTRYPOINT /sbin/service memcached start && bash
EXPOSE 11211/udp
