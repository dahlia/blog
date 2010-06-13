Bitbucket v. GitHub
===================

내가 분산형 버전 관리 시스템의 아주 기본적인 기능만을 주로 쓰기 때문에, 아무래도 인터페이스가 좀더 친절한[^1] Mercurial이 git보다 더 좋다. 하지만 두 버전 관리 시스템을 기반으로 하는 소셜 프로젝트 호스팅 두 서비스—[Bitbucket][]과 [GitHub][]를 비교하자면 정 반대이다. 내가 볼 때 Bitbucket은 현재로서는 무료 계정에서도 1개까지는 비공개 저장소를 생성 가능하다는 것 말고는 GitHub에 비해 이렇다할 장점이 없다. 디자인도 GitHub가 더 세련됐으며, GitHub는 자기네가 호스팅해주는 프로젝트 페이지를 프로젝트의 공식 홈페이지로 사용할 수 있을 정도로 만들어주는데 비해, Bitbucket은 그렇지 않다. 하지만 이런 기능 외에도 GitHub를 사용할 수밖에 없게 만드는 것이 하나 있는데, 바로 커뮤니티 크기이다. GitHub에는 너무나 유명한 프로젝트가 많은데, Bitbucket은 대체로 Python 쪽에서만 유명한 프로젝트가 전부다. 그리고 그 외에 사용자 수에도 차이가 많다.

애초에 git은 Linus Torvalds가 C로 구현한 버전 관리 시스템이고, Mercurial은 Python으로 작성되어 있다. Mercurial은 Python을 쓰는 프로젝트에서는 사용할 명분이 충분하지만, 다른 언어에서는 조금 이상하게 느껴지기 쉽다. 이를테면 Ruby나 Perl로 작성된 오픈 소스 소프트웨어를 Mercurial을 사용해서 버전 관리를 한다고 하면 사용하는데 지장은 전혀 없음에도 Mercurial이 Python으로 작성되어있다는 사실 때문에 이상하게 여겨지는 것이다. 하지만 반대로 Python을 사용하는 프로젝트가 Mercurial 대신 git을 쓴다고 해서 어색하게 느껴지진 않는다. 이렇기 때문에 아무래도 git 사용자가 훨씬 많아질 수밖에 없고, Mercurial은 점차 Python 커뮤니티에서만 사용되는 버전 관리 시스템이 되어가는 것 같다.

어찌됐든 결국 GitHub가 사용자가 훨씬 많기 때문에 프로젝트를 홍보하기 위해서는 GitHub를 이용하는 편이 훨씬 유리하다. 그래서 [야간개발팀][lunant]도 Bitbucket에서 Mercurial로 관리하던 오픈 소스 프로젝트들을 모두 GitHub로 옮겨버렸다. 인지도를 좀 더 올릴 기회가 많기 때문에 어쩔 수 없는 선택이었는데, 사용법 자체는 Mercurial이 편하기 때문에 내부의 비공개 저장소는 여전히 Mercurial을 사용해 관리하고 있다.

한 줄 정리를 하자면, 홍보에 신경을 쓰고 있다면 어찌됐든 GitHub를 권한다. 그냥 편한 게 좋다면(그리고 Subversion에 익숙하다면) Bitbucket에서 Mercurial을 써도 문제 없다.[^2]

 [^1]: Subversion에 익숙한 사람한테만 친절하게 느껴지는 걸지도 모른다.

 [^2]: 예를 들어 [Pocoo Team][pocoo]의 [Armin Rochacher][mitsuhiko](mitsuhiko)도 [Flask][] 같은 프로젝트는 GitHub에서 공개했지만, Werkzeug 같은 다른 대부분의 프로젝트들은 Mercurial을 사용한다. 덕분에 Werkzeug은 나온지 2년이 넘었고 Flask는 올해 4월에 나왔지만 Flask가 훨씬 더 유명하고 뜨겁다.

 [bitbucket]: http://bitbucket.org/
 [github]: http://github.com/
 [lunant]: http://lunant.net/
 [pocoo]: http://www.pocoo.org/
 [mitsuhiko]: http://lucumr.pocoo.org/
 [flask]: http://github.com/mitsuhiko/flask
