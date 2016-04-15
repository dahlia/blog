(github|bitbucket)-distutils
============================

StyleShare 만들 때 배포를 신속하게 만들고 싶었지만 실제로는 그렇게 빠르게 되지 않았다. 패키징을 하는데 시간이 가장 많이 들었던 부분은 바로 의존성 해결. 정확히는 PyPI가 그렇게 빠릿하게 응답하지 않아서 모든 패키지를 다운로드하는데 몇분씩 걸리다보니 당장 몇초 안에 배포를 하고 싶은 상황에서 매우 답답했던 기억이 난다. 애초에 `pip`나 `easy_install`이 [전체 의존성 그래프를 선형화시켜서 하나씩 받는 게][1] 문제라고 보지만, 어쨌든 그랬었다. (해결은 `pip`에서 제공하는 캐시 옵션을 여러가지 켜서 어느 정도 했지만 여전히 인덱스 속도가 느려서 그 이상으로 시간을 줄이지는 못했다.)

저걸 해결하기 위해서는 아니지만, 그 이후에 패키지 메타데이터를 PyPI에 올리더라도 패키지 파일 자체는 CDN이 물려있는 곳에서 호스팅하는 게 낫겠다는 생각을 계속 해오고 있었는데, 마침 Bitbucket이나 GitHub은 저장소 별로 다운로드 서비스를 제공하고 있고 둘 다 Amazon CloudFront (AWS의 저가형 CDN) 서비스의 가호를 받고 있어서 속도가 서울에서도 꽤나 괜찮게 나왔다. 그래서 패키지 릴리즈할 때 아예 그쪽에 올리게 하는 걸 만들어보자, 하는 아이디어로 최근 두 개의 패키지를 만들어서 올렸다.

 - [github-distutils](https://github.com/dahlia/github-distutils)
 - [bitbucket-distutils](https://bitbucket.org/dahlia/bitbucket-distutils)

참고로 둘 다 PyPI 패키지 명이고, 자기가 배포하려는 패키지의 setup.py 파일 안에 다음과 같이 `setup_requires`를 명시하면 쓸 수 있다.

    setup(
        name='YourPackageName',
        version='1.2.3',
        ...,
        setup_requires=['github-distutils >= 0.1.0']
    )

실제로 이걸 써서 릴리즈하면 PyPI 페이지에는 [이렇게][2] 올라가고:

![PyPI TypeQuery page](https://i.imgur.com/iRH6y.png)

저장소 다운로드 페이지에도 [이렇게][3] 올라간다:

![Bitbucket TypeQuery downloads](https://i.imgur.com/HrIdS.png)

[1]: http://www.reddit.com/r/Python/comments/tenmz/how_can_pip_be_improved/c4lzu16
[2]: http://pypi.python.org/pypi/TypeQuery
[3]: https://bitbucket.org/dahlia/typequery/downloads
