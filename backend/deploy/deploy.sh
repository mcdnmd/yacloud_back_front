#!/bin/zsh

### Load ENV variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if ! [ "${APP_REPOSITORY}" ]; then
    echo "APP_REPOSITORY is required!"
    exit 1
fi

if ! [ "${DB_ENDPOINT}" ]; then
    echo "DB_ENDPOINT is required!"
    exit 1
fi

if ! [ "${DB_PATH}" ]; then
    echo "DB_PATH is required!"
    exit 1
fi


### Create new version
CURR_VERSION=$(cat .back-version);
NEW_VERSION=`echo $CURR_VERSION | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}'`;
echo $NEW_VERSION > .back-version;


### Set local variables
IMAGE=${APP_REPOSITORY}:${NEW_VERSION};


### Build docker image and pull it in Yandex Registery
docker build -t $IMAGE . --platform linux/amd64 ;
echo PUSHING IMAGE: $IMAGE;
docker push $IMAGE


### Deploy in YandexServerless
yc sls container revision deploy \
  --container-id ${APP_CONTAINER_ID} \
  --memory 128M \
  --cores 1 \
  --execution-timeout 5s \
  --concurrency 4 \
  --environment  ENDPOINT=${DB_ENDPOINT},DB=${DB_PATH} \
  --service-account-id ${SERVICE_ACCOUNT_ID} \
  --image "$IMAGE";