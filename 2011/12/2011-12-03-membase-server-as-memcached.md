Membase Server as Memcached
===========================

Membase Server를 memcached 대신 쓰기로 했다. Membase Server는 memcached 호환 프로토콜을 사용하기 때문에  memcached를 가정하고 만든 애플리케이션을 고치지 않고도 적용할 수 있다. 사용하려는 환경은 Ubuntu이므로 .deb 바이너리를 내려받는다. ([커뮤니티 에디션 다운로드][1])

    $ wget http://packages.couchbase.com/releases/1.7.1.1/membase-server-community_x86_64_1.7.1.1.deb

설치할 때는 의존성도 함께 설치해준다.

    $ sudo dpkg -i membase-server-community_x86_64_1.7.1.1.deb 
    $ sudo apt-get -f install

Membase Server는 기본적으로 상용 제품이기 때문에 매우 훌륭한 프론트엔드 콘솔을 제공한다. 설치하고 나서 8091 포트를 웹 브라우저로 접속해보면 설정을 진행할 수 있다.

![Membase Console](https://i.imgur.com/XPNh8.png)

다만 설정을 이런 식으로 해야 하면 디플로이 자동화가 문제인데, 저 프론트엔드는 JavaScript로 구현되어 있고 실제 설정 자체는 [REST API][2]로 제공된다. 일단 대충 둘러보는 용도로는 웹 브라우저에서 프론트엔드 콘솔을 사용하는게 편할 것이다.

![Membase Configure: Step 1/4](https://i.imgur.com/JU85t.png)

자료를 저장할 파일시스템 상의 경로를 정한 뒤에 이미 존재하는 클러스터에 합류시킬 것인지 아니면 새로운 클러스터를 구성할 것인지 결정할 수 있다. 존재하는 클러스터가 없으므로 일단 만들어야 한다. 만약 클러스터에 합류하려고 한다면 클러스터 마스터의 IP 주소와 로그인 정보를 넣어야 한다.

![Membase Configure: Step 2/4](https://i.imgur.com/4AvIs.png)

그 뒤에 버킷 종류를 정해야 하는데 memcached와 Membase 둘이 있다. 짐작할 수 있다시피 둘의 차이는 영속성이다. memcached에 저장되는 자료는 휘발되어도 상관 없으므로 다중화(replication) 설정이 생략된다.

![Membase Configure: Step 3/4](https://i.imgur.com/qxPBT.png)

세번째로 나오는 화면에는 별거 없다. 적당히 채우고 진행한다.

![Membase Configure: Step 4/4](https://i.imgur.com/xzAc8.png)

마지막으로 클러스터 마스터의 관리자 계정을 만든다. 나중에 클러스터에 참여시킬 다른 노드에서 사용하게 된다.

여기까지 웹 프론트엔드 콘솔을 통해 설정한 내용은 사실 REST API로도 할 수 있다.

    $ curl -d username=Administrator -d password=passsword -d port=SAME \
           http://localhost:8091/settings/web
    $ curl -u Administrator:password \
           -d path=/opt/membase/var/lib/membase/data \
           http://localhost:8091/nodes/self/controller/settings
    $ curl -u Administrator:password -d memoryQuota=1024 \
           http://localhost:8091/pools/default
    $ curl -u Administrator:password \
           -d bucketType=memcached -d ramQuotaMB=1024 -d replicaNumber=2 \
           http://localhost:8091/controller/setupDefaultBucket
    $ curl -u Administrator:password -d sendStats=true \
           http://localhost:8091/settings/stats

클러스터 마스터 노드를 설정한 뒤에는 나머지 노드를 클러스터에 붙일 수 있다. 이 역시 웹 프론트엔드 콘솔에서 설정 가능하고 UI만 따라가면 마술처럼 잘 된다. REST API로는 이런 식으로 한다.

    $ curl -d path=/opt/membase/var/lib/membase/data \
           http://localhost:8091/nodes/self/controller/settings
    $ curl -d clusterMemberHostIp=master-node-host -d clusterMemberPort=8091 \
           -d user=Administrator -d password=password \
           http://localhost:8091/node/controller/doJoinCluster

만약 붙어있던 노드가 어떤 이유로든 장애가 발생하면 어떻게 해야 할까? 클러스터에서 빼야 한다. 이걸 자동으로 빼주게 하려면 타임아웃을 설정하여 자동 failover시키면 된다.

    $ curl -u Administrator:password -d enabled=true&timeout=60 \
           http://localhost:8091/settings/autoFailover

일단 이렇게 클러스터가 구성된 뒤에는, 애플리케이션 쪽에서 클러스터의 어떤 노드를 연결하더라도 클러스터 전체의 스토리지를 하나의 단일 스토리지처럼 투명하게 다룰 수 있게 된다.

사실 memcached로도 여러 노드를 다룰 수 있지만 기본적으로 클라이언트 쪽에서 모든 것을 다 처리해야 하기 때문에 관리가 쉽지 않다. 노드 한둘에 장애가 날 때마다 전체 노드 목록을 모든 애플리케이션 노드에 업데이트해야 하는데, 이렇게 되면 당연히 디플로이가 복잡해진다. 구현하더라도 failover가 완료되기 전까지 모든 애플리케이션에서는 장애가 난 memcached 노드를 밟을 때마다 삐걱거리며 에러 로그가 잔뜩 쌓이게 된다. 게다가 분산 책임이 클라이언트에 있으므로 전체 memcached 노드 목록이 달라질 때마다 키의 해시가 달라져서 전체 캐시가 리셋되는 현상을 방지하려면 [consistent hashing][3] 도입해야 하는데… 이쯤 되면 “심플해서” 선택했던 memcached에게 심플함은 전혀 남지 않고 관리 비용이 급속히 커진다.

만약 우리처럼

 - 애플리케이션이 memcached를 이미 사용하고 있고 (Membase Server는 memcached 호환 프로토콜을 구현한다)
 - 여러 애플리케이션 노드가 존재하고
 - 여러 memcached 노드가 존재하는

구성인 곳이라면 이미 memcached 관리에 스트레스를 꽤나 받고 있을테니 Membase Server를 memcached 대신 써보길 권하고 싶다.

[1]: http://www.couchbase.com/downloads/membase-server/community
[2]: http://www.couchbase.org/wiki/display/membase/Membase+Management+REST+API
[3]: http://www.last.fm/user/RJ/journal/2007/04/10/rz_libketama_-_a_consistent_hashing_algo_for_memcache_clients
