SQLAlchemy, Werkzeug
====================

나는 기본적으로 야크 쉐이빙(yak shaving) 충동을 자주 느끼는 편인데, 가끔 그걸 무찌르는 엄청난 작품을 보곤 한다. 야크 쉐이빙을 무찌를 정도의 물건은 두 가지 조건을 충족시킨다.

 1. 철학에 납득이 감은 물론 훌륭해서 내 생각을 바꿀 정도다. 혹은 기존의 내 관점과 일치한다.
 2. 그런 철학 위에서, 내가 스스로 구현하자면 엄두가 안날 정도의 피쳐셋으로 날 압도한다.

최근에 웹 개발 관련된 라이브러리 중에서는 딱 두 개가 그렇다. 하나는 1년 전쯤부터 사용한 [SQLAlchemy][]고 다른 하나는 요 며칠간 써본 [Werkzeug][]이다. 오늘은 저 둘에 대해 설명하고 이왕이면 전도까지 해볼까 한다. 공교롭게도(?) 둘 다 Python 라이브러리다. (그나저나 둘 다 이름이 문제다. 이름이 멋이 없으니 아무리 좋아도 쉽게 사람들의 관심을 얻지 못한다.)

**SQLAlchemy**의 철학은 대략 이렇다. RDBMS와 객체는 서로 다른 디자인 원칙을 따른다. 원칙이 다른 두 개념을 연결시키는 것이 ORM이다. 그런데 대부분의 ORM은 RDBMS의 원칙을 무시하고 RDBMS의 일부 자주 사용하는 기능만을 노출한 채 나머지는 거세하는 경향이 강하다. 이를테면 Rails의 ActiveRecord 같은 것들의 RDBMS에 대한 생각은 “똑똑한 스토리지일뿐”이다. 이는 대부분의 ORM 제작자들이 RDBMS에 대해 알지 못할뿐더러 관심조차 없기 때문에 일어나는 일이다. SQLAlchemy는 그 둘의 불일치를 이해하고, 양쪽 모두의 원칙을 지켜야 한다는 철학이다. SQLAlchemy의 맵핑 방식이 일견 다른 ORM 프레임워크에 비해 복잡해보이는 것은 사실이다. 하지만 그것은 철학을 위해 의도적으로 디자인된 부분이다. 서로 다른 컨셉을 연결애햐 하니 온갖 종류의 연결 방식을 다 제공한다. ActiveRecord마냥 모든 릴레이션이 `id`라는 이름의 프라이머리 키(primary key)를 갖는다는 가정따위는 전혀 없다. 기본적으로 나는 그런 철학에 깊게 동의했고, 거기다가 이미 성숙할대로 성숙해서 내가 스스로 구현하자면 끝도 없는 기능들을 이미 다 제공하고 있어서 거기에 압도되어 버렸다.

 - 아이덴티티 맵(identity map)[^1]
 - Python 표현식을 SQL로 변환하는 컴파일러 셋[^2]
   - 타입 시스템[^3]
     - 사용자 정의 타입 만들기
 - 여러 필드로 프라이머리 키 만들기
 - 제약 조건(constraint) 정의
 - 특정 표현식을 프로퍼티(property)로 사용하기[^4]
 - 셀프 조인
 - RDBMS에서 여러 필드로 관리되는 것을 객체에서는 하나의 애트리뷰트로 연결하기[^5]
 - 다양한 방식의 상속 지원
   - 특정 컬럼의 데이터를 가지고 다형성(polymorphic)을 구현하는 [단일 테이블 상속][1](single table inheritance)
   - [조인으로 구현하는 테이블 상속][2](joined table inheritance)
   - 각각 나눠진 테이블을 마치 하나의 클래스 계통(class hierarchy)인 것처럼 보이게 해서 맵핑하는 [컨크리트 테이블 상속][3](concrete table inheritance)
 - 둘 이상의 테이블을 하나의 클래스로 연결하기 (RDBMS의 뷰와 비슷하지만 DML이 가능하다는 점이 다르다.)
 - 관계 매핑을 딕셔너리(`dict`) 등으로 하기[^6]
 - 다양한 RDBMS 벤더 지원 [^7]

