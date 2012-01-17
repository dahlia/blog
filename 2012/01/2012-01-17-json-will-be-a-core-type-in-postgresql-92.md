[JSON will be a core type in PostgreSQL 9.2][source]
====================================================

JSON이 PostgreSQL 9.2의 기본 타입으로 들어간다. 이미 이전부터 `xml`, [`hstore`][1] 등의 타입을 가지고 있었기 때문에 예상된 수순이었지만 그럼에도 놀라운 소식. 이게 들어가면… 긴 말 필요 없고 [HN에 누가 단 댓글][2]을 인용해보자.

> 이게 [표현식 색인][3]과 함께 쓰이면 JSON 데이터를 저장할 수 있을 뿐만 아니라 JSON 안쪽에 들어있는 값들을 색인할 수도 있게 된다. 즉, 달리 얘기하자면, PostgreSQL의 성숙한 구현을 희생하지 않고 NoSQL 데이터 모델의 장점중 하나를 누릴 수 있게 된다.

[1]: http://www.postgresql.org/docs/9.1/static/hstore.html
[2]: http://news.ycombinator.com/item?id=3472460
[3]: http://www.postgresql.org/docs/9.1/interactive/indexes-expressional.html

[source]: http://people.planetpostgresql.org/andrew/index.php?/archives/244-Under-the-wire.html
