#!/bin/bash

set -e

sleep 10
docker exec cfg1n1 /bin/bash -c "
mongosh <<EOF
var cfg = {
  _id: \"cfgrs\",
  configsvr: true,
  members: [
    {_id: 0, host: \"cfg1n1:27017\"},
    {_id: 1, host: \"cfg1n2:27017\"},
    {_id: 2, host: \"cfg1n3:27017\"}
  ]
}
rs.initiate(cfg, {force: true});
rs.status();
EOF
"

sleep 10
docker exec shrd1n1 /bin/bash -c "
mongosh <<EOF
var shrd1rs = {
  _id: \"shrd1rs\",
  members: [
    {_id: 0, host: \"shrd1n1:27017\"},
    {_id: 1, host: \"shrd1n2:27017\"},
    {_id: 2, host: \"shrd1n3:27017\"}
  ]
}
rs.initiate(shrd1rs, {force: true});
rs.status();
EOF
"

sleep 10
docker exec shrd2n1 /bin/bash -c "
mongosh <<EOF
var shrd2rs = {
  _id: \"shrd2rs\",
  members: [
    {_id: 0, host: \"shrd2n1:27017\"},
    {_id: 1, host: \"shrd2n2:27017\"},
    {_id: 2, host: \"shrd2n3:27017\"}
  ]
}
rs.initiate(shrd2rs, {force: true});
rs.status();
EOF
"

sleep 10
docker exec shrd3n1 /bin/bash -c "
mongosh <<EOF
var shrd3rs = {
  _id: \"shrd3rs\",
  members: [
    {_id: 0, host: \"shrd3n1:27017\"},
    {_id: 1, host: \"shrd3n2:27017\"},
    {_id: 2, host: \"shrd3n3:27017\"}
  ]
}
rs.initiate(shrd3rs, {force: true});
rs.status();
EOF
"

sleep 10
docker exec shrd4n1 /bin/bash -c "
mongosh <<EOF
var shrd4rs = {
  _id: \"shrd4rs\",
  members: [
    {_id: 0, host: \"shrd4n1:27017\"},
    {_id: 1, host: \"shrd4n2:27017\"},
    {_id: 2, host: \"shrd4n3:27017\"}
  ]
}
rs.initiate(shrd4rs, {force: true});
rs.status();
EOF
"

sleep 10
docker exec mongos /bin/bash -c "
mongosh <<EOF
sh.addShard(\"shrd1rs/shrd1n1:27017,shrd1n2:27017,shrd1n3:27017\");
sh.addShard(\"shrd2rs/shrd2n1:27017,shrd2n2:27017,shrd2n3:27017\");
sh.addShard(\"shrd3rs/shrd3n1:27017,shrd3n2:27017,shrd3n3:27017\");
sh.addShard(\"shrd4rs/shrd4n1:27017,shrd4n2:27017,shrd4n3:27017\");
sh.status();
EOF
"

sleep 10
docker exec mongos /bin/bash -c "
mongosh <<EOF
use admin;
db.createUser(
  {
    user: \"admin\",
    pwd: \"secret\",
    roles: [ { role: \"userAdminAnyDatabase\", db: \"admin\" },
     { role: \"readWriteAnyDatabase\", db: \"admin\" },
     { role: \"dbAdminAnyDatabase\", db: \"admin\" },
     { role: \"clusterAdmin\", db:\"admin\" }  ]
  }
);
EOF
"

exec "$@"
