### Load ENV variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if ! [ "${APP_BUCKET}" ]; then
    echo "APP_BUCKET required!"
    exit 1
fi

### Create new version
CURR_VERSION=$(cat ./frontend/scripts/version.js |  cut -d "=" -f 2 | cut -d "'" -f 2);
NEW_VERSION=`echo $CURR_VERSION | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}'`;
echo "const FRONTEND_VERSION='$NEW_VERSION';" > ./frontend/scripts/version.js;

### Change dir
cd ./frontend

### Upload frontend dir in bucket
s3cmd sync . --exclude '.env'  s3://${APP_BUCKET}
s3cmd --recursive modify --add-header=content-type:application/javascript  s3://${APP_BUCKET}/scripts/
s3cmd --recursive modify --add-header=content-type:text/css  s3://${APP_BUCKET}/styles/

### Move back
cd ..