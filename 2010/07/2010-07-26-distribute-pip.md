distribute, pip
===============

 <ins datetime="2013-11-12T20:55:00+09:00">업데이트: 2013년에 드디어 [Distribute와 setuptools가 합쳐졌다.](http://pythonhosted.org/setuptools/merge.html) 따라서 이제 다시 setuptools라는 이름으로 통일되었고, Distribute는 그만 잊어버려도 된다.</ins>

최근에 [`setuptools`][setuptools] 대신 [`distribute`][distribute]를, [`easy_install`][easy_install] 대신 [`pip`][pip]를 쓰기 시작했다.

조금 설명하자면, `setuptools`는 Python 표준 라이브러리에 있는 `distutils`를 확장한 것인데, `distutils`는 Makefile 같은 빌드 스크립트의 Python 버전이다. Ruby의 `rake`나 Java의 Ant를 생각하면 된다. 표준 라이브러리에 있기 때문에 Python에서 프로젝트를 패키징하고 빌드 자동화를 하는 가장 기본적이고 표준적인 방법이라고 보면 된다. `setuptools`는 `distutils`의 확장 인터페이스를 이용해[^1] 의존성 해결(dependency resolution)도 해주게 만든 것이다. 보통은 setup.py 파일을 아래처럼 작성하므로 `setuptools`가 설치되어 있지 않아도 빌드는 가능하다.

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

`distribute`는 `setuptools`를 대체하기 위해 리팩토링한 버전이다. 사실 `setuptools`의 차세대 대안이라고들 말해서 쓰긴 하지만 나도 정확히 어떤 잇점이 있는지는 모른다. 다만 요즘 여러 패키지들이 `distribute`로 패키징을 하다보니까 가끔 `setuptools`에서 설치되지 않는 경우가 있어서 설치하게 되었다. `distribute`의 가장 큰 목표가 `setuptools`를 완전히 대체하는 것이기 때문에 저게 설치되면 `setuptools`를 완전히 갈아치워서 `import setuptools`를 해도 실제로는 `import distribute as setuptools`한 것처럼 작동한다. `setuptools`와의 호환성도 유지하지만 `distribute`에만 있는 기능을 쓴다면 제대로 `setuptools`만으로는 당연히 제대로 설치되지 않는다. 그리고 가끔 의존성에 아예 `distribute`를 넣어두는 패키지가 있어서, 그걸 설치하면서 쥐도 새도 모르게 설치되기 쉬운게 바로 `distribute`라고 할 수 있겠다.

`setuptools`나 `distribute`는 정확히 말해서 의존성의 전체 목록과 설치 순서를 계산해주며, 실제로 의존하는 패키지들을 [PyPI][]에서 다운로드하고 순서대로 설치하는 것은 `easy_install` 명령어가 구현한다. 다만 `easy_install` 명령어가 `setuptools` 패키지를 설치하면 생기기 때문에 보통 `setuptools`가 `easy_install`이라고 기억하는 사람도 적지 않다. `pip`는 `easy_install` 명령어의 차세대 대안이다. 이건 라이브러리가 아니라 프론트엔드이기 때문에 명령어의 하위호환성을 갖는 것은 아니며, 더 나은 인터페이스를 제공하기 위해 중간 명령어를 추가했다. 예를 들어 `easy_install SQLAlchemy`라고 쓰던 것을 `pip install SQLAlchemy`처럼 쓰게 한 것이다(그래도 글자수는 더 적다). 눈에 띄는 가장 큰 개선점으로 두 개가 있는데:

 - 설치했던 패키지를 `uninstall` 명령어로 쉽게 삭제할 수 있다.
 - 일단 의존하는 모든 패키지를 다운로드를 받고 나서 설치한다. 따라서 설치하다가 중간에 네트워크 문제로 중단되더라도 일부만 설치되는 일이 없다.

`pip`는 `distribute`가 나오기 전에 만들어진 것이고, `easy_install`만을 대체하기 위해 만들어졌으므로 `setuptools`와 `pip`를 함께 쓰는 경우도 많다. 물론 반대로 `distribute`를 설치해서 `easy_install` 명령을 여전히 사용하는 경우도 있다. 내가 바로 얼마 전까지`distribute`와 `easy_install`을 함께 사용하다가 최근부터 `pip`를 쓰기 시작했는데, 아무래도 `pip`는 프론트엔드이기 때문에 사용자로서 개선되었다는 느낌을 더 강하게 받는 것은 `distribute`보다는 `pip`인 것 같다.

 [^1]: 사실은 꼭 주어진 확장 인터페이스만 곧대로 쓰는 것은 아닌 모양이다.`distutils`가 원래 의도하지 않은 방향으로 핵(hack)도 조금 하는듯.

[setuptools]: http://peak.telecommunity.com/DevCenter/setuptools
[distribute]: http://packages.python.org/distribute/
[easy_install]: http://peak.telecommunity.com/DevCenter/EasyInstall
[pip]: http://pip-installer.org/
[pypi]: https://pypi.python.org/

*[PyPI]: Python Package Index
