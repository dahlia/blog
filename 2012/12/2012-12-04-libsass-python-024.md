[libsass-python 0.2.4][source]
==============================

[libsass-python 0.2.4][1] 버전을 릴리즈했습니다. (CSS의 수퍼셋 언어인 [SASS/SCSS][2]의 Python 바인딩입니다.) 이번 버전에 크게 바뀐 것은 다음 두 가지입니다.

- 이번 버전부터 [`sassc`][3]라는 명령행 도구가 제공됩니다.
- [libsass][] 업스트림의 그동안 변화([`e997102`–`a84b181`][4])를 머지했습니다. 그 사이에 바뀐 것 중에서 가장 눈에 띄는 것은 [content block을 mixin에 전달할 수 있는 기능][5]이 추가된 것입니다.

설치는 `pip`나 `easy_install`로 할 수 있습니다. PyPI 패키지 네임은 `libsass`입니다(`libsass-python`이 아님).

    $ pip install libsass
    $ easy_install libsass

참고로 `pip`는 egg를 설치하지 못합니다. libsass는 C 확장이므로 컴파일을 해야 하는데 Windows에서 컴파일을 하려면 Visual Studio가 필요합니다.그래서 PyPI에 Windows용 64비트 바이너리 egg도 올려뒀습니다. 근데 `pip`로 설치하려고 하면 그걸 쓰지 않고 소스코드를 빌드하려고 하다가 Visual Studio 없다고 에러가 날 겁니다. 그런고로 Windows 쓰시는 분들은 `easy_install`로 설치해주세요.

[libsass]: https://github.com/hcatlin/libsass
[1]: http://pypi.python.org/pypi/libsass/0.2.4
[2]: http://sass-lang.com/
[3]: http://dahlia.github.com/libsass-python/sassc.html
[4]: https://github.com/hcatlin/libsass/compare/e9971023785dabd41aa44f431f603f62b15e6017...a84b181a6e59463c0ac9796ca7fdaf4864f0ad84
[5]: http://sass-lang.com/docs/yardoc/file.SASS_REFERENCE.html#mixin-content

[source]: http://pypi.python.org/pypi/libsass/0.2.4
