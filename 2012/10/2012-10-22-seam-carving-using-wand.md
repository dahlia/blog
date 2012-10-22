Seam carving using Wand
=======================

<img src="https://raw.github.com/dahlia/wand/e7e8d415b7b125c6aae2b1695ffecaaea392860f/docs/_static/original.jpg" alt="원본 이미지" width="187" height="242">

이미지의 너비와 높이에 변화를 주는 방법에는 여러가지가 있다. 가장 흔한 방법으로는 리사이징(resizing)과 크롭(cropping)이 있는데 이 둘에는 각자의 단점이 있다.

<img src="https://raw.github.com/dahlia/wand/e7e8d415b7b125c6aae2b1695ffecaaea392860f/docs/_static/resize.jpg" alt="리사이즈한 이미지" width="140" height="242">

리사이징은 이미지의 전체를 모두 포함시키면서 돋보기나 오목렌즈처럼 이미지를 확대/축소하는 방법이다. 하지만 리사이징은 이미지의 너비/높이 비율을 원본과 다르게 하고 싶을 때 이미지의 비율이 깨져 납작하거나 길쭉히 보이게 된다는 단점이 있다. 위에 첨부한 이미지를 보면 원본에 비해 <del>IU가</del> 기형적으로 길쭉하게 보인다.

<img src="https://raw.github.com/dahlia/wand/e7e8d415b7b125c6aae2b1695ffecaaea392860f/docs/_static/crop.jpg" alt="잘라낸 이미지" width="140" height="242">

크롭은 이미지의 일부 영역을 포기하고 잘라내는 것이다. 따라서 이미지를 더 크게 만드는 데는 쓰지 못할 뿐만 아니라, 작게할 때도 중요한  부분까지 잘라낼 위험이 있다. 가령 이미지의 내용을 알 수 없는 상태에서 일괄적으로 여러 이미지를 크롭한다고 할 때는 보통 이미지의 중요한 내용이 가운데에 분포할 것이라고 가정하고 가장자리만 잘라내게 되는데, 사람 얼굴이 가장자리에 있을 경우 그 사람의 얼굴까지 잘려나가게 되는 식이다. 위에 첨부한 이미지를 예로 들자면, 뒤쪽의 벽이나 의자보다 더 중요하게 여겨지는 의상<del>과 IU의 머리카락</del> 오른쪽 가장자리가 잘려나갔다.

보통 두 가지를 혼합하여 단점을 완화하게 되는데, 원본의 너비/높이 비율을 유지한 채로 확대/축소할 대상 크기에 맞춰 리사이징을 한 뒤, 넘치는 부분만 크롭하는 식이다. 이 때는 넘치는 부분이 한쪽 방향으로만 쏠리지 않게 가운데에 맞추게 된다. 역시나 이미지의 중요한 부분이 가운데에 있을 거라는 거친 가정에 의존한다.

<img src="https://raw.github.com/dahlia/wand/e7e8d415b7b125c6aae2b1695ffecaaea392860f/docs/_static/liquid.jpg" alt="Seam carving으로 축소한 이미지" width="140" height="242">

내가 지금 소개하려는 [씸 카빙][1](seam carving)은 꽤 최근(2007)의 방법으로 content-aware resizing, liquid rescaling 등의 이름으로도 불린다. 이 알고리즘의 아이디어는 꽤 유효한 하나의 가정에서 출발한다. 이미지에서 비슷한 부분이 계속해서 이어지는 부분은 그렇지 않은 부분에 비해 정보가 적을 것이라는, 다시 말해 별로 중요하지 않을 가능성이 높다는 가정이다. 해안선을 뒤로 하고 찍은 인물 사진을 예로 들면, 비록 그 사진에서 인물이 가장자리에 위치하고 있을지라도, 사람의 얼굴이 끝없이 이어지는 해안선보다 대체로 더 중요하다는 뜻이다. 그래서 씸 카빙은 그렇게 비슷하게 이어지는 영역을 덜 중요하다고 여겨서 잘라낼 때 그 부분을 우선적으로 줄여나간다. 반대로 확대를 할 경우에는 그 부분에 비슷한 것들을 채워넣는 식으로 크기를 확대한다.

위에 예로 든 이미지를 보자면, 리사이즈나 크롭과는 달리 <del>IU도 멀쩡하고</del> 꽤 자연스럽게 크기가 축소됐음을 알 수 있다.

개발중인 Wand의 최신 버전에는 씸 카빙 기능이 추가되어 쉽게 사용할 수 있다. 이 기능은 Wand 0.3 버전에 정식으로 포함될 예정이지만, 지금 당장도 Git에서 내려받아 사용해볼 수 있다. 우선 `pip`를 이용해 Wand의 최신 개발 버전을 설치한다.

    $ pip install git+git://github.com/dahlia/wand.git

(Wand는 ImageMagick 바인딩이므로 ImageMagick도 설치해야 한다. 각 OS별 설치법은 [설치 문서][2]를 참고한다.)

그 다음에는 다음과 같이 Wand로 이미지를 열어 [`Image.liquid_rescale()`][3] 메서드를 사용하면 몇줄 코드로 씸 카빙을 쓸 수 있다.

    from urllib2 import urlopen
    from wand.image import Image
    from wand.display import display

    u = urlopen('http://git.io/ogDj-A')
    with Image(file=u) as img:
        img.liquid_rescale(281, 485)
        display(img)

(이 글의 내용은 [공식 문서][4]에도 포함되어 있다. :-)

[1]: http://en.wikipedia.org/wiki/Seam_carving
[2]: http://dahlia.github.com/wand/guide/install.html
[3]: http://dahlia.github.com/wand/wand/image.html#wand.image.Image.liquid_rescale
[4]: http://dahlia.kr/wand/guide/resizecrop.html#seam-carving-also-known-as-content-aware-resizing
