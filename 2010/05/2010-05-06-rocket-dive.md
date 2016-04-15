[ROCKET DIVE][0]
================

![ROCKET DIVE 창](https://media.tumblr.com/tumblr_l1z9p9ZVzI1qz6t91.png)

Python으로 웹 개발을 하려면 개발용 WSGI[^1] 컨테이너가 필요하다. 하지만 Python을 잘 모르는 사람이 개발 환경을 꾸리기는 쉽지 않다. 이를테면 디자이너는 .html 템플릿 파일을 수정해야 하는데, 그걸 위해서 [Green Unicorn][gunicorn]이니 [Rocket][]이니 하는걸 설치해서 커맨드라인으로 서버를 켜고 끄는 것은 너무 복잡하다. 그래서 GUI로 뭔가 간단하게 켜고 끄는 걸 가능하게 해야겠다 싶어서 하나 만들었다.

Rocket의 GUI 프론트엔드고, 이름은 그래서 **ROCKET DIVE**다.[^2] Tkinter를 써서 인터페이스가 구린데, Rocket 외의 다른 라이브러리에 의존성을 만들고 싶지 않았기 때문에 어쩔 수 없었다. 참고로 Tkinter는 Python 표준 라이브러리에 들어있다.

Windows를 기준으로 설치 방법을 설명하자면: Python 2.6과 [setuptools][](`easy_install` 명령어를 위해)를 먼저 설치하고 커맨드 프롬프트에서 `easy_install`로 다음과 같이 설치한다. 이때 Windows Vista 이상일 경우 커맨드 프롬프트를 관리자 권한으로 실행해야 한다.

    C:\> easy_install distribute
    C:\> easy_install rocketdive

([Distribute][]는 Rocket이 의존하고 있는데, setuptools의 대안으로 등장한 물건이다. 이게 setuptools를 덮어쓰다보니 그냥 `easy_install rocketdive`로 설치해버리면 중간에 스스로를 갈아치우려다가 오류가 나버린다. 그래서 먼저 Distribute를 설치해야 한다.)

설치가 끝나면 `pythonw.exe -m rocketdive`로 단축 아이콘을 만들면 된다.

![단축 아이콘 만드는 화면](https://media.tumblr.com/tumblr_l1zamhay271qz6t91.png)

[소스 코드는 Bitbucket에 올려뒀으니][1], Mercurial로 받을 수 있다.

    $ hg clone https://dahlia@bitbucket.org/dahlia/rocketdive

[^1]: Python과 웹 서버 사이의 통신 규약. Java의 Servlet이나 Ruby의 Rack 같은 것이라고 보면 된다. [PEP 333][pep-333] 참고.

[^2]: 아는 사람은 알겠지만 hide의 노래 제목인데, 음악과의 연관성은 딱히 없고 Rocket의 프론트엔드니 이름을 로켓 어쩌고로 해야겠네 해서 생각나서 썼다.

*[WSGI]: Web Server Gateway Interface
[gunicorn]: http://gunicorn.org/
[rocket]: https://pypi.python.org/pypi/rocket
[setuptools]: https://pypi.python.org/pypi/setuptools
[distribute]: https://pypi.python.org/pypi/distribute
[pep-333]: http://www.python.org/dev/peps/pep-0333/
[0]: https://pypi.python.org/pypi/rocketdive
[1]: https://bitbucket.org/dahlia/rocketdive
