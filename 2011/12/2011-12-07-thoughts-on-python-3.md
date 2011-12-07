[Thoughts on Python 3][source]
==============================

[Flask][], [Werkzeug][], [Jinja2][] 등을 만든 [Armin Ronacher][]가 블로그에 [Python 3에 대한 생각][1]을 올렸다. 급진적인 주장은 별로 없고 뭐 다들 알만한 사람들은 아는 내용이지만 전체적으로 잘 정리되어 있으니 관심 있는 사람들은 전문을 읽어보면 되겠다. 여기에는 개인적으로 인상깊었던 부분만 인용해보겠다.

> “Always complaining, not doing anything”. There is just so much stuff I would love to see Python go but at the end of the day, I'm a user of Python more than a developer.

세상에 Python 사용자는 많지만 Python 언어 구현을 해킹하는 사람은 매우 드물다. Python 사용자는 항상 Python 언어의 디자인에 대해 이러쿵 저러쿵 떠들지만 세상을 위해 실질적으로 코드를 기여하지는 못한다.

> But the real reason why I loved and adored Python was the fact that I was looking forward to each new release like a child to Christmas. The small things and improvements blew my mind. Even benign things like the fact that you can now specify a starting index for the enumerate function made me appreciate a new release of Python. And all that with a strong focus of backwards compatibility.

지금까지의 Python은 어느 정도 하위 호환성을 지키면서 점진적으로 진화해 왔다. 초기 디자인은 나쁠지 몰라도, 시간이 지나면서 “잘못된 결정들”은 하나 둘 고쳐져 나간다. Python 언어의 가장 중요한 부분은 언어 자체가 아니라 PEP 같은 언어 개선 프로세스이다. 나도 강하게 동의하는 부분.

조금 더 내 생각을 적자면…, 세상에는 C++나 Java와 같은 위원회 언어라는 것이 존재한다. 하지만 그 반대편에는 Perl이나 Python과 같이 “언어를 쓰는 사람이 곧 언어의 디자인에 기여하는” 커뮤니티 언어들도 존재한다. 어떤 언어가 더 좋은지 얘기하기는 힘들다. 하지만 어떤 언어 디자인 프로세스가 더 좋은지는 명백하다. 1995년 첫 Java의 디자인은 1991년 첫 Python의 디자인보다 전체적인 면에서 대체로 더 훌륭했다(고 생각한다). 2011년 12월 현재, 일반적인 Java 코드는 IoC로 점철되어 있으며 Python은 제너레이터와 코루틴을 사용한다.

> Python 3 is in the spot where it changed just too much that it broke all our code and not nearly enough that it would warrant upgrading immediately. And in my absolutely personal opinion Python 3.3/3.4 should be more like Python 3 and Python 2.8 should happen and be a bit more like Python 3. Because as it stands, Python 3 is the XHTML of the programming language world. It's incompatible to what it tries to replace but does not offer much besides being more “correct”.

결국 Python 3와 XHTML은 비슷한 운명을 가지고 있다. 대체하려 하는 대상과 호환되지 않는 주제에 더 “올바르길” 요구하면서 제공하는 것은 별로 없다.

> Python is not “too big to fail”. Python can become unpopular very quickly. Pascal and Delphi became niece languages even though they were amazing even after the introduction of the .NET framework and C#. They were ruined by mismanagement more than anything else. People still develop in Pascal, but how many are starting new projects in it? Delphi does not work on the iPhone, it does not run on Android. It's not well integrated into the UNIX market. And if we're honest, in some areas Python is already losing track. Python used to be sufficiently popular in computer games but that ship has sailed a long time ago. In the web community new competitors arrive on a daily basis and if we like it or not, JavaScript is becoming more and more an ubiquitous scripting language that challenges Python.

> Delphi did not adjust quick enough and people just jumped on the next technology. If 2to3 is our upgrade path to Python 3, then py2js is the upgrade path to JavaScript.

Python 3가 현재의 방향을 고수하면 Delphi처럼 될 것이다. 안 쓰이는 것은 아니지만 새로운 프로젝트에서 Python을 선택하는 일은 적어질 것이다.

[Flask]: http://flask.pocoo.org/
[Werkzeug]: http://werkzeug.pocoo.org/
[Jinja2]: http://jinja.pocoo.org/
[Armin Ronacher]: http://lucumr.pocoo.org/
[1]: http://lucumr.pocoo.org/2011/12/7/thoughts-on-python3/

[source]: http://lucumr.pocoo.org/2011/12/7/thoughts-on-python3/
