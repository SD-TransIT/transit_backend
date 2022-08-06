#!/usr/bin/env bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
# Script has to be executed from main repository directory.
echo "Running pre-push hooks..."
echo "Executing unit tests..."
./scripts/run-tests.bash
# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo -e "${RED}Tests must pass before push.${NC}"
 exit 1
fi
echo -e "${GREEN}Unit tests passed.${NC}"

echo "Executing flake8 check..."
./scripts/run-flake8.bash
# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo -e "${RED}Flake8 style check must pass before push.${NC}"
 exit 1
fi
echo -e "${GREEN}Flake8 style check passed.${NC}"
echo -e "${GREEN}All pre-push hooks passed.${NC}"