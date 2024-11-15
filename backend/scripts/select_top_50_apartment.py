from PIL import Image, ImageDraw, ImageFont
import os
import asyncio
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
from decimal import Decimal


DATABASE_URL = "mysql+aiomysql://admin:0PY34xRY4YtqLGYowgqa@dev.db.yuppie.business/tax_platform"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_top_50_apartment():
    async with async_session() as session:
        async with session.begin():
            # 최근 5년간 거래횟수 상위 50개 아파트 조회
            result = await session.execute(text("""
                SELECT *, COUNT(*) AS 거래횟수
                FROM apartment_trade_history
                WHERE 계약년도 BETWEEN 2019 AND 2024
                GROUP BY 단지일련번호
                ORDER BY 거래횟수 DESC
                LIMIT 50
            """))
            
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

async def this_month_trade_history():
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    contract_year = today.split('-')[0]
    contract_month = today.split('-')[1]

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text("""
                SELECT * FROM apartment_trade_history 
                WHERE 계약년도 = :계약년도 AND 계약월 = :계약월
            """), {
                '계약년도': contract_year,
                '계약월': contract_month
            })
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

async def preprocess_df(df):
    dong_code_df = pd.read_csv('src/data/법정동코드.csv')

    road_addresses = []
    formatted_prices = []
    
    for _, row in df.iterrows():
        # 1. 도로명주소 생성
        sigungu = dong_code_df[dong_code_df['법정동시군구코드'] == int(row['법정동시군구코드'])]['시군구명'].iloc[0]
        dong = dong_code_df[
            (dong_code_df['법정동시군구코드'] == int(row['법정동시군구코드'])) & 
            (dong_code_df['법정동읍면동코드'] == int(row['법정동읍면동코드']))
        ]['읍면동명'].iloc[0]

        main_num = str(int(row['도로명건물본번호코드']))  # 앞쪽 0 제거
        road_address = f"부산광역시 {sigungu} {dong} {row['도로명']} {main_num}"
        
        if pd.notna(row['도로명건물부번호코드']) and str(row['도로명건물부번호코드']) != '0000':
            sub_num = str(int(row['도로명건물부번호코드']))  # 앞쪽 0 제거
            if sub_num != '0':
                road_address += f"-{sub_num}"
        
        road_addresses.append(road_address)
        
        # 2. 거래금액 포맷팅
        price = int(str(row['거래금액']).replace(',', ''))
        억 = price // 10000
        만 = price % 10000
        price_text = f"{억}억"
        if 만 > 0:
            price_text += f" {만:,}만"
        price_text += "원"
        
        formatted_prices.append(price_text)
    
    # 새로운 컬럼들 한번에 추가
    df['도로명주소'] = road_addresses
    df['거래금액'] = formatted_prices

    return df

async def generate_thumbnail(df):
    # 색상 정의
    TOSS_BLUE = "#0064FF"  # 토스 메인 파란색
    WHITE = "#FFFFFF"      # 흰색
    LIGHT_WHITE = "#FFFFFF99"  # 반투명 흰색

    # 폰트 설정 (맥OS 기준)
    font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    title_font = ImageFont.truetype(font_path, 72)  # 단지명 크기 증가
    large_font = ImageFont.truetype(font_path, 48)  # 가격
    medium_font = ImageFont.truetype(font_path, 36)  # 주소
    small_font = ImageFont.truetype(font_path, 32)  # 기타 정보
    
    for _, row in df.iterrows():
        # 이미지 생성
        img = Image.new('RGB', (1080, 1080), color=TOSS_BLUE)
        draw = ImageDraw.Draw(img)
        
        # 내용 작성
        # 단지명 (중앙 정렬)
        y = 180
        text = row['단지명']
        text_width = title_font.getlength(text)
        x = (1080 - text_width) / 2
        draw.text((x, y), text, font=title_font, fill=WHITE)
        
        # 도로명주소 (중앙 정렬)
        y += 120
        text = row['도로명주소']
        text_width = medium_font.getlength(text)
        x = (1080 - text_width) / 2
        draw.text((x, y), text, font=medium_font, fill=LIGHT_WHITE)
        
        # 거래금액 (중앙 정렬)
        y += 120
        label = "거래금액"
        label_width = medium_font.getlength(label)
        x = (1080 - label_width) / 2
        draw.text((x, y), label, font=medium_font, fill=LIGHT_WHITE)
        
        y += 50
        price_text = row['거래금액']
        price_width = large_font.getlength(price_text)
        x = (1080 - price_width) / 2
        draw.text((x, y), price_text, font=large_font, fill=WHITE)
        
        # 기타 정보 (중앙 정렬)
        y += 160
        info_list = [
            f"전용면적 {float(row['전용면적']) / 3.3:.2f}평 ({Decimal(row['전용면적']).normalize()}㎡)",  # 전용면적을 평으로 변환
            f"{row['층']}층",
            f"{row['계약년도']}년 {row['계약월']}월 {row['계약일']}일 거래"
        ]
        
        for info in info_list:
            text_width = small_font.getlength(info)
            x = (1080 - text_width) / 2
            draw.text((x, y), info, font=small_font, fill=LIGHT_WHITE)
            y += 60
        
        # 이미지 저장
        os.makedirs('thumbnails', exist_ok=True)
        filename = f"thumbnails/{row['단지일련번호']}_{row['계약년도']}{row['계약월']}{row['계약일']}.png"
        img.save(filename, 'PNG', quality=95)
        print(f"썸네일 생성 완료: {filename}")

async def main():
    top_50_apartment_df = await get_top_50_apartment()
    top_50_apartment_list = top_50_apartment_df['단지일련번호'].tolist()

    # 한달 거래 데이터 중에서 top 50 아파트에 속하는 거래가 있는지?
    this_month_df = await this_month_trade_history()
    this_month_df = this_month_df[this_month_df['단지일련번호'].isin(top_50_apartment_list)]
    
    # temp
    this_month_df = this_month_df[:5]

    this_month_df = await preprocess_df(this_month_df)

    await generate_thumbnail(this_month_df)

    await engine.dispose()
    

if __name__ == "__main__":
    asyncio.run(main())