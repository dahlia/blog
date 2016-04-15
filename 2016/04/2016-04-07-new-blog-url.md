6년만의 블로그 이전
===================

원래 Tumblr에서 호스팅하던 블로그를 옮겼다. [2010년 초에 Tumblr로 옮긴][1] 뒤 6년만의 블로그 이사이다.
Tumblr를 떠나게 된 계기는 최근부터 내가 쓴 글에 달린 링크를 가로채서 다른 URL로 바꿔치기 하도록 업데이트됐기 때문이다.

<blockquote class="twitter-tweet" data-lang="en"><p lang="ko" dir="ltr">방금 알았는데 Tumblr가 언제부터인가 내가 글에서 링크한 URL을 가로채서 자기네 중간 리다이렉션 페이지를 거치도록 바뀐 URL을 삽입해놨다. 옵션을 찾아봐도 끄는 방법을 찾을 수 없다. 지금까지는 떠날 이유도 없고 귀찮아 냅뒀지만, 슬슬 옮겨야.</p>&mdash; Hong Minhee ・ 洪 民憙 (@hongminhee) <a href="https://twitter.com/hongminhee/status/716599931432140801">April 3, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

몇년 전부터 정적 사이트 생성기로 블로그 만드는 게 프로그래머 사이의 유행이 되어서 나 역시 옮기고 싶다고 생각했었는데,
막상 귀찮아서 생각만 하다가 계기가 생겨서 이참에 옮기게 되었다.

새 블로그 주소는 <https://blog.hongminhee.org/>이다. 참고로 이전 블로그의 모든 퍼머링크들은
내가 오기와 집념으로 거의 다 리다이렉션(`301 Moved Permanently`) 시켰다.

[Jekyll][2] 같은 훌륭한 정적 사이트 생성기도 있고,[^1] 그 외에도 다양하게 존재하지만,
예전부터 내가 원하는 정적 사이트 생성기의 조건은 어느 정도 확립되어 있었다. 그 중 가장 중요한 조건은
[2010년에 Tumblr로 블로그를 이사했을 때][1]나 지금이나 같은데, Markdown을 어떤 식으로 지원하느냐다.
지금까지 6년동안 블로그에 올렸던 모든 글을 제대로 빌드할 수 있어야 하기 때문이다.
10년 전부터 Markdown Extra 문법을 사용해왔고, 이 문법의 제대로 된 구현은 현재까지 내가 알기로는
레퍼런스 구현인 [PHP Markdown Extra][4]와 [Pandoc][5] 정도밖에 없다. 그래서 Pandoc을 Markdown
구현 백엔드로 사용하는 것들만 추리니 얼마 안 남았다. [Hakyll][6] 같은 것들이 나왔는데,
처음 조금 시도해 보다가 포기하고 그냥 직접 만들기로 했다.

[Hakyll][6]에서 아쉬웠던 것은 자체 템플릿 엔진이 반복문을 두겹 이상으로 사용할 수 없다는 점이었다.
두 단계 이상으로 접혀 들어가는 내용을 다루기가 아주 까다로웠다. 사실 설정이 그냥 Haskell 코드라서
유연하다는 장점이 있었고, 분명 내가 좀더 파고들었으면 어떻게든 해결 가능했을 것이라는 생각이 든다.
실제로 해결 비슷하게 하긴 했는데, 다 하고 보니 상당양의 로직 코드를 만든 뒤라 허탈감이 왔다.
그 뒤에 `href` 끝에 index.html 같은 것을 없애는 방법이라던가, 로컬 빌드에서는 `href`를 만들 때
index.html을 붙이고, 실제로 배포할 때는 뺀 경로로 올리는 방법 같은 것을 찾아봤지만 그런 것은 별도
기능으로 있지 않았고, 모두 다 내가 직접 구현을 해야 했다. RSS 등 몇가지 더 원하는 기능이 있었는데,
하루 종일 코딩해서 일요일 하루를 날리고 보니 인내심이 사라져서 Hakyll은 버리기로 했다.

내게 남은 휴일이 얼마 없다보니 조급해졌는데, 그래서 대충 쉘 스크립트로 Pandoc을 엮어서 결과물을
얼른 내놓기로 했다. 첫 구현은 썩 잘 돌아갔는데, 아카이브 페이지나 첫 페이지 등을 만드려면 템플릿 엔진
비슷한 게 필요해졌다. 쉘 스크립트의 단순 문자열 치환으로는 HTML 중간에 반복되는 내용을 넣기가 어려웠기
때문이다. 아니, 넣을 수는 있었는데 나중에 수정할 수 없을 것 같은 코드가 나온다.

그래서 쉘 스크립트를 대충 Python으로 옮겨 적기 시작했다. 하다보니 bash로는 쉽게 할 수 없는 추상화가
가능해져서, 하는 김에 일반화를 조금 하기도 했다. 이 정도까지 하니 졸린데다 주말이 다 사라져서 아쉽지만
다음날 이어서 작업하기로 했다. (다행히 휴가 하루 냈었다.)

