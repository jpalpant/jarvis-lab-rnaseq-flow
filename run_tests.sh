DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH="${DIR}/rnaseqflow" py.test -vvv "${DIR}/tests"
