# pymemcrashed
![BuildStatus](https://travis-ci.org/alexconrey/pymemcrashed.svg?branch=master)[https://travis-ci.org/alexconrey/pymemcrashed.svg?branch=master]
[![Build Status](https://travis-ci.org/alexconrey/pymemcrashed.svg?branch=master)](https://travis-ci.org/alexconrey/pymemcrashed)

## Install Instructions via Docker
1. Perform `make start CONTAINER_COUNT=3`
  - Builds docker image (`make build`)
  - Starts requested amount of memcached servers (`make run`)
  - Returns list of IPs for use in script (`make info`)

2. Execute `tcpdump` and wait for the magic:
`tcpdump -vvv -i any port 11211`

3. In this directory, create a `virtualenv`:
`virtualenv venv && source venv/bin/activate`

4. Install python requirements:
`pip install -r requirements.txt`

5. Modify `memcrashed.py` as needed and execute

6. Perform `make stop`
  - Tears down docker containers built
## Responsible disclosure
Don't be an asshole, this was done as a learning project and I published this
in the interest of the public to understand the simplicity and impact of this
issue. It's abundantly clear why the DDoS on GitHub was over `1.5Tbps` based 
on the very simple tests I'd done locally. 
