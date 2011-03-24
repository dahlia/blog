[sqlalchemy.ext.hybrid][source]
===============================

곧 정식 버전이 출시될 SQLAlchemy 0.7에는 `sqlalchemy.ext.hybrid`라는 이름의 재밌는 (그리고 매우 똑똑해서 놀라운!) 기능이 들어간다. 링크된 문서를 보면 자세한 것을 볼 수 있는데, 대략 다음과 같은 것들이 가능하다: (링크한 문서에서 인용)

    from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
    from sqlalchemy.orm import mapper, Session, aliased

    class Interval(object):
        def __init__(self, start, end):
            self.start = start
            self.end = end

        @hybrid_property
        def length(self):
            return self.end - self.start

        @hybrid_method
        def contains(self, point):
            return (self.start <= point) & (point < self.end)

        @hybrid_method
        def intersects(self, other):
            return self.contains(other.start) | self.contains(other.end)

    mapper(Interval, interval_table)

위와 같이 OR 매핑된 클래스를 정의해놓는다. `hybrid_property`는 `property`와 기본적으로 비슷한 일을 한다.

    >>> i1 = Interval(5, 10)
    >>> i1.length
    5

더불어서, SQLAlchemy에서 쿼리를 할 때도 똑똑하게 SQL로 번역이 된다.

    >>> print Interval.length
    interval."end" - interval.start

    >>> print Session().query(Interval).filter(Interval.length > 10)
    SELECT interval.id AS interval_id, interval.start AS interval_start, 
    interval."end" AS interval_end 
    FROM interval 
    WHERE interval."end" - interval.start > :param_1

SQLAlchemy는 점점 다른 ORM이 따라올 수 없을 정도의 수준으로 똑똑해지고 있는 듯하다.

[source]: http://www.sqlalchemy.org/docs/07/orm/extensions/hybrid.html
