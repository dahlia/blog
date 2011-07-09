Python Compatibility Table
==========================

 <ins datetime="2012-10-01T07:18:41+09:00">이 글은 2011년 7월 10일에 작성된 글이다. 2012년 10월 1일 현재 [PyPy][]의 최신 버전은 1.9이며 매우 추천해줄만한 구현이 되었다.</ins>

(tl;dr: [CPython 2.7.2][]나 [PyPy][] 1.5 쓰세요.)

| Ver \ Impl | [CPython][]       | [PyPy][] | [Jython][]       | [IronPython][]       | [Stackless Python][]   |
| ---------- | ----------------- | -------- | ---------------- | -------------------- | ---------------------- |
| [2.5][]    | [CPython 2.5.6][] | PyPy 1.4 | [Jython 2.5.2][] | [IronPython 2.0.3][] | Stackless Python 2.5.5 |
| [2.6][]    | [CPython 2.6.7][] |          |                  | [IronPython 2.6.1][] | Stackless Python 2.6.5 |
| 2.7        | [CPython 2.7.2][] | PyPy 1.5 |                  |                      | Stackless Python 2.7.1 |
| 3.0        | [CPython 3.0.1][] |          |                  |                      | Stackless Python 3.0.1 |
| 3.1        | [CPython 3.1.4][] |          |                  |                      | Stackless Python 3.1.3 |
| 3.2        | [CPython 3.2][]   |          |                  |                      | Stackless Python 3.2   |

고등학교 후배가 내 Facebook 담벼락에 [Python의 버전 및 구현별 차이점에 대해 물어봐서][1] 글로 써본다.

Python의 호환성 및 기능의 차이는 크게 언어 표준의 버전과 언어 구현, 두 축에 따라 크게 달라진다. Python은 커뮤니티에 의해 디자인을 발전시켜 나가는 언어로, [PEP][]이라는 형식의 제안서들과 그것을 투표 등의 방법을 통해 해당 제안을 다음 버전에 적용할지 결정한다. 결정된 디자인에 따라, CPython이라는 Python의 전통적인 레퍼런스 구현에 제안된 것들을 실제로 구현하여 릴리즈한다.

언어는 버전이 올라감에 따라 크게 문법이 추가되거나 표준 라이브러리에 새로운 모듈이 추가된다. (혹은 기존 모듈에 새로운 함수나 메서드 따위가 추가되기도 하고, 표준 라이브러리의 행동이 약간 달라지는 경우도 있다.) 버전은 X.Y.Z 형식을 따르는데, Y는 다른 버전의 언어 스펙을 구현했음을 표시한다. 예를 들어 2.6에는 없는 집합 조건제시법(set comprehension) 문법이 2.7에는 있다. 하지만 Y가 올라가도 기존 언어의 시멘틱은 거의 깨뜨리지 않는다. 즉, 기존 언어에 문법이 더해지기는 하나, 기존 문법의 시멘틱이 바뀌지는 않는다. 다시 말해, 2.5에서 정상적으로 동작하던 코드는 2.6에서도 대부분 제대로 돌아간다고 볼 수 있다. (Y - 1) 버전은 사실상 Y 버전의 부분집합이다.

Z 버전은 언어의 시멘틱이 전혀 추가되거나 변경되지 않으며 (즉, 당연히 문법이 추가되거나 표준 라이브러리에 새로운 API가 생기지 않으며), 다만 표준에 따르면 응당 그렇게 구현됐어야 했으나 그렇지 못했던 버그들을 수정하기만 한다.

가장 중요한 부분은 X 버전인데, 그러니까, Python 2와 Python 3의 차이인데, **이 두 언어는 완전히 다른 언어라고 생각하면 된다.** 애초에 하위호환성을 포기한다는 전제 하에 언어 디자인을 많은 부분 갈아엎었기 때문이다. (Ruby 사용자라면 1.8과 1.9 정도, 혹은 그보다 약간 더 큰 차이가 있다고 생각하면 된다. Perl 사용자라면 5.0과 5.14 정도의 차이가 있다고 생각하면 된다. 5와 6 정도의 차이까지는 아니다.) 예를 들어 Python 2에서는 일반 문자열 리터럴의 타입은 `str`이고, 이건 바이트열을 뜻한다(즉 C의 `char[]`과 같다). 그리고 앞에 `u` 접두사가 붙은 문자열 리터럴의 타입은 `unicode`고, 이건 Unicode 문자열이다(UTF-8 바이트열 같은 게 아니다). Python 3에서도 일반 문자열의 타입이 `str`인 것은 같지만, 이건 사실상 Python 2의 `unicode`이다. Python 2에서 `str`과 같은, 즉, Unicode 문자열이 아닌 바이트열을 원한다면 `bytes`라는 타입을 써야 하고 문자열 리터럴 앞에 `b` 접두사를 붙여야 한다.