사실 위에서 적은 것만도 일부일 뿐이고 정말 방대한 기능들을 제공하고 있어서 메뉴얼을 차근차근 읽어보면 압도될 수밖에 없게 만드는 ORM 프레임워크다. 왜 이렇게 쓸데없이 많은 기능들을 제공하는지 모르겠다고 하면 SQLAlchemy의 철학에 수긍하지 못해서 그럴 것이다. 저렇게 많은 맵핑 방법을 제공하기 때문에 **RDBMS를 RDBMS답게 쓰면서 객체를 객체답게 디자인할 수 있게 된다.**

참고로 난 ORM 프레임워크에 특별히 관심이 많고, 기준도 제법 높은 편이라 Ruby의 DataMapper 같은 제법 똑똑하다는 ORM 프레임워크를 보고도 “병신이네”하고 말았던(오만하기 짝이 없지만;) 정도인데 SQLAlchemy는 정말 날 매료시켰다. 다만 기능이 너무 많아 제대로 쓰려면 꽤 오랫동안 배워야 하는게 문제. 나도 제대로 잘 쓰는데 1년 정도 걸린 것 같다.

**Werkzeug**은 비교적 최근에 발견했는데 기존에 잔뜩 쏟아지고 있는 Rails, Django 류의 풀스택 프레임워크와도 전혀 다르고, 그렇다고 해서 [djng][]이나 [Sinatra][], [Flask][][^8] 같은 최근 유행하는 마이크로프레임워크와도 다른 물건이다.

일단 Werkzeug은 프레임워크가 아니라 라이브러리다. 프레임워크는 기본적으로 앞으로 작성될 코드가 그 프레임워크에 맞춰지도록 강요한다. Django에서 Django ORM만 갖다 쓴다거나 Rails에서 `app/{models,controllers,views}` 디렉토리 구조를 거부할 수는 없으며 할 수 있다고 해도 그 프레임워크를 쓰는 의미가 사라진다.

Werkzeug은 MVC를 강요하지도 않으며 ORM으로 어떤 걸 쓸지도 정해놓지 않았고, 디렉토리 구조도 전혀 제시하지 않는다. 그럼 Werkzeug은 어디에 쓰냐 하면, 내 생각에는 인하우스 프레임워크를 만들기 위한 도구들이라고 생각한다. 앞서 얘기한 것만 보면 기능이 별로 없고 가벼울 것 같지만, 실제로 Werkzeug은 HTTP와 WSGI 프로토콜 안에서 생각할 수 있는 모든 기능을 다 제공한다. 이를테면 내용 협상(content negotiation)부터 세션, 시큐어 쿠키, 정적 파일들을 서빙해주는 WSGI 미들웨어, 디버깅을 위한 미들웨어, 프로파일러, 가상 호스트, URL 라우팅, 캐시, 날짜 및 시간 관련 유틸리티, HTML 헬퍼……. 그런데도 프레임워크는 아니다. 필요한 만큼만 `import`해서 쓰게 되어있기 때문이다. 열거한 기능들 중에 이를테면 시큐어 쿠키 기능 딱 하나만 쓰려고 `import werkzeug.contrib.securecookie`해서 써도 전혀 이상하지 않게 되어있다.

저런 디자인이 가능한 것은 Python에 WSGI가 있기 때문이다. Werkzeug의 primitive는 WSGI이고, WSGI 인터페이스 이상의 추상화가 없기도 하다. 딱 WSGI의 인터페이스만으로 모든 것을 해결한 라이브러리다. 프레임워크를 만들 수 있게 해주는 프레임워크, 즉 메타프레임워크쯤 된달까.

게다가 클래스, 함수 하나하나의 디자인이 모두 센스 넘치게 잘 되어있다. 현대적인 Python 프로그램 디자인의 모범이라 할만하다. 철학부터 제공되는 기능들 모두가 날 만족시킨다. 최근 몇년동안 이렇게 날 만족시킨 웹 개발 관련 라이브러리도 처음이다.

