From Celery to gevent
=====================

내부적으로 만들어서 사용하는 빌드봇이 있다. Bitbucket 커밋 훅에 걸어놓고 쓰는 건데, 커밋했을 때마다 IRC 채널에 알려주는 일과 커밋 로그에 이슈 번호가 언급되었을 경우 해당 이슈에 코멘트로 커밋 로그를 링크해주는 일을 한다.

커밋 훅 인터페이스가 HTTP `POST`로 작동하는 일반적인 [WebHook][]인데 지금까지는 요청을 받으면 [Celery][]에 태스크를 던져놓고 Celery가 백그라운드에서 IRC에도 노티하고 이슈트래커에도 코멘트를 남기는 식으로 만들어뒀었다. 이 빌드봇은 [ep.io][]에 올려놓고 있는데, 이상하게 어제부터 ep.io에서 Celery beat 프로세스가 작동하지 않길래 삽질하다가 그냥 Celery 쓰는 것을 포기하고 [gevent][]로 [`spawn`][gevent.spawn]하도록 바꿨다. 간단한 프로그램이라 그랬겠지만, 생각보다 변경이 어렵지는 않았다.

    from celery import task

대신

    import gevent.monkey
    gevent.monkey.patch_all()

이라고 쓰고, 태스크 함수에 붙은 `@task` 데코레이터를 다 지운 다음,

    func.delay(arg, arg)

로 호출하던 것을

    gevent.spawn(func, arg, arg)

로 고치면 모든 것이 잘 작동한다. HTTP 응답을 바로 주기 위해서 `spawn`된 프로세스를 [`join`][gevent.Greenlet.join]할 필요는 없다.

[WebHook]: http://webhooks.org/
[Celery]: http://celeryproject.org/
[ep.io]: http://ep.io/
[gevent]: http://gevent.org/
[gevent.spawn]: http://gevent.org/gevent.html#gevent.spawn
[gevent.Greenlet.join]: http://gevent.org/gevent.html#gevent.Greenlet.join
