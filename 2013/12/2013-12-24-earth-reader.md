[Earth Reader][source]
======================

Google Reader 망한다는 소식이 뜬지 얼마 되지 않았을 때, [RSS 리더는 원래 데스크탑 앱이었다][1]는 글을 쓴 적이 있습니다. 그 때 생각만 해두고 실제로 실행에 옮기지는 못하고 있다가, Google Reader 망한지 한참 지나서야 뒷북치며 RSS 리더를 직접 만들게 되었습니다.

이름은 Earth Reader입니다. 구름(클라우드)과 반대되는 느낌의 이름을 찾다가 땅이 좋겠다고 생각해서 지었습니다. 지구 리더가 아니라 땅 리더인 셈입니다.

[Earth Reader의 목표][2]는 지난번에 썼던 글의 동기를 거의 그대로 물려받았습니다. 바로 구독자의 모든 데이터(읽었던 모든 글들, 읽은 표시, 별표 등)에 대한 제어권을 되찾기 위해, 특정 업체의 중앙집중적인 서비스에 의존하지 않고 뉴스를 구독하자는 것입니다. 그러기 위해서 다음과 같은 몇가지 세부적인 하위 목표가 생겼습니다.

- 모든 데이터는 구독자 자신에 의해 관리될 수 있어야 합니다. 데이터를 파기하는 것도, 유지하는 것도 구독자의 제어 아래 있어야 합니다. 그러기 위해 모든 데이터를 손에 잡히는 모습으로, 파일 시스템 위에 저장합니다.
- 그러면서도 기존 서비스형 뉴스 리더 서비스가 제공하던 가장 큰 장점, 바로 다양한 기기 간에 일관적인 데이터를 보여주는 것을 그대로 취합니다.
- 데이터 형식은 기존에 이미 널리 사용되던 기술적인 표준을 최대한 따르고자 합니다. 나아가, 구현 기술 역시 오픈 소스로 고쳐서 쓸 수 있도록 합니다.
- 가능하면 여러 플랫폼에서 [네이티브 앱의 형태][3]로 다가가려 합니다. (저희는 [Transmission][]의 크로스플랫폼 전략을 따르고 싶습니다.)

사실 위의 목표 중 저희가 가장 중요하다고 생각했던 몇가지는 기본적인 수준으로 달성을 했습니다. Earth Reader는 사실 데이터를 어떻게 동기화할지 고려하지 않고, 동기화 기능을 직접 제공하지도 않습니다. 하지만 원한다면 Earth Reader 데이터 폴더(저희는 ‘저장소’라고 부릅니다)를 Dropbox 폴더 안쪽에 두거나, 혹은 Google Drive, 아니면 [다음 클라우드][4] 폴더 안쪽에 두고 쓰실 수 있습니다. 컴퓨터에 익숙한 분이면 아예 직접 `rsync`를 걸어도 됩니다. 중요한 것은, [Earth Reader는 서로 다른 기기에서 동시에 같은 저장소에 접근하고 수정해도 데이터 정합성이 항상 유지되도록 고려되어 있다는 점입니다.][5]

반면 여러 플랫폼에서 네이티브 앱 형태로 만들겠다는 목표는 아직 큰 진전이 없습니다. 오늘 소개하는 Earth Reader의 첫 버전도 사실은 (저희의 목표가 무색하게도) 웹 버전입니다. 하지만 여러 앱 사이에서 공통으로 사용될 기술은 [`libearth`][6]라는 공용 라이브러리 형태로 따로 제작되고 있으므로 머지 않아 데스크탑 앱 형태로도 모습을 보여드릴 수 있을 것 같습니다.

웹 버전은 기본적으로 개인 서버가 있는 분들, 즉 코딩을 할 줄 알고 컴퓨터를 꽤 익숙하게 다루시는 분들을 대상으로 한 첫번째 구현입니다. Earth Reader는 오픈 소스이므로 초기 사용자들이 직접 기능 제안도 하고 기여도 하길 원했기 때문에 나쁜 시작은 아니라고 위안하고 있습니다.

설치하려면 일단 Python이 필요합니다. 최소 Python 2.6부터 Python 3.3 버전까지 쓸 수 있습니다. (아쉽게도 Python 3.0부터 Python 3.2까지는 쓸 수 없습니다.) 웹 버전은 현재 [PyPI][7]에 올라가 있으므로 `pip`를 써서 설치할 수 있습니다.

    $ pip install EarthReader-Web

다 설치하고 나면 `earthreader`라는 명령어가 생깁니다. `earthreader server` 명령을 써서 서버를 실행시킬 수 있습니다. 이 때 인자로 데이터를 저장할 [저장소][8] 경로를 지정해야 합니다. 존재하지 않는 경로면 알아서 디렉토리를 생성합니다.

    $ earthreader server /path/to/repository/dir
    $ earthreader server -p 8080 /path/to/repository/dir  # listen to 8080 port

브라우저를 통해 서버에 접근하면 아무 구독도 포함되어 있지 않은 빈 목록이 나옵니다. 그 상태에서 구독을 추가해서 사용해보실 수 있습니다. (아직 디자인이 안 되어 있습니다. 다소 못 생겼어도 이해해주세요…)

Python 웹 개발에 익숙하신 분들은 [WSGI 서버를 직접 운영하는 방법][9]도 있으니 참고해주세요.

혹시 개발에 적극적으로 참여하고 싶으신 분들, 혹은 사용하는데 문제가 생겨서 질문이 필요한 분들은 [웹용 Earth Reader 이슈 트래커][10](눈에 보이는 UI 관련), [`libearth` 이슈 트래커][11](로직 관련), [메일링 리스트][12](<earthreader@librelist.com>), 혹은 IRC 대화방([오징어 네트워크][13] #earthreader 채널)을 찾아주세요.

소스 코드는 GitHub 저장소에서 보실 수 있습니다:

Earth Reader for Web
:   <https://github.com/earthreader/web>

`libearth`
:   <https://github.com/earthreader/libearth>

----

Google Reader 망하기 전에 제가 [Google Reader에 있는 모든 데이터를 다 백업하는 스크립트][14]를 공개한 적이 있습니다. 그때 백업한 데이터를 Earth Reader로 그대로 옮길 수 있습니다. 스크립트 저장소에 있는 [`toearth.py`][15] 스크립트를 쓰면 백업한 데이터를 Earth Reader 저장소로 만들어줍니다.

[1]: https://blog.hongminhee.org/2013/06/01/51871409701/
[2]: http://blog.earthreader.org/2013/11/goal/
[3]: https://blog.hongminhee.org/2012/02/19/17855554774/
[Transmission]: http://www.transmissionbt.com/
[4]: http://cloud.daum.net/
[5]: http://blog.earthreader.org/2013/12/sync/
[6]: http://libearth.earthreader.org/
[7]: https://pypi.python.org/pypi/EarthReader-Web
[8]: https://github.com/earthreader/web#repository
[9]: https://github.com/earthreader/web#wsgi-server
[10]: https://github.com/earthreader/web/issues
[11]: https://github.com/earthreader/libearth/issues
[12]: http://librelist.com/browser/earthreader/
[13]: http://ozinger.org/
[14]: https://bitbucket.org/dahlia/escape-from-google-reader
[15]: https://bitbucket.org/dahlia/escape-from-google-reader/src/tip/toearth.py

[source]: http://earthreader.org/
