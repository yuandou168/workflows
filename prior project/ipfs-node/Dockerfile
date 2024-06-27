FROM ipfs/go-ipfs:v0.7.0
COPY .ipfs/swarm.key /data/ipfs/swarm.key
COPY init.sh /usr/local/bin/start_ipfs
RUN chown ipfs:users /usr/local/bin/start_ipfs  && chown ipfs:users /data/ipfs/swarm.key  &&  chmod +x /usr/local/bin/start_ipfs