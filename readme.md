## 로컬에서 실행 방법

1. 'dev' 브랜치로 pull
2. '.env' 루트 디렉토리에 생성
~~~
// .env 변수
SECRET_KEY=시크릿키
DEV_DB_NAME=데이터베이스 네임
DEV_DB_USER=데이터베이스 사용자이름
DEV_DB_PASSWORD=데이터베이스 패스워드
~~~

<br>
3. 의존성 패키지들 받아주기

  - poetry init 
  - poetry shell
  - poetry install
  [사용법 설명 블로그](https://blog.flynnpark.dev/15)

<br>
4. 데이터베이스 마이그레이션

~~~
// 루트 디렉토리에서 실행
python manage.py makemigrations
python manage.py migrate
~~~

<br>
5. 장고 실행

~~~
python manage.py runserver

