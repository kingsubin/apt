import asyncio
from PublicDataReader import TransactionPrice
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd

DATABASE_URL = "mysql+aiomysql://admin:0PY34xRY4YtqLGYowgqa@dev.db.yuppie.business/tax_platform"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# encoding key
SERVICE_KEY = "d4q07XC5UDj5LfyXT0KsuIHzGJKwedbZa%2FP5rrzHagOC6niAictIEyRQ4lkKUw6w8pHQx1CBekboTGRnBoSN2Q%3D%3D"
api = TransactionPrice(SERVICE_KEY)
columns = [
    '법정동시군구코드', '법정동읍면동코드', '법정동지번코드', '법정동본번코드', '법정동부번코드', '도로명',
    '도로명시군구코드', '도로명코드', '도로명일련번호코드', '도로명지상지하코드', '도로명건물본번호코드',
    '도로명건물부번호코드', '법정동', '단지명', '지번', '전용면적', '계약년도', '계약월', '계약일', '거래금액',
    '층', '건축년도', '단지일련번호', '해제여부', '해제사유발생일', '거래유형', '중개사소재지', '등기일자',
    '아파트동명', '매도자', '매수자', '토지임대부아파트여부'
]
busan_sigungu_codes = [
    "26110", # 중구
    "26140", # 서구
    "26170", # 동구
    "26200", # 영도구
    "26230", # 부산진구
    "26260", # 동래구
    "26290", # 남구
    "26320", # 북구
    "26350", # 해운대구
    "26380", # 사하구
    "26410", # 금정구
    "26440", # 강서구
    "26470", # 연제구
    "26500", # 수영구
    "26530", # 사상구
    "26710", # 기장군
]
years = [
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
]

def get_trade_data(sigungu_code, start_year_month, end_year_month):
    print(f"----- 아파트 매매 실거래가 조회 시작 -----")
    print(f"sigungu_code: {sigungu_code}, start_year_month: {start_year_month}, end_year_month: {end_year_month}")

    df = api.get_data(
        property_type="아파트",
        trade_type="매매",
        sigungu_code=sigungu_code,
        start_year_month=start_year_month,
        end_year_month=end_year_month,
    )   

    df['거래금액'] = df['거래금액'].apply(lambda x: int(str(x).replace(',', '')) if pd.notna(x) else None)
    df['전용면적'] = df['전용면적'].apply(lambda x: float(x) if pd.notna(x) else None)
    df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None})

    print(f"df.shape: {df.shape}")
    print(f"----- 아파트 매매 실거래가 조회 완료 -----")
    return df


async def insert_trade_data(df):
    print(f"----- 아파트 매매 실거래가 데이터 저장 시작 -----")

    if df.empty:
        print("데이터가 없습니다.")
        return
    
    # DataFrame을 딕셔너리 리스트로 변환
    records = df.to_dict('records')
    
    # SQL 쿼리 생성
    insert_query = text("""
    INSERT INTO apartment_trade_history (
        법정동시군구코드, 법정동읍면동코드, 법정동지번코드, 법정동본번코드, 법정동부번코드, 
        도로명, 도로명시군구코드, 도로명코드, 도로명일련번호코드, 도로명지상지하코드, 
        도로명건물본번호코드, 도로명건물부번호코드, 법정동, 단지명, 지번, 전용면적, 
        계약년도, 계약월, 계약일, 거래금액, 층, 건축년도, 단지일련번호, 해제여부, 
        해제사유발생일, 거래유형, 중개사소재지, 등기일자, 아파트동명, 매도자, 매수자, 
        토지임대부아파트여부
    ) VALUES (
        :법정동시군구코드, :법정동읍면동코드, :법정동지번코드, :법정동본번코드, :법정동부번코드,
        :도로명, :도로명시군구코드, :도로명코드, :도로명일련번호코드, :도로명지상지하코드,
        :도로명건물본번호코드, :도로명건물부번호코드, :법정동, :단지명, :지번, :전용면적,
        :계약년도, :계약월, :계약일, :거래금액, :층, :건축년도, :단지일련번호, :해제여부,
        :해제사유발생일, :거래유형, :중개사소재지, :등기일자, :아파트동명, :매도자, :매수자,
        :토지임대부아파트여부
    )
    """)
    
    try:
        async with async_session() as session:
            async with session.begin():
                await session.execute(insert_query, records)
                await session.commit()
    except Exception as e:
        print(f"데이터 입력 중 오류가 발생했습니다: {str(e)}")
        raise
    finally:
        await engine.dispose()
    
    print(f"{len(records)}개의 거래 데이터가 성공적으로 입력되었습니다.")
    print(f"----- 아파트 매매 실거래가 데이터 저장 완료 -----")

async def main():
    for sigungu_code in busan_sigungu_codes:
        for year in years:  
            df = get_trade_data(sigungu_code, year + "01", year + "12")
            
            # insert trade data
            await insert_trade_data(df)

    

if __name__ == "__main__":
    asyncio.run(main())