| Version | Byte String Type | Unicode String Type |
| ------- | ---------------- | ------------------- |
| 2       | `str`            | `unicode`           |
| 3       | `bytes`          | `str`               |

게다가 Python 2에는 `int`와 `long`이 자연스럽게 변환되긴 하지만 여전히 별도의 자료형으로 처리되는데 반해, Python 3는 `int` 하나로 일반화했다. Python 2에서는 올드 스타일 클래스(old-style class)와 뉴 스타일 클래스(new-style class)가 공존하고 `object`를 명시적으로 상속받으면 뉴 스타일 클래스를 쓸 수 있게 해놨지만, Python 3는 올드 스타일 클래스가 사라지고  명시적으로 `object`를 상속받지 않아도 항상 뉴 스타일 클래스로 정의된다. 메타클래스(metaclass) 사용 문법도 달라졌다. 이것저것 따지자면 바뀐 게 너무 많고 기존 Python 2에서 돌아가던 코드는 십중팔구 Python 3에서는 문법 에러부터 나며, 운 좋게 문법 에러를 만나지 않더라도 제대로 동작하지 않는다. 

Python 2와 Python 3 사이에서 결정하는 것은 아직까지 큰 딜레마가 있다. 아직 대부분의 써드파티 모듈들은 Python 3에서 동작하지 않지만, Python 2는 더이상 업데이트가 없다고 결정되었기 때문이다. 먼 미래를 고려한다면 Python 3를 선택해야 하지만 그러면 당장 쓸 수 있는 라이브러리가 매우 제한된다.

CPython을 제외한 PyPy, IronPython, Jython 등은 모두 Python의 또다른 구현으로, 이상적으로는 Python 언어 표준을 그대로 구현해야 한다. 하지만 리얼 월드는 만만치 않아서, 대부분의 CPython 기준으로 작성된 코드를 다른 구현에서 수정 없이 돌렸을 때 제대로 동작하는 경우는 생각보다 낮다. 호환성이 깨지는 부분은 각 구현에 따라 달라지지만 대개는 C 확장 모듈이 가장 큰 원인이다.

참고로 Stackless Python은 처음부터 새로(from scratch) 만든 구현이 아니고, CPython의 포크이며, CPython의 새로운 버전이 나올 때마다 매번 패치를 적용해서 같은 버전의 Stackless Python을 배포하는 식이다. 둘 사이의 가장 큰 차이는 CPython은 C 스택을 사용하지만 Stackless Python은 C 스택을 사용하지 않고 스택을 직접 구현했다는 점(그래서 웬만하면 호출 스택이 넘치지는 않는다), 코루틴(coroutine)과 마이크로쓰레드(microthreads)를 구현했다는 점 정도이다. C API는 거의 유지되기 때문에 CPython에서 돌아가는 C 확장 모듈은 대부분 Stackless Python에서도 다시 컴파일하면 그대로 돌아간다. (사실 난 돌아가지 않는 C 확장 모듈을 아직 못봤다.)

IronPython 같은 경우 이름에서 유추할 수 있다시피 .NET이나 Mono와 같은 CLR 위에서 돌아가는 C#으로 구현된 Python이다. CPython과 가장 큰 차이점이라면, Python 2만 구현하고 있는데도 문자열 시멘틱은 Python 3에 가깝다는 점이다. IronPython의 `str`은 `unicode`를 가리키게 되어있다. 바이트열을 쓰려면 꽤나 큰 고통을 수반하고 당연히 `str`이 바이트열이라는 언어 스펙에 의존하는 많은 코드들이 IronPython에서 깨진다. IronPython 개발팀은 Python 2.7 호환성을 높이는 대신 바로 Python 3 구현에 집중하려는 모양이다. 하지만 아직 나오지 않았다,

Jython 역시 이름에서 유추할 수 있다시피 JVM 위에서 돌아가는 Java로 구현된 Python이다. 난 많이 써보지 않아서 잘 모르겠다. (아직 Python 2.5만 구현하고 있어서 쓸 일이 없었다.)

