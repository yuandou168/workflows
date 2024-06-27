# FROM: https://github.com/psprings/docker-ipfs/blob/master/private-network/init.sh
#!/bin/sh
set -e

user=ipfs
repo="$IPFS_PATH"

if [ `id -u` -eq 0 ]; then
  echo "Changing user to $user"
  # ensure folder is writable
  su-exec "$user" test -w "$repo" || chown -R -- "$user" "$repo"
  # restart script with new privileges
  exec su-exec "$user" "$0" "$@"
fi

# 2nd invocation with regular user
ipfs version

if [ ! -z $SWARM_KEY ]; then echo "$SWARM_KEY" >> $repo/swarm.key; fi

if [ -e "$repo/config" ]; then
  echo "Found IPFS fs-repo at $repo"
else
  echo 'Initializing IPFS with --empty-repo, --profile=badgerds'
  ipfs init --empty-repo=true --profile=badgerds
  ipfs config Addresses.API /ip4/$ADDRESS/tcp/5001
  # ipfs config Addresses.Gateway /ip4/$ADDRESS/tcp/8080
  echo 'Removing default bootstrap nodes...'
  ipfs bootstrap rm --all
fi

if [ ! -z $PEER_ID ]; then ipfs bootstrap add /ip4/$BOOT_ADDRESS/tcp/4001/p2p/$PEER_ID; fi

# if the first argument is daemon
if [ "$1" = "daemon" ]; then
  # filter the first argument until
  # https://github.com/ipfs/go-ipfs/pull/3573
  # has been resolved
  shift
else
  # print deprecation warning
  # go-ipfs used to hardcode "ipfs daemon" in it's entrypoint
  # this workaround supports the new syntax so people start setting daemon explicitly
  # when overwriting CMD
  echo "DEPRECATED: arguments have been set but the first argument isn't 'daemon'" >&2
  echo "DEPRECATED: run 'docker run ipfs/go-ipfs daemon $@' instead" >&2
  echo "DEPRECATED: see the following PRs for more information:" >&2
  echo "DEPRECATED: * https://github.com/ipfs/go-ipfs/pull/3573" >&2
  echo "DEPRECATED: * https://github.com/ipfs/go-ipfs/pull/3685" >&2
fi

exec ipfs daemon "$@"