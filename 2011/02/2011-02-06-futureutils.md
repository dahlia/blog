[futureutils][source]
=====================

요즘 혼자서 만들고 있는 프로그램이 하나 있는데, 성능을 위해 병렬화를 해야하는 부분이 생겼다. 마침 병렬화할 수 있는 부분이 많았는데 죄다 제너레이터 함수(generator function)로 생성되는 반복자들이었다. 이걸 일반적으로 병렬화할 수 있을 거라는 생각이 들어 간단하게 퓨쳐(future)를 구현하게 되었는데, 나의 썩 좋지 못한 코딩 습관 중 하나가 하나 있어서… 바로 과하게 일반화한다는 것이다. 게다가 내 블로그를 계속 읽어온 사람은 알겠지만 나는 문서화를 강조하는 편이고, 당연히 내가 개발하는 것들을 문서화하는 습관이 있다. 그래서 이 간단한 퓨쳐 구현은 과하게 일반화된데다 문서화까지 되어서 급기야 “이것만 따로 패키지로 만들어서 올려도 되지 않을까”하는 생각을 하게 만들었다.

그래서 내친 김에 문서를 아예 좀더 보강하고 Python 2.5와 PyPy 1.4 호환성까지 곁들여서 패키징한 다음 [PyPI에 올렸다.][1] 이름은 **`futureutils`**라고 지었다. pip나 easy_install로 설치 가능하다.

    $ pip install futureutils  # 또는
    $ easy_install futureutils

사용법은 간단하다. 일반 함수 하나 — [`futureutils.promise()`][2] — 와 데코레이터 함수 — [`futureutils.future_generator()`][3] — 하나가 있는데, 전자는 좀더 일반적으로 사용 가능한 약간 저수준의 인터페이스고, 후자는 제너레이터 함수에 대해 데코레이터로 사용 가능한 조금 고수준의 인터페이스다. 병렬화할 반복자가 제너레이터 함수에 의해 만들어진다면, 제너레이터 함수에 `future_generator()`를 적용하기만 하면 된다.

    import lxml.html
    from futureutils import *

    @future_generator
    def list_hrefs(url):
        html = lxml.html.parse(url)
        for href in html.xpath('//a[@href]/@href'):
            href = href.strip()
            if href and not href.startswith('#'):
                yield href

어차피 이 데코레이터를 적용하든 그렇지 않든 제너레이터 함수의 작동은 동등하다. 함수의 의미는 바꾸지 않고 병렬화만 해서 효율을 늘리는 방식이기 때문이다.[^1]

좀더 일반적으로, 제너레이터 함수에 의한 반복자 뿐만 아니라, 모든 반복자에 대해서도 `promise()` 함수를 써서 병렬화가 가능하다. 위 예를 조금 고치면 다음과 같이 바꿀 수도 있다.

    import lxml.html
    from futureutils import *

    def list_hrefs(url):
        html = lxml.html.parse(url)
        for href in html.xpath('//a[@href]/@href'):
            href = href.strip()
            if href and not href.startswith('#'):
                yield href

    iterator = list_hrefs('http://dahlia.kr/')
    parallelized_iterator = promise(iterator)

보다시피 `promise()` 함수는 반복자 하나를 받아서 새로운 반복자 랩퍼(wrapper)를 반환하는데, 이 녀석이 원본 반복자를 안쪽에서 병렬화해서 돌리고 결과 자체는 일반 반복자와 같은 방식으로 전달해준다. 따라서 이것 역시 반복자의 의미에 변경을 가하지 않는다.

뭐, 함수 두 개밖에 없는 모듈이긴 하지만 자세한 것은 [API 레퍼런스 문서][4]를 참고하시면 되겠다.

소스 코드는 Bitbucket 저장소에서 Mercurial을 통해 받을 수 있다. <https://bitbucket.org/dahlia/futureutils>

    $ hg clone https://bitbucket.org/dahlia/futureutils

이 패키지는 MIT 라이센스로 배포된다.

덧. Reddit에도 올려봤다. <http://www.reddit.com/r/Python/comments/ffw7a/futureutils_introduces_futures_and_promises_into/> 괜찮다고 생각하시는 분들은 upvote해주시면 감사.

[^1]: 물론 제너레이터 함수 안쪽에서 뭔가 병렬화를 고려하고 무슨 짓을 하고 있다면 의미가 바뀔 수도 있으니 조심해야 한다. 이런 경우 그냥 쓰지 않는게 상책.

[1]: http://pypi.python.org/pypi/futureutils
[2]: http://dahlia.bitbucket.org/futureutils/#futureutils.promise
[3]: http://dahlia.bitbucket.org/futureutils/#futureutils.future_generator
[4]: http://dahlia.bitbucket.org/futureutils/#api

[source]: http://dahlia.bitbucket.org/futureutils/
