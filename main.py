from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# fps수치 제거
window.fps_counter.enabled = False
# exit button제거
window.exit_button.visible = False


# sound effect
punch = Audio('assets/punch.wav', autoplay = False) 

# block texture로드, 저장
blocks = [
    load_texture('assets/grass.png'),   # 0
    load_texture('assets/grass.png'),   # 1
    load_texture('assets/stone.png'),   # 2
    load_texture('assets/gold.png'),    # 3
    load_texture('assets/lava.png'),    # 4
]
 # 키보드 1, 2, 3, 4누르면 텍스처 바뀌게 설정
block_id = 1

# 키보드 입력받는 함수 만들기
def input(key):
    # block_id를 전역변수로 지정
    global block_id, hand
    # 숫자 입력하면
    if key.isdigit():
        # block_id에 입력받은 숫자를 int로 변경해서 넣음
        block_id = int(key)

        # 블록이 4개밖에 없으니 예외처리 
        if block_id >= len(blocks):
            block_id = len(blocks) - 1

        hand.texture = blocks[block_id]


# 하늘 만들기
sky = Entity(
    parent = scene,
    # model = 구형 모양 
    model = 'sphere',
    # google search : sky sphere texture
    # 이미지 다운로드 후 불러오기
    texture = load_texture('assets/sky.jpg'),
    scale = 500,
    # sky texture를 구의 양면에 적용하기
    double_sided = True
)

# 손추가
hand = Entity(
    parent = camera.ui,
    model = 'assets/block',
    texture = blocks[block_id],
    scale = 0.2,
    # 들고있는 블록 회전시켜 입체감 주기
    rotation = Vec3(-10, -10, 10),
    # 손의 위치는 화면 오른쪽 아래
    position = Vec2(0.6, -0.6)
)

# 클릭할 때 마다 손 움직이게 설정
def update():
    # 왼 or 오 마우스 클릭
    if held_keys['left mouse'] or held_keys['right mouse']:
        # 마우스 누를 시 재생
        punch.play()
        # 손의 위치 변경
        hand.position = Vec2(0.4, -0.5)
    # 버튼 안누르면 제자리로
    else:
        hand.position = Vec2(0.6, -0.6)


# 블록(Voxel) 객체 생성
class Voxel(Button):
    # position = 기본 블록 위치(x, y, z)
    # texture = 기본 블록 텍스처
    def __init__(self, position = (0, 0, 0), texture = 'assets/grass.png'):
        super().__init__(
            parent = scene,
            position = position,
            # 기본 블록 모델(정육면체)  
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            # 블록 색상지정
            # hsv컬러스페이스로 표현_흰 블록, 명도를 0.9-1.0의 random한 값으로
            color = color.color(0, 0, random.uniform(0.9, 1.0)),
            # 블록 크기 지정
            scale = 0.5
        )

    # 블록을 생성하고 파괴하는 코드 작성
    def input(self, key):
        # 마우스 블록위에 올리고
        if self.hovered:
            # 왼쪽 마우스 클릭
            if key == 'left mouse down':
                # 블록 하나 생성
                # 생성된 블록은 마우스로 클릭한 부분에 위치
                # 새 블럭 추가할 때, 선택된 블록 텍스처로 생성
                Voxel(position = self.position + mouse.normal, texture = blocks[block_id])
            # 오른쪽 마우스 클릭
            elif key == 'right mouse down':
                # 클릭한 블록 파괴
                destroy(self)




# 바닥에 블록 깔아 발로 딛고 설 수 있는 공간 만들기
for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x, 0, z))

# 플레이어(1인칭 컨트롤러)추가
player = FirstPersonController()


app.run()