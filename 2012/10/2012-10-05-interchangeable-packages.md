Interchangeable packages
========================

(배경 설명이 길어서 본론이 좀 밑에서부터 시작합니다.)

이미 있는 유명한 라이브러리의 인터페이스만 맞추고서 내부 구현은 다른 (보통 성능 향상 등을 위해 새로 작성한) 라이브러리들이 있다. 예를 들어 libjpeg의 인터페이스를 맞추고 성능을 끌어올린 libjpeg-turbo 같은 것이 그런 것인데, 이럴 때 보통 “libjpeg-turbo는 libjpeg의 drop-in replacement다”라는 표현을 쓴다. 한국어로는 해당하는 단어가 뭐가 있을지 잘 모르겠다.

Python에서도 비슷한 것들이 있는데, 예를 들어 JSON 구현체들이 그렇다. Python 2.6에 추가된 표준 라이브러리에 `json` 모듈이 있는데 이 모듈은 매우 간단한 인터페이스로 구성되어 있다. `load()`, `loads()`, `dump()`, `dumps()` 이렇게 4개의 함수를 제공하는 모듈이다.

그런데 이 표준 `json` 모듈과 같은 인터페이스로 성능에 촛점을 맞춰 서로 경쟁적으로 구현된 서드파티 라이브러리들이 꽤 된다. 가장 유명한 것으로는 `simplejson`이 있고, 또 `ujson`이라는 것도 있다. 지금은 Python 2.7 런타임을 제공하지만 Google App Engine이 작년까지도 Python 2.5 런타임만 제공하여 표준 라이브러리의 `json`을 쓸 수 없었을 때, SDK에 내장된 `django.utils.simplejson` 모듈을 사용해야 했다. 현재 가장 최근 버전의 Jython인 Jython 2.5 역시 표준 라이브러리에 `json`이 없으므로 서드파티 라이브러리인 Jyson에 들어있는 `com.xhaus.jyson.JysonCodec`를 써야 한다.

종합해서, 사용할 수 있는 가장 좋은 성능의 JSON 모듈을 쓰면서도, 가장 이식성이 높은 코드를 쓰기 위해 다음과 같은 긴 `try`–`except`–`import` 패턴을 써야 한다.

    try:
        import ujson as json
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            try:
                from django.utils import simplejson as json
            except ImportError:
                try:
                    from com.xhaus.jyson import JysonCodec as json
                except ImportError:
                    import json

만약 Python에서 위와 같은 패턴을 지원하는 문법을 별도로 지원하고자 한다면 다음과 같은 것이 필요할 것이다.

    import (ujson or simplejson or django.utils.simplejson or
            com.xhaus.jyson.JysonCodec or json) as json

한편, 저런 식으로 인터페이스가 호환되는 서로 다른 구현체가 존재하는 모듈들이 JSON만 있는 것은 아니다. 예를 들어 `ElementTree`라는 XML 파서 인터페이스와 호환되는 것만 표준의 `xml.etree.ElementTree`, `xml.etree.cElementTree`, 서드파티 libxml2 바인딩인 `lxml.etree` 등이 있다.

여기서부터가 본론이다.

그런데 객체의 중립적인 인터페이스는 형식(할 수 있는 것)에 대해서는 합의하는 반면 시멘틱(해야할 것)에 대해서는 불가지론적(agnostic)인데, 반면 모듈의 중립적인 인터페이스는 시멘틱에 대해서도 합의한다는 차이점이 있다.[^1] 그래서 오래전부터 생각한 아이디어가 두 개 있다. 이 두 아이디어는 하나의 시스템으로 통합될 수도 있다.

첫번째 아이디어는 이렇다. 현재의 모듈 인터페이스는 C++의 템플릿 시그너쳐나 덕 타입 언어의 객체 인터페이스처럼 암시적으로 “생겨나는” 것이다. 이와 같은 종류의 합의는 합의가 변해야 할 시점이 오면 큰 문제가 생기게 된다. 즉, 실제 구현체가 어떤 인터페이스에 의도적으로 합의했는지 알 수 없으므로 어떤 종류의 전후처리도 불가능하거나 힘들게 한다. 그래서 C++0x 얘기가 오갈 때 Haskell의 타입클래스를 배낀 [컨셉][1](concepts)을 도입하자는 주장이 있었던 것이다. 하지만 모듈 인터페이스에 있어서 더 중요한 것은, **선언 없이는 구현체가 인터페이스에 합의하는지는 알 수 있지만 인터페이스에 합의하는 모든 구현체를 찾는 일은 할 수 없다는 점이다.**

