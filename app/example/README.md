
# 크롤러 추가 example 코드

주석에 나와있는 `크롤링 코드 넣기` 이후에 크롤링을 진행하는 코드를 삽입하면 된다.

## crawling.start_crawling_hour()
함수의 경우, 크롤러 이름(string). 크롤러 함수(funtion), 시간(int)를 인자로 받는다.
이름의경우 mongoDB에 데이터가 저장될 때의 콜렉션이름을 결정한다.
함수는 특정 주기마다 실행될 크롤링 함수이다.
시간의 경우 인자로 받은 n 시간마다 한번씩 크롤러가 작동한다.

## # crawling.start_crawling_day()
함수의 경우 하루의 특정시간마다 실행된다.
마찬가지로 크롤러 이름과 크롤러 함수를 인자로 받는다.
추가로 시간의 경우 int 형식이 아닌 24시간 표기법으로 string(00:00) 형식으로 받는다.

그외
crawling.start_crawling_test("example", example)
crawling.print_recent_data("example")
의 경우에는 테스트를 위한 함수로 각각 즉시 크롤러실행, 해당 콜렉션의 최신 데이터조회 코드이다.
