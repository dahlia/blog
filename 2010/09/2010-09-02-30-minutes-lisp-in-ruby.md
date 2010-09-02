[30 minutes Lisp in Ruby][source]
=================================

소프트웨어 마에스트로 과정의 멘토단 중 하나로 선출되고 난 뒤, 요즘에는 Lisp 구현 프로젝트를 멘토링하고 있다. 멘티들이 Lisp을 구현하는데 내가 도와주는 식이다. 그런데 다들 Lisp 구현을 해보기는 커녕 Lisp을 써본 적도 없는 친구들이 대부분이라 난항을 겪고 있는데, 그래서 내가 멘티들을 모아다 같이 앉아서 약 30분 가량 해설을 하면서 처음부터 끝까지 Lisp을 구현해 보았다.

그날은 이미 파서는 다들 구현했고, 파싱된 리스트를 평가(`eval`)하고 적용(`apply`)하는 부분을 설명해야 했기 때문에, 별도로 s-expression 파서를 구현하지는 않았다. 대신 Ruby의 문법을 사용해서 `eval`을 구현했다. 그래서 팩토리얼 함수를 구현하면 다음과 같은 모양의 코드가 된다.

     [:def, :factorial,
       [:lambda, [:n],
         [:if, [:"=", :n, 1],
               1,
               [:*, :n, [:factorial, [:-, :n, 1]]]]]]

링크한 소스 코드는 그날 작성된 것은 아니고, 내가 집에 와서 같이 지내는 야간개발팀 친구들에게 비슷한 설명을 한 번 더 하면서 작성한 것을 토대로 정리를 많이 한 것이다.

덧. reddit에도 올렸다. <http://www.reddit.com/r/ruby/comments/d8ldl/30_minutes_lisp_in_ruby/> Hacker News에도 올렸다. <http://news.ycombinator.com/item?id=1655673>

<script src="http://gist.github.com/562017.js"> </script>

[source]: http://gist.github.com/562017