최종적으로 만든 정적 사이트 생성기는 전적으로 내 블로그에서만 쓸 수 있도록 일반화가 거의 안 되어 있는
[gen.py][7] 스크립트다.[^2] 이걸 GitHub 저장소에 푸시할 때마다 자동으로 빌드되게 하고 싶어서
[Travis CI를 활용했다.][14] 그리고 빌드된 결과는 다시 GitHub Pages로 푸시된다.
결과적으로 새 블로그는 딱히 오픈 소스도 아니건만 오픈 소스를 위한 공공 인프라를 무전취식하고 있다.

하여간, 그리고 Tumblr에 올라가 있던 글을 다 옮겨와야 했다. 사실은 이 작업을 더 먼저 했다.
[이쪽도 Tumblr API를 써서 평범하게 Python 스크립팅으로 끝냈다.][9]
한번 쓰고 버릴 스크립트다보니 더더욱 오늘만 사는 심정으로 얼렁뚱땅 짰지만, 그럭저럭 잘 돌아갔다.

마지막으로 기존 URL을 새 URL로 리다이렉션시키는 작업에 착수했다. 내가 생각한 방법은,
리다이렉션만 해주는 간단한 서버를 작성하고, 기존에는 Tumblr에 물려있던 blog.dahlia.kr 도메인을
해당 서버로 돌려 물리는 것이었다. [우선 기존 Tumblr의 글 목록과, 각 글의 새 URL을 담고 있는
테이블을 만들었다.][10] 다행히 Tumblr 글을 마이그레이션하는 스크립트의 출력 결과를 가져다가
기계적으로 구성할 수 있었다. [그리고 Flask를 써서 간단한 리다이렉션 서버까지 작성했다.][11] 서버는
<del datetime="2016-04-08T02:14:59+09:00">Heroku</del><ins
datetime="2016-04-08T02:14:59+09:00">Google App Engine</ins>[^3]에 공짜 앱으로
배포하고, DNS 레코드를 수정하여 blog.dahlia.kr가 더이상 Tumblr
서버를 바라보지 않게 만들었다.

(공짜 <del datetime="2016-04-08T02:14:59+09:00">Heroku</del><ins
datetime="2016-04-08T02:14:59+09:00">Google App Engine</ins>[^3] 서버에
Travis CI, GitHub Pages 등… [돈 한푼 안내고 서버 없이 무전취식하는][15]
잔재주는 날이 갈수록 늘어난다.)

내 블로그는 이제 10년째 운영중이다. 6년 전에 블로그 이사했을 때도 RSS 주소는 유지했다.
이제는 살아있는 시체가 되어버린 [FeedBurner][12]를 쓰고 있었기 때문이다. 하여간 아직 운영은 되고
있으니 들어가서 소스 URL을 Tumblr에서 제공하는 RSS에서 새 블로그의 RSS로 옮겼다.
아마 RSS 리더로 구독해서 보고 있던 분들은 (이미 읽었던 글이 새 글로 좀 뜰 수도 있겠지만)
그대로 이어서 구독할 수 있을 것이다.

이렇게 하면 거의 다 한 것 같았는데, 생각해보니 내 기존 블로그는 Tumblr 팔로워도 상당히 많았다.
(사실 그것도 Tumblr 탈출을 망설이게 한 요인이다.) 어쩔까 하다가 기존에 올라온 글 내용을 몽땅 수정해서,
각 글의 새 URL로 링크해주기로 했다. [이것 역시 손으로 할 수는 없으니 스크립트를 짰다.][13]

여기까지 해보니 블로그 하나 옮기겠다고 온갖 삽질을 한 것 같아 보인다. 맨 처음 이사는 3년 블로깅 후에
한 것이었고, 이번 이사는 그 뒤로 6년 블로깅한 후에 옮긴 것이니, 귀찮아서 앞으로 12년간은 블로그
이사는 하지 않으련다.

[^1]: 더구나 [Jekyll][2]을 쓰면 GitHub Pages에서 빌드까지 돌려준다.

[^2]: 저 스크립트가 들어있는 [블로그 저장소][8]의 다른 문서나 스크립트들은 그렇지 않지만,
      [gen.py][7] 스크립트만은 GPLv3이다.

[^3]: [Heroku 무료 앱에는 사용량 제한이 있어서 늦은 시간이 되자 서버 오류가 나기 시작했다.][16]
      그래서 [Google App Engine으로 교체했다.][17]

[1]: https://blog.hongminhee.org/2010/02/09/379524623/
[2]: https://jekyllrb.com/
[3]: https://jekyllrb.com/docs/github-pages/#deploying-jekyll-to-github-pages
[4]: https://michelf.ca/projects/php-markdown/extra/
[5]: http://pandoc.org/
[6]: https://jaspervdj.be/hakyll/
[7]: https://github.com/dahlia/blog/blob/master/gen.py
[8]: https://github.com/dahlia/blog/tree/master
[9]: https://github.com/dahlia/blog/tree/migrate
[10]: https://github.com/dahlia/blog/blob/redirector/index.json
[11]: https://github.com/dahlia/blog/blob/redirector/redir.py
[12]: http://feedburner.com/
[13]: https://github.com/dahlia/blog/blob/redirector/edit.py
[14]: https://github.com/dahlia/blog/blob/master/.travis.yml
[15]: http://blog.hongminhee.org/2013/12/21/70680247969/
[16]: https://twitter.com/hongminhee/status/718059459919020032
[17]: https://twitter.com/hongminhee/status/718124928243879936
