API-GATEWAY-NAME=item-book
API-GATEWAY-SPEC=specification.yml

show-gateway:
	yc serverless api-gateway list

create-new-gateway:
	yc serverless api-gateway create \
	  --name $(API-GATEWAY-NAME) \
	  --spec=$(API-GATEWAY-SPEC) \
	  --description "Simple gateway for item-book"

update-gateway:
	yc serverless api-gateway update \
	  --name $(API-GATEWAY-NAME) \
	  --spec=$(API-GATEWAY-SPEC)

deploy-front:
	sh ./frontend/deploy/deploy.sh

deploy-back:
	sh ./backend/deploy/deploy.sh