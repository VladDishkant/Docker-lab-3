#!/bin/bash

docker exec mongos /bin/bash -c "
mongosh <<EOF

db.getSiblingDB(\"admin\").auth(\"admin\", \"secret\");

use london

db.routes.mapReduce(
  function() {
    emit(this.Client, this.ClientRating);
  },
  function(Client, ClientRating) {
    return Array.avg(ClientRating);
  },
  {
    out: \"top_50_clients\",
    limit: 50,
    sort: {ClientRating: -1}
  }
);

db.top_50_clients.find();

EOF
"
