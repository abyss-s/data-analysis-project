import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")
# 마이너스 기호가 깨지는 문제 해결
plt.rcParams["axes.unicode_minus"] = False

# 파일 경로 설정
file_path_expense = (
    "data/가구의_월평균_소득별_학생_1인당_월평균_사교육비_20240609023723.csv"
)

# 데이터 로드
df_expense = pd.read_csv(file_path_expense, encoding="utf-8", header=1)

# 열 이름 변경
df_expense.columns = [
    "과목 및 유형",
    "평균",
    "300만원 미만",
    "200만원 미만",
    "200-300만원",
    "300-400만원",
    "400-500만원",
    "500-600만원",
    "600-700만원",
    "700-800만원",
    "800만원 이상",
]

# 필요한 데이터만 추출
df_expense_needed = df_expense[
    df_expense["과목 및 유형"].str.contains(
        "과목: 일반교과 사교육|국어|영어|수학|사회, 과학"
    )
]

# 열 이름 변경
df_expense_needed = df_expense_needed.rename(columns={"평균": "평균(만원)"})

# 200만원 미만의 저소득층과 평균 소득 가구의 사교육비 비교
low_income_level = "200만원 미만"
average_income_level = "평균(만원)"

# 필요한 데이터 추출
df_low_income = df_expense_needed[["과목 및 유형", low_income_level]].rename(
    columns={low_income_level: "저소득층 사교육비(만원)"}
)
df_average_income = df_expense_needed[["과목 및 유형", average_income_level]].rename(
    columns={average_income_level: "평균 사교육비(만원)"}
)

# 저소득층과 평균 소득 가구의 데이터 병합
df_support_needed = pd.merge(df_low_income, df_average_income, on="과목 및 유형")
df_support_needed["차이"] = (
    df_support_needed["평균 사교육비(만원)"]
    - df_support_needed["저소득층 사교육비(만원)"]
)
df_support_needed = df_support_needed.sort_values(by="차이", ascending=False)

# 데이터 시각화
plt.figure(figsize=(14, 8))
sns.barplot(data=df_support_needed, x="과목 및 유형", y="차이")
plt.title("저소득층 학생들이 가장 투자하지 못하는 과목")
plt.xlabel("과목 및 유형")
plt.ylabel("사교육비 차이 (만원)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 결과 출력
print("저소득층 학생들이 가장 투자하지 못하는 과목:")
print(df_support_needed[["과목 및 유형", "차이"]])
