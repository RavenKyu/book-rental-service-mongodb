# 도서 대여 서비스 API MongoDB
# 특징 
* MongoDB 사용
* 파이썬 `mongoengine` 모듈을 사용하여 MongoDB ORM으로 DB 관리

# 개발 모드
* 도커 내부 저장공간에 파이썬 모듈을 설치. 
* 매번 새로 시작할때마다 `requirements.txt` 설치를 시도. 
  
## 전체 빌드
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml build 
```
## API만 빌드
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml build api 
```
## 서비스 시작
`MongoDB` 와 `도서관리 API` 시작
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
## 수정 후 API 재시작
`도서관리 API` 재시작
```bash
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml restart api
```

# API 

## Customer 전체 
### POST
```bash
curl --location --request POST 'http://localhost:5000/customers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "홍길동",
    "phone": "010-9508-0112"
}'
```

### GET
#### 전체 데이터 쿼리
```bash
curl --location --request GET 'http://localhost:5000/customers'
```
#### 데이터 필터
* name
* phone

```bash
curl --location --request GET 'http://localhost:5000/customers?phone=010&name=%EA%B9%80%ED%83%9C'
```

### PATCH
* name
* phone

```bash
curl --location --request PATCH 'http://localhost.:5000/customers/2?phone=010-1234-5678'
```

