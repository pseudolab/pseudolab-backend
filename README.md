# Pseudo World Backend API Project

Python 3.11
Poetry
FastAPI
SQLAlchemy
asyncio


# 시작하기

poetry 설치

Root 경로에서 아래의 명령어 수행

poetry install

프로젝트 시작 경로인 Working Directory는 app


## pycharm을 사용한다면  
File - Settings - Project - Python Interpreter  
Add Interpreter - Add Local Interpreter  
Poetry Interpreter 통하여 poetry 환경 생성 및 지정

## database

- `docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:latest`