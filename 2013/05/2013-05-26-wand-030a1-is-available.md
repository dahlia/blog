[Wand 0.3.0a1 is available][source]
===================================

원래 여기 블로그에도 소식을 올리고 자려고 했지만, 너무 졸려서 까먹고 [메일링 리스트][1]와 [영어 블로그][2]에만 포스팅하고 자버렸다. 그래서 이 블로그는 조금 늦게 소식을 올린다.

작년 말까지 Wand 0.3을 출시하겠다고 약속하고도 올해에도 출시를 연기한 것이 여러번. 거듭된 연기 때문에 올해 초에는 예정에 없던 [0.2.3을 출시하기도][3] 했다. 정말 출시를 좀 해보려고 기존의 로드맵에서 Python 3 호환 같은 기능을 나중으로 미루기로 했다. [현재의 0.3 로드맵][4] 참고.

0.3에 들어가야 할 기능들로는 시퀀스, 드로잉, 전에 [이 블로그에서 언급했던 심 카빙(seam carving)][5] 등이 있는데, 구현하려던 기능들을 이제 모두 넣게 되어서 일단 알파 버전이라도 내놓게 되었다:

<http://dahlia.github.io/wand/dist/Wand-0.3.0a1.tar.gz>

이 버전은 어느 정도 API 호환이 깨질 위험이 있는 변화들을 포함하고 있다. (가령 기존에는 `Image` 클래스 하나만 있었지만 지금은 `BaseImage`가 있고 그걸 상속하는 `Image`와 `SingleImage`가 별도로 있다.) 따라서 사용하기 전에 [시퀀스에 대한 변경목록][6]과 [그 외 기능에 대한 변경 목록][7]을 확인하도록 하자.

PyPI에 올리면 기존에 의존성을 Wand 최신 버전으로 해놓고 있던 분들이 날벼락을 맞을 수 있기 때문에 올리지 않고, 대신 그냥 파일 형태로만 업로드했다. 하지만 기존 `pip`를 이용하거나 `distutils`/`setuptools`를 이용해서 의존성을 관리하던 곳에서도 바로 시도해볼 수 있다.

`pip`와 `requirements.txt` 목록을 이용하는 경우, 간단히 `Wand` (혹은 `Wand==0.2.3` 같은 줄) 부분을 위 타볼 URL로 치환하면 된다:

    http://dahlia.github.io/wand/dist/Wand-0.3.0a1.tar.gz#egg=Wand-0.3.0a1

`setup.py` 스크립트를 이용하는 경우, `install_requires` 목록에 `Wand==0.3.0a1`를 추가하고 `dependency_links`를 설정하면 된다:

    setup(
        install_requires=['Wand==0.3.0a1'],
        dependency_links=['http://dahlia.github.io/wand/dist/Wand-0.3.0a1.tar.gz']
    )

다들 한번 써봐주시고, 혹시라도 문제를 마주하면 [이슈 트래커][8]에 알려주셨으면 한다. (말로 하는 게 더 편하신 분들은 IRC[^1]나 Facebook 메신저, Twitter 메션/DM 등 편한 연락 방법도 환영.)

[^1]: [오징어 서버][9]에 있는 `#hongminhee` 채널. 대화명은 `hongminhee`.

[1]: http://librelist.com/browser/wand/2013/5/25/wand-0-3-0a1-is-available/
[2]: https://minhee.quora.com/Wand-0-3-0a1-is-available
[3]: http://librelist.com/browser//wand/2013/1/25/released-wand-0-2-3/
[4]: http://docs.wand-py.org/en/sequence/roadmap.html#version-0-3
[5]: https://blog.hongminhee.org/2012/10/22/seam-carving-using-wand/
[6]: http://docs.wand-py.org/en/sequence/changes.html#branch-sequence
[7]: http://docs.wand-py.org/en/sequence/changes.html#version-0-3-0
[8]: https://github.com/dahlia/wand/issues
[9]: http://ozinger.org/

[source]: https://minhee.quora.com/Wand-0-3-0a1-is-available
