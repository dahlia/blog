[Persistence of Memory][source]
===============================

[방금 막 올린 글](http://blog.dahlia.kr/post/18548824137) 때문에 생각난 건데, Persistence of Memory라는 매우 깊은 통찰이 담긴 글이 있으니 일독하기를 추천한다. 개인적인 기준에서의 하이라이트만 인용해보자면…

> Most of the arguments about efficiency, though, ignore questions of functionality.  It is senseless to compare the “efficiency” of one data structure that provides different functionality than another.  A persistent data structure does *more for you* than does an ephemeral one.  It allows you to have multiple futures, including those that evolve in parallel with one another.  It makes no sense to insist that some ephemeral approximation of such a data structure is “more efficient” if it does not provide those capabilities!

불변 자료 구조(immutable data structures)가 일반적인 자료 구조에 비해 비효율적인 것은, 불변 자료 구조가 더 많은 기능—이른바 **다중 미래**(multiple futures)라고 하는!—을 제공하기 때문에 당연하다는 것. 그렇다. 반대로 얘기하면, 자료 구조의 불변성은 다중 미래라는 강력한 기능을 얻기 위한 **우연적 성질**(incidental property)이지 불변성 자체를 원해서 쓰는 게 아니라는 것이다. 같은 기능을 가지고 있다면 굳이 비효율적인 디자인을 따를 이유가 없다. 얻고자 하는 더 많은 기능을 제공하기 때문에 비효율성을 감수하는 것이다.

[source]: http://existentialtype.wordpress.com/2011/04/09/persistence-of-memory/
