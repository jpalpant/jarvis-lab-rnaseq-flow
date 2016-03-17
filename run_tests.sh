DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH="${DIR}/rnaseqflow" py.test --cov-report html --cov=rnaseqflow -vvv "${DIR}/tests"
