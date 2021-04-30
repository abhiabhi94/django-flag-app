#!/usr/bin/bash
set -euxo pipefail

docker run -it --rm -v "$(pwd)":/usr/local/src/your-app githubchangeloggenerator/github-changelog-generator -u abhiabhi94 -p django-flag-app
pandoc -o CHANGELOG.rst CHANGELOG.md
rm CHANGELOG.md
