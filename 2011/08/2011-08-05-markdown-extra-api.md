[Markdown Extra API][source]
============================

글을 쓰다보면 바닐라 [Markdown][] 그대로 쓰기보다는 테이블이나 각주 같은 것들 때문에 확장 스펙인 [Markdown Extra][]를 쓰게 되는데,[^1] 이 확장 스펙을 제안한 Michel Fortin이 직접 만든 레퍼런스 구현 비슷한 것이 PHP Markdown Extra이다. 그런데 Markdown이 여러 구현이 많지만 이 확장 스펙의 모든 기능을 제대로 구현한 것은 아직 PHP Markdown Extra 말고는 없다. 그래서 나처럼 확장 스펙의 모든 기능을 많이 활용하는 사람은 다른 구현을 쓰다보면 불편함을 느낀다. 하지만 이것 하나 때문에 모든 웹 애플리케이션을 PHP로 만들 수는 없는 노릇이라, 이번에 그냥 HTTP로 요청하면 결과를 던져주는 API로 만들었다. 개인적으로 Google App Engine 같은 플랫폼에서 쓰려고 만든 것이니만큼 별다른 기능은 없다.

    $ curl -F'text=*Markdown* test' http://markdownextra.phpfogapp.com/
    <p><em>Markdown</em> test</p>

[^1]: [이 블로그도 Markdown Extra를 지원한다는 이유 때문에 Tumblr에서 운영하게 되었다.][1]

[Markdown]: http://daringfireball.net/projects/markdown/
[Markdown Extra]: http://michelf.com/projects/php-markdown/extra/
[1]: https://blog.hongminhee.org/2010/02/09/379524623/


[source]: http://markdownextra.phpfogapp.com/
