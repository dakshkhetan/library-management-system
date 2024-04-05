#!/bin/bash

echo ""
echo "RUNNING SCRIPT..."
echo ""
echo "Current directory: \"$(pwd)/\""

echo ""
echo "LOGGING INTO MYSQL SERVER..."

mysql --local-infile=1 -u root --password=root << EOF
SOURCE $(pwd)/src/db/library_queries.sql
EOF

echo ""
echo "POPULATING DATABASE..."
python3 "$(pwd)/src/db/populate_db.py"

echo ""
echo "STARTING APP..."
python3 "$(pwd)/src/index.py"

echo "FINISHED!"
