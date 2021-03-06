[A Record of reStructuredText Syntax Alternatives][source]
==========================================================

reStructuredText는 매우 훌륭한 마크업 언어 디자인 사례다.[^1] 어째서 그러한지는 링크한 이 글, [후보 문법에 대한 기록][1] 문서를 보면 알 수 있다.

일단, 결과물이 아니라 과정에 존재했던 여러 후보들에 대한 문서가 남아있다는 점 자체가 매우 모범적이다. 마크업 언어 뿐만 아니라, 프로그래밍 언어, 혹은 모든 소프트웨어들이 문서화를 하지 않는다. 당연히 디자인 문서(디자인 골과, 미션을 달성하기 위한 디자인 과정에서 있었던 디자인 결정들에 대해 상세히 기록한 문서)를 남기는 소프트웨어는 더욱 적다.

저런 문서가 있는 소프트웨어는 그런 게 있다는 사실 하나만으로 소프트웨어가 훌륭하다는 증거가 된다. 사려깊게 후보들을 따져보고 합리적인 판단을 하려면 어떤 식으로든 디자인 문서 비슷한 게 초안 형태로 나오게 된다. 예를 들면 SQLite는 내부 구현 디자인에 관한 문서가 여러 페이지로 존재한다. 홈페이지에 가면 찾아볼 수 있다. 또다른 예로는 Lua가 있다. [Lua 5.0의 구현][2]이라는 디자인 문서는 Lua의 내부 구현 디자인과 언어 디자인에 대해 설명한다. 왜 그런 디자인 결정을 했는지를 설명한다. 프로그래밍 언어 디자인/구현을 공부하려는 사람에게는 값어치를 매기기 힘든 보물과도 같은 자료라고 할 수 있다.

그리고 매우 희귀한 몇몇 소프트웨어는 디자인 문서 뿐만 아니라, 디자인 과정에 대한 기록까지 문서로 남아있다. 지금 소개하는 reStructuredText가 그렇고, 언어 중에서는 Perl이 CPAN을 통해 언어 디자인 과정을 모두 기록하고 문서화하는 걸로 유명하고, 이에 영향을 받은 Python 역시 PEP을 통해 디자인 과정 전체를 기록하고 문서화한다. 디자인 결정에 있어서 어떤 대안이 있었으며, 어떤 이유에서 그것들이 선택되지 않았는지, 어떤 이유에서 그런 결정이 최종적으로 내려졌는지 알 수 있다. 이런 문서들은 유명한 오픈 소스 소프트웨어들의 소스 코드를 읽는 것만큼이나, 혹은 그 이상으로 배우는 것이 많지만, 소스 코드를 읽는 것보다는 훨씬 쉽다는 점에서 가치를 따지기 힘들 정도로 값진 자료들이다.

디자인 과정의 기록을 문서화하면 소프트웨어를 선택할 때도 좀 더 합리적인 결정을 할 수 있게 도와준다. 예를 들어 어떤 비동기 입출력 라이브러리가 비동기 호출을 코루틴 대신 CPS로만 하게 한다고 하자. 만약 그 라이브러리의 디자인 과정을 기록해뒀다면, 해당 디자인 결정 과정에서 후보에 코루틴이 있었지만 어떤 이유에서 탈락되었는지, 아니면 애초에 후보에도 없었는지 알 수 있다. 만약 후자라면 만든 사람은 코루틴이라는 더 좋은 방법이 있다는 걸 그냥 몰라서 CPS를 쓴 것이라고 추측할 수 있다.

솔직히 말해서 요즘 유행하는 여러 언어들이나 플랫폼들은 이런 게 거의 없다시피하다는 점에서 의심스러운 게 한둘이 아니다. 그 소프트웨어들의 디자인 결정은 의심스러운 것들이 많다. 그 결정들이 단순히 소프트웨어 설계자의 잘못된 판단이나 효용은 없고 고집스럽기만 한 취향 혹은 설계 능력 부재 같은 비합리성으로부터 유래한 것인지, 아니면 실제로 많은 제약과 충분한 이유가 있어서 매우 합리적으로 선택한 결과인지는 알 수 없다.

대신 요즘 나오는 소프트웨어들은 디자인 문서 말고 홈페이지 디자인을 힙하고 예쁘게 한다. ㅋㅋㅋㅋ 감성 마케팅의 시대니까 오픈 소스 소프트웨어도 홈페이지 예쁘게 만드는 건 중요하긴 하다. 하지만 그건 소프트웨어를 홍보하는 사람의 입장에서 해야 할 행동이고, 여러 플랫폼과 소프트웨어 중에 하나를 선택해야 하는 사람의 입장에서는 그런 것에 휘둘려서 뭔가 쿨해보이긴 하는데 실속은 없는 것들을 선택하는 일이 없도록 조심할 필요가 있다. 내 개인적인 조언은, **그 소프트웨어의 디자인 문서를 읽고 결정하라는 것이다.** 중요한 결정인 경우, 난 기본적으로 디자인 문서가 없는 소프트웨어는 아예 선택에서 웬만하면 제외하는 편이다.

[^1]: 내가 하고 싶은 말은, 정확히 말하자면, ((훌륭한 (마크업 언어)) 디자인 사례)가 아니라 ((훌륭한 ((마크업 언어) 디자인)) 사례)라는 뜻이다. 결과물 말고 디자인 과정 자체가 훌륭하다는 얘기.

[1]: http://docutils.sourceforge.net/docs/dev/rst/alternatives.html
[2]: http://www.lua.org/doc/jucs05.pdf

[source]: http://docutils.sourceforge.net/docs/dev/rst/alternatives.html
