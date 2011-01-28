Java Collections Framework
==========================

Java Collections Framework는 확실히 잘 디자인되어 있다. 다음 몇 가지 아쉬운 점을 제외하면.

 - 자료구조가 항상 mutable하다는 가정을 깔고 있다. 예를 들어 immutable list를 구현하려면 `java.util.List`를 구현하고 `add()` 등 자료 구조에 변경을 가하는 연산에 대해서는 `java.lang.UnsupportedOperationException` 예외를 내도록 구현해야 하는데 이건 분명 넌센스다.

 - Python이나 Clojure 같은 언어에서 자주 사용되는 lazy data structure에 대한 고려가 딱히 없다. Clojure나 Python 같은 언어를 보면 확실히 언어에서 제공하는 자료 구조의 laziness는 엄청나게 강력하다는 것을 알 수 있는데, 애초에 Java는 이런 문화와 거리가 멀다.

 - Java에 mixin이나 다중 상속이 없고 인터페이스만 제공되기 때문에, 굳이 구현할 필요 없는 것들을 구현해야 하고 boilerplate code가 등장하기 시작한다. 예를 들어 `java.util.List` 인터페이스의 `toArray()` 메서드는 `iterator()`와 `size()`를 구현했으면 알아서 채워질 수 있는 메서드이다.

역시 Java는 함수형 프로그래밍 스타일에서 배울 것들이 아직 너무나 많아보인다.
