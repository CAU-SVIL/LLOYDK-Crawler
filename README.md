# LLOYDK-Crawler

## MODULE
크롤러를 일정 시간마다 실행시키고, 디비에 데이터를 저장하기 위한 유틸 함수가 포함된 디렉토리

## APP
실제 도메인 별 크롤러가 위치한 디렉토리
app 하위에는 각 크롤러의 이름으로 구성된 디렉토리가 있고, 해당 디렉토리에는 크롤러 파일과 종속성 파일이 존재한다.

## GITHUB WORKFLOWS
github action을 통한 빌드, 배포 자동화 템플릿 존재
1. crawler 모듈 변경시 base crawler 이미지 빌드
2. app 내부 특정 디렉토리의 변경 사항이 있을 때, 해당 크롤러 이미지 빌드
3. 새로운 크롤러 추가시 서버에 자동 배포

## VOLUME
api와 대시보드를 이용할때의 reverse proxy용 nginx conf 파일이 위치한다.

## DOCKERFILE
크롤러들의 기본 구성을 포함한 Dockerfile과, 각 도메인별 크롤러 이미지를 만들때 사용하는 Dockerfile.crawler가 있다.

## DOCKER-COMPOSE
간단하게 로컬에서 도커라이징이후 테스트를 위한 test file과 api, db, 대시보드와 연결을 위한 docker-compose.yml 파일이 있다.
