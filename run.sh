#!/bin/bash
/add_host
source .env
cd gcp-metadata
./run.sh & 
cd ../gcp-monitoring
./run.sh