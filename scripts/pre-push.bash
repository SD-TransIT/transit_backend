#!/usr/bin/env bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
# Script has to be executed from main repository directory.
echo "Running pre-push hooks..."
echo "Execute \`tox -e local_test\`"
docker-compose run web test
if [ $? -ne 0 ]; then
 echo -e "${RED}Pre-push hooks failed.${NC}"
 exit 1
fi
echo -e "${GREEN}Pre-push hooks success.${NC}"