[PyPy는 내가 이전에 쓴 글을 참고하면 된다.][2] 결론만 얘기하자면, Python 2.7 버전까지 구현하고 있는데다, CPython과 호환성도 매우 높다. “CPython에서 돌아가는 코드가 PyPy에서 돌아가지 않으면 이유 막론하고 PyPy의 버그다”라는 게 PyPy 개발팀의 원칙이기 때문이다. **그리고 현존하는 모든 Python 구현 중에 가장 성능이 좋을 뿐만 아니라 압도적이다.** 최근 나는 CPython보다 PyPy를 더 많이 쓴다.

여기까지는 주로 사실을 썼고, 후배가 물어본 것에 답을 하자면 몇가지 케이스로 나누어서 추천해야겠다.

일단, Java나 CLR로 된 애플리케이션이 있고 그 안에서 플러그인 따위를 Python 언어로 스크립팅할 수 있게 하려면 Jython이나 IronPython이 답이다. 하지만 반대로 이야기하면 저런 경우가 아니라면 IronPython이나 Jython은 피하라는 뜻도 된다. 성능 때문에 저 두 구현을 선택하진 말길 바란다.

성능에 민감한 경우, 그리고 애플리케이션이 I/O 성능이 아닌 CPU 성능에 의존적인 경우 (한마디로 데이터베이스나 소켓 통신 따위가 아니라 계산을 주로 한다면), PyPy가 답이다. PyPy는 일반적인 웹 개발을 하는 경우에도 추천할만하다. 웹 개발에 필요한 대부분의 써드파티 라이브러리나 프레임워크는 PyPy에서 잘 돌아간다.

Stackless Python은 말 그대로 코루틴(coroutine)과 마이크로쓰레드(microthreads)가 필요하면 쓰면 된다. 하지만 CPython에서 [`gevent`][gevent]나 [Twisted][]를 쓰는 대안도 존재한다.

아무것도 모르겠고 생각하기도 싫다면 CPython을 쓰면 된다. 사실 거의 모든 경우에는 대안 구현을 피하고 CPython 쓰는게 답이다.

버전을 이야기해보자. [PyPI][]에 올릴 배포용 모듈을 만든다면 Python 2.5를 지원하는게 좋다. 적어도 Python 2.6은 지원해야 한다. 그리고 요즘에는 PyPy 같은 다른 구현에서도 테스트해보는 경향이 있다.

상용 애플리케이션을 만든다면 굳이 버전에 얽매일 필요가 없다. Python 2.7이나 Python 3.2를 쓰면 된다.

다만 앞서 이야기했다시피 Python 2와 Python 3 사이에서 결정하는 것은 꽤 중요하다. 한번 정하면 거의 돌아갈 수 없는 강을 건넜다고 보면 된다. 자신이 사용해야할 라이브러리들의 목록을 정리해보고, 필요한 것들이 모두 Python 3를 지원한다면 Python 3를 써도 된다. 하지만 그렇지 않다면 그냥 Python 2.7을 선택하라고 권하고 싶다. 특히 웹 개발을 한다면 아직 Python 3를 쓰기는 힘들다. Python 3에서의 웹 개발의 어려움에 대해서는 작년에 Armin Ronacher가 쓴 [WSGI on Python 3][3]라는 글을 참고.

[2.5]: http://docs.python.org/release/2.5/whatsnew/whatsnew25.html
[2.6]: http://docs.python.org/release/2.6/whatsnew/2.6.html
[CPython]: http://python.org/
[PyPy]: http://pypy.org/
[Jython]: http://jython.org/
[IronPython]: http://ironpython.net/
[Stackless Python]: http://www.stackless.com/
[CPython 2.5.6]: http://python.org/download/releases/2.5.6
[CPython 2.6.7]: http://python.org/download/releases/2.6.7
[CPython 2.7.2]: http://python.org/download/releases/2.7.2/
[CPython 3.0.1]: http://python.org/download/releases/3.0.1
[CPython 3.1.4]: http://python.org/download/releases/3.1.4
[CPython 3.2]: http://python.org/download/releases/3.2
[Jython 2.5.2]: http://sourceforge.net/projects/jython/files/jython/2.5.2/jython_installer-2.5.2.jar/download
[IronPython 2.0.3]: http://ironpython.codeplex.com/releases/view/30416
[IronPython 2.6.1]: http://ironpython.codeplex.com/releases/view/36280
[PEP]: http://www.python.org/dev/peps/
[gevent]: http://www.gevent.org/
[Twisted]: http://twistedmatrix.com/
[PyPI]: http://pypi.python.org/
[1]: https://www.facebook.com/hongminhee/posts/2252486511494
[2]: http://blog.dahlia.kr/post/5124874464
[3]: http://lucumr.pocoo.org/2010/5/25/wsgi-on-python-3/

*[PEP]: Python Enhancement Proposal
