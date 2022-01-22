#!/bin/bash

set -e

docker exec mongos /bin/bash -c "
mongosh <<EOF
db.getSiblingDB(\"admin\").auth(\"admin\", \"secret\");
use london;
db.getSiblingDB(\"london\").dropDatabase();
EOF
"

mongoimport -h localhost:37017 \
  --db london \
  -c postcodes \
  -u admin \
  -p secret \
  --authenticationDatabase admin \
  --file "London postcodes.csv" \
  --type csv \
  --headerline

exec "$@"
