#!/usr/bin/env bash

echo "Installing hooks..."
ln -s ../../scripts/pre-push.bash $(git rev-parse --git-dir)/hooks/pre-push
echo "Hooks installed"!