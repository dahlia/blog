Dynamic scoping
===============

Flask와 Werkzeug에는 [context local proxy][1]가 있다. ([관련 글][2]도 참고.) 이걸 통해 같은 전역 변수지만 실제 내용은 각 요청(즉, 문맥)마다 다른 것을 가리키게 만들어둔 것이다. 이렇게 한 이유는 사실 알고보면 별 게 아니다. Flask의 디자인 문서에 해당 부분을 [그렇게 만든 이유][3]가 나와있다.

> [<del>왜죠.</del>][4] 저거 안 좋은 생각 같은데요.
>
> Why is that and isn’t that a bad idea?
>
> 네, 보통 쓰레드 로컬을 쓰는 건 대개 그리 훌륭한 아이디어는 아닙니다. 쓰레드 로컬은 쓰레드 개념에 기초하지 않은 서버 위에서는 문제를 일으키는데다[^1] 큰 규모의 애플리케이션은 유지보수하기 힘들게 만듭니다. 하지만 Flask는 큰 규모의 애플리케이션이나 비동기 서버를 염두하고 디자인되지도 않았습니다. Flask는 전통적인 웹 애플리케이션을 빠르고 쉽게 만들 수 있게 만들고 싶었습니다.
>
> Yes it is usually not such a bright idea to use thread locals. They cause troubles for servers that are not based on the concept of threads and make large applications harder to maintain. However Flask is just not designed for large applications or asynchronous servers. Flask wants to make it quick and easy to write a traditional web application.

돌려서 말하고 있지만, 사실 Django처럼 매 뷰 함수마다 `request` 인자를 맨 앞에 붙이는 것이 *빠르고 쉽게* 만드는 측면에서는 거추장스러운 존재인 것은 맞다. 아마 그래서 반복되는 인자를 제거하기 위해, 즉 PHP의 초전역(superglobals) 변수 쓰듯이 Python으로 웹 애플리케이션을 만들고 싶었기 때문에 저런 디자인 선택을 한 것으로 보인다.

언어적인 면에서 보자면, 반복적인 인자를 제거하는 방법 중 가장 널리 알려진 패턴은 인자들을 하나의 자료형으로 묶어서 넘기는 것이다. 하지만 정확히 말하자면 이건 둘 이상의 반복되는 인자를 그보다 적은 수의 반복되는 인자로 바꾸는 것이지, 위 상황처럼 단 하나의 반복되는 인자를 아예 제거하고 싶을 때는 작동하지 않는 패턴이다.

이럴 때 쓰는 것이 바로 동적 스코핑(dynamic scoping)이다. 동적 스코핑을 지원하는 언어는 그렇게 많지 않다. 내가 확실히 알고 있는 언어 중에서는 Common Lisp, Emacs Lisp[^2], Clojure, Perl 정도인데, 어쨌거나 Python에는 없다.

동적 스코핑은 정적 스코핑(static scoping), 즉 일상적으로는 보통 렉시컬 스코핑(lexical scoping) 혹은 클로져(closure)라고 하는 것과 비교되는 개념이다. 예를 들어 다음 JavaScript 코드를 보자.

    function makeAccount(balance) {
        return function(add) {
            return balance += add;
        };
    }

    var accountA = makeAccount(0);
    var accountB = makeAccount(5);

    console.log(accountA(1));
    console.log(accountB(10));
    console.log(accountA(100));

위 코드는 각각 1, 15, 101을 출력한다. 정적 스코핑은 가장 널리 쓰이는 기법이고 잘 알려져 있으므로 굳이 어렵게 설명할 필요는 없고, 핵심만 말하자면 위 코드의 안쪽 익명 함수에 위치한 `balance` 변수는 바깥족 `makeAccount()` 함수의 인자로 들어온 `balance`를 가리킨다. 호출하는 쪽 문맥에 `balance`가 무엇이든, 있든 없든 익명 함수 안쪽의 `balance`는 항상(정적으로) lexically 바로 바깥쪽에 위치한 `balance`를 가리킨다.