요즘 SQLAlchemy + Werkzeug + [Jinja2][]으로 웹 개발을 하고 있는데, 최근 몇년간 했던 웹 개발 중에서 가장 행복하다. 정말로.

 [^1]: 같은 레코드에 대한 객체는 레퍼런스도 같도록 매핑하는 것. 그러니까 하나의 레코드에 대해서는 하나의 객체만 존재하게 해준다.

 [^2]: 사실 SQLAlchemy에서 가장 핵심적인 모듈이면서 가장 강력한 모듈이다. 이게 있기 때문에 SQLAlchemy의 다른 방대한 기능이 존재할 수 있다. SQL 컴파일러가 존재하니 그 윗단에서는 SQL 해킹을 할 필요 없이 추상화 레이어를 쌓아올리면 되기 때문이다.

 [^3]: 컴파일러 셋을 만들어야 하니 당연히 의미에 맞는 번역을 하기 위해서는 타입 시스템이 필요해진다.

 [^4]: 예를 들어 `deleted_at`이라는 컬럼이 있고 그 컬럼은 해당 레코드가 삭제되지 않았다면 `NULL`이고, 삭제되었다면 삭제된 시각이 채워진다. 이런 경우 `deleted`라는 또다른 불리언(boolean) 컬럼을 객체에서 가상으로 만들 수 있다.

        deleted = sqlalchemy.orm.column_property(deleted_at != None)

    위와 같이 `deleted`를 지정하면 사용할때 `record.deleted`와 같이 쓸 수 있을 뿐만 아니라, 쿼리할 때도 크라이테리아를 지정하기 위해 `Record.deleted`처럼 사용 가능하다. 그렇게 하면 SQL으로는 `WHERE deleted_at IS NOT NULL`과 같이 컴파일되는데 이 얼마나 똑똑한 작동인가.

 [^5]: 지저분한 예지만 이를테면 RDBMS에서는 전화번호를 `tel1`, `tel2`, `te3`로 저장하고 있는데 그걸 객체에서는 `telephone`이라는 하나의 프로퍼티로 관리하고 그 타입은 [`collections.namedtuple`][collections.namedtuple]을 이용해 `Telephone(tel1, tel2, tel3)` 같은 식으로 맵핑할 수 있다.

 [^6]: 만약 `person(id pk, name)` 따위의 테이블이 있고 또 `post(id pk, category pk, author_id fk, body)` 따위의 테이블이 있다면 `person.posts[category]`처럼 맵핑하는 것을 말한다. 꼭 `dict`가 아니라도 아무 컬렉션 타입으로든 맵핑이 가능하다.

 [^7]: 대부분의 ORM 프레임워크들은 자신이 지원하는 RDBMS 벤더의 기능 집합들 사이에 교집합만을 지원하고, 나머지 특정 벤더에서만 존재하는 기능들(vendor-specific features)은 지원하지 않고 거세하는 경향이 강하지만, SQLAlchemy는 전혀 그렇지 않고 각 벤더 고유의 기능들을 그대로 살린다. 이를테면 PostgreSQL의 배열 타입(array type) 같은 것을 그대로 사용 가능하다.

 [^8]: 사실 이것도 Werkzeug 기반이다.

  [sqlalchemy]: http://www.sqlalchemy.org/
  [werkzeug]: http://werkzeug.pocoo.org/
  [collections.namedtuple]: http://docs.python.org/dev/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields
  [djng]: http://github.com/simonw/djng
  [sinatra]: http://www.sinatrarb.com/
  [flask]: http://flask.pocoo.org/
  [jinja2]: http://jinja.pocoo.org/2/
  [1]: http://www.sqlalchemy.org/docs/mappers.html#single-table-inheritance
  [2]: http://www.sqlalchemy.org/docs/mappers.html#joined-table-inheritance
  [3]: http://www.sqlalchemy.org/docs/mappers.html#concrete-table-inheritance
