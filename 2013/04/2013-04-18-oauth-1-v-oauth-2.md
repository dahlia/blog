[OAuth 1 v. OAuth 2][source]
============================

지난해 Daniel Greenfeld가 [Python OAuth 구현체들의 유감스러운 상태][1]에 대해 글을 쓰고난 뒤, 이 문제가 중요하다고 여긴 Idan Gazit는 OAuth를 철저히 표준에 의거하여 “제대로” 구현하는 [oauthlib][] 라이브러리를 만들었다. 이 라이브러리는 앞서 링크한 글의 문제를 해결하려면 기존 Python 커뮤니티에 혼란을 주었던 각종 OAuth 1 및 OAuth 2 라이브러리로부터 승리해야 했기 때문에 그 모든 것들의 기능을 총망라하고 있다. OAuth 1 및 OAuth 2 구현을 모두 제공하고 있을 뿐 아니라, 클라이언트와 프로바이더 구현 모두 제공한다. 따라서 2013년 4월 현재 Python에서 OAuth를 쓴다고 하면 OAuth 1을 쓰든 OAuth 2를 쓰든 간에 [oauthlib][]을 선택하는 것이 정답이다.

이 oauthlib의 문서 앞쪽에는 어떤 인증 수단을 선택해야 할지에 대한 친절한 가이드라인을 [별도 장][2]을 할애해서 다루고 있는데 oauthlib 자체와 독립적으로 설명하고 있기 때문에 *Python을 쓰고 있지 않더라도* 인증 수단이 필요한 모든 클라이언트/서버 프로그래머에게 도움이 된다고 생각해서 링크한다. 분량도 간결하고 내용도 매우 훌륭하다. 추천!

덧. oauthlib은 이름도 그렇고 어쩐지 Python 표준 라이브러리에 포함되는 것을 염두한 것 같기도 하다.

[1]: http://pydanny.com/the-sorry-state-of-python-oauth-providers.html
[2]: https://oauthlib.readthedocs.org/en/latest/oauth_1_versus_oauth_2.html
[oauthlib]: https://github.com/idan/oauthlib

[source]: https://oauthlib.readthedocs.org/en/latest/oauth_1_versus_oauth_2.html
