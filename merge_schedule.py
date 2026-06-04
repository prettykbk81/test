# -*- coding: utf-8 -*-
import pandas as pd

# 각 홈쇼핑사 데이터 로드
homeshow_files = {
    '홈앤쇼핑': '홈앤쇼핑_편성표_6월4일.csv',
    'GS홈쇼핑': 'GS홈쇼핑_편성표_6월4일.csv',
    'CJ온스타일': 'CJ온스타일_편성표_6월4일.csv',
    '롯데홈쇼핑': '롯데홈쇼핑_편성표_6월4일.csv',
    '현대홈쇼핑': '현대홈쇼핑_편성표_6월4일.csv',
}

# 모든 데이터 통합
combined_data = []

for homeshow_name, filename in homeshow_files.items():
    df = pd.read_csv(filename)
    df['홈쇼핑사'] = homeshow_name
    combined_data.append(df)

# 합치기
combined_df = pd.concat(combined_data, ignore_index=True)

# 컬럼 순서 조정
combined_df = combined_df[['홈쇼핑사', '시간', '상품명', '출연진', '예상가격', '카테고리']]

# CSV로 저장
combined_df.to_csv('편성표_통합_6월4일.csv', index=False, encoding='utf-8-sig')

print("통합 완료!")
print(f"총 {len(combined_df)}개 프로그램")
print("\n홈쇼핑사별 프로그램 수:")
print(combined_df['홈쇼핑사'].value_counts().sort_index())