따라서 **중립적인 모듈 인터페이스 역시 선언적(declarative)이어야 한다.** 즉, 인터페이스의 선언이 존재하고, 구현체가 그 인터페이스에 합의한다는 선언도 존재해야 한다. 그렇게 되면 언어의 패키지 시스템은 모듈을 구현체 이름으로 임포트할 수 있을 뿐만 아니라, 선언된 중립적인 모듈 인터페이스로도 임포트할 수 있을 것이다. 예를 들어,

    from xml.etree import cElementTree as etree

라고 하거나, (가상의 문법으로 예를 들자면)

    import (lxml.etree or xml.etree.cElementTree or xml.etree.ElementTree) as etree

라고 하는 대신 (선언된 모듈 인터페이스 이름이 `etree`라고 할 때) 다음과 같이 임포트할 수 있을 것이다.

    import etree

좀더 나아가자면, 모듈 인터페이스는 구현체의 다양한 관점의 효과성이나 효율성, 기능성 등에 대해서도 매개변수를 선언할 수 있고, 임포트 시에는 특정 매개변수를 기준으로 선호하는 구현체가 적절히 선택되도록 할 수 있을지도 모른다.

    import etree:
        less node_memory_use
        more maximum_child_depth
        if html_parseable
        unless c_used

두번째 아이디어는 첫번째 아이디어에 의존적이다. 중립적인 모듈 인터페이스가 선언적이고, 앞서 내가 제시한 가설과 같이 모듈 인터페이스에는 객체 인터페이스와 달리 모듈이 할 수 있는 일(형식) 뿐만 아니라 해야할 일(시멘틱)에 대해서도 합의한다면, **시멘틱을 검증할 수 있는 수단을 함께 선언할 수 있어야 할 것이다.** 그리고 내 생각에 **시멘틱은 자동화된 테스트로 검증할 수 있다.**

즉, 중립적인 모듈 인터페이스는 특정 대상 구현체를 상정하지 않은 테스트를 포함할 수 있을 것이다. 앞서 예로 든 JSON 모듈의 경우를 생각해보자. 각자 다른 구현체이지만, 인터페이스도 같고 하는 일도 같다. 즉, 시멘틱을 공유한다. 같은 JSON을 파싱하면 각 구현체는 어쨌든 같은 Python 객체를 반환해야 한다.[^2] 같은 Python 객체를 직렬화하면 같은 JSON이 나와야 한다. **즉, 테스트 케이스는 공유할 수 있다.**

Markdown 구현체를 생각해보자. [Markdown은 표준적인 테스트 스위트가 있다.][2] 이게 모듈 인터페이스의 테스트가 될 수 있다. Markdown 인터페이스를 구현하는 모듈은 자체적인 테스트를 포함할 수 있지만, 중립적인 모듈 인터페이스의 표준 테스트도 함께 통과해야 한다.

이런 예는 너무 많기 때문에 쉽게 열거할 수 있다. WSGI 서버, XML 파서, 마크업 언어 번역기, diff, 이미지 처리 등…

요약하자면 이렇게 된다. 모듈에는 인터페이스와 구현체가 있을 수 있다. 인터페이스는 선언과 테스트가 들어간다. 구현체에는 테스트를 통과하는 구현체가 들어간다. 패키지 시스템은 모듈을 인터페이스 혹은 특정 구현체 이름으로 임포트할 수 있다. 인터페이스는 매개변수를 포함할 수도 있으며, 구현체는 매개변수에 적절한 값을 제공하고, 임포트 시에 매개변수를 이용해 세밀한 조건을 제시할 수 있다.

내가 언어를 만들게 되면 패키지 시스템을 이렇게 만들 생각이다.

[1]: http://en.wikipedia.org/wiki/Concepts_%28C%2B%2B%29
[2]: http://six.pairlist.net/pipermail/markdown-discuss/2004-December/000909.html

[^1]: 그렇지 않은 모듈 인터페이스도 있다. 가령 위에서 소개한 `load()`, `loads()`, `dump()`, `dumps()` 네 개의 함수로 이루어진 JSON 모듈 인터페이스는 사실 JSON 모듈 인터페이스이기 전에 Python의 표준적인 직렬화 모듈 인터페이스다. `pickle`, `cPickle`, `marshal` 등 Python의 많은 직렬화 모듈들이 오래전부터 이 인터페이스로 합의해왔고, JSON도 직렬화 방식이기 때문에 원래부터 있던 인터페이스를 따른 것뿐이다. 하지만 저 직렬화 모듈들은 서로 다른 직렬화 포맷이고 기능도 상이하다. 물론 저 모듈들 사이에서도 `loads(dumps(value)) == value` 같은 최소한의 시멘틱은 존재할 수 있다.

[^2]: 코드로 얘기하자면 `json` 모듈이 실제 어떤 구현체를 지칭하든 간에, 구현체는 항상 `json.dumps(range(3)) == '[0, 1, 2]'`를 만족해야 한다.
