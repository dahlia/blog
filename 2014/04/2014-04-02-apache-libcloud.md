[Apache Libcloud][source]
=========================

최근 [libcloud][]를 써볼 일이 있었다. 많이 써보지는 않았지만 여러모로 좋은 라이브러리라는 생각이 들어 소개해본다.

Libcloud는 [boto][]와 비슷한 기능을 공유하는 라이브러리인데, boto가 Amazon Web Services API의 클라이언트 라이브러리라면, libcloud는 AWS 외에도 Microsoft Azure, Google Cloud Compute 등 다양한 업체의 서비스도 함께 지원한다는 점이 가장 큰 차이점이라고 할 수 있다. 어차피 각 업체마다 대응되는 같은 용도의 서비스가 있는데, 크게 EC2 같은 가상화 인스턴스 서비스 (그야말로 클라우드의 primitive라고 할 수 있는…), EBS와 같이 거기서 쓸 블록 스토리지 서비스, S3와 같은 오브젝트 스토리지 서비스, ELB 같은 로드 밸런서 서비스, Route 53 같은 DNS 서비스 등이다.

그래서 가령 libcloud를 이용해서 EC2 인스턴스를 새로 만들고, 만들었던 인스턴스를 삭제하고, S3에 이미지를 올리는 스크립트를 짜고 나서, 맨 위쪽에서 드라이버 종류만 AWS에서 다른 업체로 바꾸면 그대로 돌아간다. (실제로는 [각 프로바이더마다 확장하는 기능][1]이 존재하는데, 네이밍 컨벤션에 따라 그런 함수나 인자명은 앞에 `ex_`가 붙는다.)

Libcloud는 현재 25 종류 이상의 드라이버를 제공하고 있고, 이 안에는 심지어 KT ucloud까지 포함되어 있다. [강대명 씨가 드라이버 코드를 기여했다고 한다.][2] 나는 앞으로도 쓸 일이 없겠지만… 전략적으로 돈이 없을 때 ucloud를 쓰다가 사업이 번창하여 돈을 많이 벌면 AWS 등으로 옮길 때 유용하게 쓸 수 있을 것이다. ㅋㅎㅎ

이 외에도 boto보다 libcloud가 더 나은 점이 많다.

- API가 boto보다 더 깔끔하고 쓰기 쉽게 되어 있다. 여러 클라우드 서비스를 오갈 일이 없이, 그냥 AWS만 쓴다고 해도 boto의 대안으로서 나쁘지 않다.
- Python 2에서만 돌아가는 boto와 달리 Python 3에서도 아주 잘 돌아간다.
- 더미 드라이버를 제공하기 때문에 단위 테스트 짜기가 훨씬 쉽다. boto를 쓰면 mock을 만들거나, 아예 libcloud가 해주는 그런 레이어링을 내 애플리케이션 코드에서 만들어야 하는데 이러다가 풀고자 하는 문제에 집중을 못하게 된다.

물론 아직 boto를 써야만 하는 이유도 있다. 가령 SQS 같이 AWS에서 제공하지만 다른 업체들에서는 일반적으로 제공하지 않는 종류의 제품군은 libcloud로 커버가 안된다. 그런 것들을 boto를 이용해서 쓰고 있었다면 당장 libcloud를 쓰기에는 기능이 부족할 것이다.

[libcloud]: http://libcloud.apache.org/
[boto]: http://docs.pythonboto.org/
[1]: https://libcloud.readthedocs.org/en/latest/faq.html#what-are-the-extension-methods-and-arguments
[2]: http://charsyam.wordpress.com/2013/11/17/%EC%9E%85-%EA%B0%9C%EB%B0%9C-libcloud-%EB%A1%9C-kt-olleh-ucloud-biz-%EC%9D%B4%EC%9A%A9%ED%95%98%EA%B8%B0/

[source]: http://libcloud.apache.org/
