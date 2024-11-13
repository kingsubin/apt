from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_text_image(text, background_color=(255, 255, 255), text_color=(0, 0, 0), 
                     font_path="Arial.ttf", font_size=60, image_size=(1080, 1080)):
    """
    텍스트가 포함된 이미지를 생성하는 함수
    
    Parameters:
    - text: 이미지에 넣을 텍스트
    - background_color: 배경색 (RGB)
    - text_color: 텍스트 색상 (RGB)
    - font_path: 폰트 파일 경로
    - font_size: 폰트 크기
    - image_size: 이미지 크기 (width, height)
    """
    # 새 이미지 생성
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        # 폰트 파일을 찾을 수 없는 경우 기본 폰트 사용
        font = ImageFont.load_default()
    
    # 텍스트 줄바꿈 처리
    # 이미지 너비의 80%를 사용하도록 설정
    max_width = int(image_size[0] * 0.8)
    wrapped_text = textwrap.fill(text, width=int(max_width/font_size))
    
    # 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 텍스트를 이미지 중앙에 배치
    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - text_height) / 2
    
    # 텍스트 그리기
    draw.text((x, y), wrapped_text, font=font, fill=text_color)
    
    return image

# 사용 예시
if __name__ == "__main__":
    sample_text = "Hello!\nThis is a sample text."
    image = create_text_image(
        text=sample_text,
        background_color=(240, 240, 240),  # 연한 회색 배경
        text_color=(33, 33, 33),          # 진한 회색 텍스트
        font_size=80
    )
    image.save("output.png")
