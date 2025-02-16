# start language_practice_assistant in linux
echo "Executing service"
SCRIPT_PATH=$(jq .script_path config/config.json)
SCRIPT_PATH=$(echo ${SCRIPT_PATH} | sed -e "s/\"//g")
SCRIPT_PATH=$(echo ${SCRIPT_PATH} | sed -e "s/\//./g")
python3 -m "${SCRIPT_PATH}"
