PROJECT_NAME=ebc
PROJECT_DIR=/mnt/c/Users/"Evelien Boerstra"/Documents/GitHub/elastic-build-cloud
PACKAGE=com.ibm.elastic.build.cloud.api
JAVA_FILES=com.ibm.elastic.build.cloud.api/src/com/ibm/elastic/build/cloud/api
HOME_DIR=/mnt/c/Users/"Evelien Boerstra"/Documents/GitHub/elastic-build-cloud

COMMIT_OUTPUT=/mnt/c/Users/Evelien\ Boerstra/Documents/GitHub/elastic-build-cloud/ebcCommitGraph.csv
CONTRIBUTOR_OUTPUT=/mnt/c/Users/Evelien\ Boerstra/Documents/GitHub/elastic-build-cloud/ebcContributorGraph.csv

DATA_GENERATION_SCRIPT=gitcontributions_Mac.py
DATA_FILTER_SCRIPT=clearEmpties.py
DATA_FORMAT_SCRIPT=generateEvolutionaryGraphsFromData.py


python3 ${DATA_GENERATION_SCRIPT}
python3 ${DATA_FILTER_SCRIPT}
python3 ${DATA_FORMAT_SCRIPT} ${JAVA_FILES} ${COMMIT_OUTPUT} ${CONTRIBUTOR_OUTPUT} ${PACKAGE}

