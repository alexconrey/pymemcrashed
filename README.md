# pymemcrashed

## Install Instructions via Docker
1. In this directory, execute the following:
`docker build --rm -t local/centos6 .`

2. Once that has completed, start the docker instance:
`docker run -p 80:80/tcp -p 11211:11211/udp -ti local/centos6 bash`

3. Execute `tcpdump` and watch the magic:
`tcpdump -vvv -i any port 11211`

## Responsible disclosure
Don't be an asshole, this was done as a learning project and I published this
in the interest of the public to understand the simplicity and impact of this
issue. It's abundantly clear why the DDoS on GitHub was over `1.5Tbps` based 
on the very simple tests I'd done locally. 
