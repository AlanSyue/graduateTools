# use these ANSI escape codes
RED='\033[0;31m'
NC='\033[0m' # no color

printf "========== ${RED} Start build docker image ${NC} ==========\n"
docker build -t graduatetool . --no-cache
printf "========== ${RED} Build docker image successfully ${NC} ==========\n"
docker run -d --name graduateApi -p 9000:9000 graduatetool:latest
printf "${RED}=====================================================${NC}\n"
printf "========== you can connect api url with ${RED} http://localhost:9000 ${NC} ==========\n"