이것과 반대가 되는 개념인 동적 스코핑은 다음과 같이 작동한다. (Perl 모르는 분들을 위한 엉터리 간단 설명: `sub`는 Python의 `def` 같이 함수/서브루틴을 만드는 키워드이다. 그 뒤에는 이름이 오거나 익명 함수의 경우 이름이 생략된다. 함수 안에서 `shift`는 첫번째 인자를 뜻한다. 정확히는 인자는 배열로 들어오고 `shift`는 배열의 첫번째 인자를 빼서 반환하는 함수. 근데 이 함수는 인자가 생략되면 자동으로 사용되고 있는 함수의 인자 배열에 암시적으로 적용됨. `say`는 출력 키워드.)

    use feature qw(say);

    sub add {
        $balance += shift;
    }

    sub transaction_a {
        local $balance = 0;
        say add(1);
        transaction_b();
        say add(100);
    }

    sub transaction_b {
        local $balance = 5;
        say add(10);
    }

    transaction_a();

위 코드 역시 1, 15, 101을 출력하지만 원리는 사뭇 다르다. `add()` 함수는 정의되지 않은 `$balance`라는 변수를 사용하려 든다. 실제 `$balance` 변수는 **함수가 정의되는 쪽이 아니라, 함수가 호출되는 쪽에서** 선언된다. 바로 `local`이 dynamic scoped variable를 선언하기 위한 Perl의 키워드이다. 이렇게 선언된 변수는 해당 스코프에서 호출되는 모든 함수를 **관통**(침투)한다.

나도 잘은 모르지만 Perl 커뮤니티에서도 `local`은 뭔가 어려운 개념, 혹은 잘 쓰이지 않는 기능 정도로 이해되는 것 같다. 물론 이런 동적 스코핑은 실제로 쓰려고 하면 적용할 구석이 마땅치 않고, 정적 스코핑과 달리 얼른 와닿는 개념도 아니기 때문에 오히려 유지보수에 방해가 될 수도 있다. 하지만 Flask의 `request`, `g` 같은 컨텍스트 로컬 사용은 그야말로 매우 예시로 들기 딱 좋은, 언어에 동적 스코핑이 없어서 나타나는 패턴의 사례다. (이 블로그의 지속적인 테마지만, 나는 대부분의 패턴이 기본적으로 언어의 직무 유기에서 비롯된 workaround라고 생각한다.)

다양하게 쓰일 수 있는 강력하지만 용도가 다소 모호한 프리미티브도 최대한 수용하기 보다는 (Common Lisp이나 Perl이 대체로 이런 편이다), 정갈하고 명확한 용도의 기능셋으로 제한하려는 Python의 철학에 있어서 (Java도 대체로 비슷한 성향인듯), 확실히 동적 스코핑은 그다지 어울리지 않는 개념이긴 하다. 하지만 어쨌거나 나는 동적 스코핑이 언어에 없어서 Flask가 context locals 같은 걸 만들 수밖에 없었다고 생각하고, 결과적으로는 비참한 일면이라고 생각한다.

결론: 1. 난 언어 만들면 동적 스코핑 지원해야징. 2. Python도 까일 구석은 얼마든지 있다.

[^1]: 예를 들어 모든 요청이 하나의 프로세스, 하나의 쓰레드/코루틴 안에서 단순히 이벤트 루프로 처리되는, 요즘 유행하는 서버들을 생각해보자. 실제로는 Flask는 저런 서버 위에서 잘 작동하긴 한다. 하지만 모든 서버에서 잘 작동하냐는 면에서는 보장하기 힘들다는 점에서는 맞는 이야기다.

[^2]: 근데 이건 오히려 더 자주 쓰이는 정적 스코핑을 제공 안해서 뭔가 디자인이 잘못되어 있음.

[1]: http://flask.pocoo.org/docs/reqcontext/
[2]: https://spoqa.github.io/2012/05/07/about-flask-request.html
[3]: http://flask.pocoo.org/docs/design/#thread-locals
[4]: https://namu.wiki/w/%EC%99%9C%EC%A3%A0
