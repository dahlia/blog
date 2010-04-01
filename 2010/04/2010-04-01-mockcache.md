[mockcache][source]
===================

요즘에 memcached 쓸 일이 많은데, 로컬에서 작업할 때 memcached 설치하기 참 귀찮다. 어차피 memcached는 실제 배포했을 때만 작동하면 된다. 그래서 [mockcache][]라는 것을 만들었다. 테스트 용도로 써도 되는데, 꼭 그런 용도는 아니고 memcached 클라이언트 라이브러리가 하나도 없을 때 이걸 쓰도록 fallback을 구성할 때도 좋다.

    try:
        import memcache
    except ImportError:
        import warnings
        import mockcache as memcache
        warnings.warn("imported mockcache instead of memcache; cannot find "
                      "memcache module")

    mc = memcache.Client(["127.0.0.1:11211"])

Python에서 쓸 수 있는 memcached 클라이언트 구현이 여럿 있는데, Python 특유의 낙관적인 인터페이스 문화 덕분에 별 표준이 있는 것도 아닌데도 다들 거의 동일한 인터페이스를 제공한다.[^1] 그것에 착안해서 만든 것이라 mockcache 역시 그 인터페이스를 따른다.

내부적으로는 그냥 `dict` 객체를 하나 생성해서 그걸로 상태를 관리하는 식이다. 그래도 expiration 같은 것도 구현은 했다.

PyPI에 올렸으니 `easy_install` 등으로 설치가 가능할 것이다. (관리자 권한으로 실행해야 한다.)

    $ easy_install mockcache

Bitbucket에 소스 코드를 올렸다. MIT 라이센스다. <http://bitbucket.org/lunant/mockcache/> Mercurial로 클론할 수 있다.

    $ hg clone http://bitbucket.org/lunant/mockcache/

버그 등의 이슈는 [Bitbucket에서 제공하는 이슈트래커][1]에 올려주시라.


  [^1]: 그래서 보통 `import` 문만 수정하면 어떻게든 비슷하게 쓸 수 있는 것이다. 모듈 단위의 폴리모피즘(polymorphism)이랄까.

  [mockcache]: http://pypi.python.org/pypi/mockcache
  [1]: http://bitbucket.org/lunant/mockcache/issues/new/

[source]: http://pypi.python.org/pypi/mockcache
