[HTTP Link header][source]
==========================

10년도 더 됐지만, HTTP 표준으로 제안된 헤더 중에 [`Link`][1]라는 게 있다. 링크에서 짐작할 수 있다시피 HTML `<link>` 태그와 같은 용도로서, `Content-Type`이 `text/html`이 아닐 때도 `<link>` 태그에 담기는 내용들을 메타데이터로 전송할 수 있게 해준다. 예를 들어 다음과 같은 식이다.

    Link: <http://dahlia.kr/>; rel=canonical

이걸 실제로 쓰는 곳이 있을까 싶은데, GitHub API가 이걸 [페이지네이션 용도][2]로 쓰고 있다. 확실히 페이지네이션을 저렇게 하면 응답이 좀더 깔끔해진다. 무슨 뜻이냐면, 예를 들어 어떤 긴 목록을 반환하는 리소스가 있다고 했을 때,

    HTTP/1.1 200 OK
    Content-Type: application/json

    [...]

형태로 주는 쪽이 깔끔하겠지만, 페이지네이션 정보가 필요하면 다음과 같이 목록을 무언가로 더 감싸야만 한다.

    HTTP/1.1 200 OK
    Content-Type: application/json

    {'objects': [...], 'nextUrl': 'http://example.com/objects/?from=...'}

이런 경우에 GitHub처럼 `Link` 헤더를 쓰면 되겠다.

    HTTP/1.1 200 OK
    Link: <http://example.com/objects/?from=...>; rel=next
    Content-Type: application/json

    [...]

게다가 [`rel` 속성에는 원래 `next`나 `prev` 같은 것들이 들어갈 수 있다.][3] 그러고 보니 Opera 같은 브라우저는 실제로 `rel` 속성이 `next`나 `prev`인 경우에 네이베이션 버튼들이 해당 시멘틱을 따라서 작동했던 걸로 기억한다.

덧. 상관 없는 얘기지만 HTTP API를 만들 때 응답이 JSON이고 인증이 필요한 경우, [응답이 리스트이면 보안상 문제가 될 수 있다.][4] 간단히 설명하면 전혀 다른 사이트에서 `<script>` 태그로 해당 리소스를 불러오는데, 그 직전에 해당 페이지에서 `Array` 함수를 덮어씌우면 리스트 리터럴이 해당 생성자를 호출하게 되어 있기 때문에 JSONP 쓰는 것 마냥 값을 받아올 수 있다.

[1]: http://www.w3.org/Protocols/9707-link-header.html
[2]: http://developer.github.com/v3/#pagination
[3]: http://www.w3.org/TR/REC-html40/types.html#type-links
[4]: http://flask.pocoo.org/docs/security/#json-security

[source]: http://www.w3.org/Protocols/9707-link-header.html
