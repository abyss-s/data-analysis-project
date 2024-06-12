import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")

# 마이너스 기호가 깨지는 문제 해결
plt.rcParams["axes.unicode_minus"] = False

# 데이터 로드
file_path_expense = "data/가구의_월평균_소득별_학생_1인당_월평균_사교육비_20240609023723.csv"
try:
    df_income_expense = pd.read_csv(file_path_expense, encoding="utf-8")
except UnicodeDecodeError:
    df_income_expense = pd.read_csv(file_path_expense, encoding="latin1")

# 열 이름 변경
df_income_expense.columns = [
    "과목 및 유형",
    "평균",
    "200만원 미만",
    "200-300만원",
    "300-400만원",
    "400-500만원",
    "500-600만원",
    "600-700만원",
    "700-800만원",
    "800만원 이상",
    "여분",
]

# '사교육비' 행 선택
df_income_expense = df_income_expense[df_income_expense["과목 및 유형"] == "사교육비"]

# '여분' 열 제거
df_income_expense = df_income_expense.drop(columns=["여분"])

# 데이터 변환 (소득 구간을 행으로 변환)
df_income_expense = df_income_expense.melt(
    id_vars=["과목 및 유형"], var_name="소득수준", value_name="월평균 사교육비"
)

# '월평균 사교육비' 컬럼을 숫자로 변환
df_income_expense["월평균 사교육비"] = df_income_expense["월평균 사교육비"].astype(float)

# 데이터 확인
print(df_income_expense.head())

# 소득 구간별 학생 1인당 월평균 사교육비 시각화
plt.figure(figsize=(10, 8))
sns.barplot(x="소득수준", y="월평균 사교육비", data=df_income_expense)
plt.title("소득수준에 따른 학생 1인당 월평균 사교육비")
plt.xlabel("소득수준")
plt.ylabel("월평균 사교육비 (만원)")
plt.xticks(rotation=0)  # x축 레이블을 가로로 설정
plt.show()

# 데이터 로드
file_path_grade = "data/학생_성적_구간별_학생_1인당_월평균_사교육비_20240609023827.csv"
try:
    df_grade_expense = pd.read_csv(file_path_grade, encoding="utf-8")
except UnicodeDecodeError:
    df_grade_expense = pd.read_csv(file_path_grade, encoding="latin1")

# 열 이름 변경
df_grade_expense.columns = [
    "과목 및 유형",
    "평균",
    "20% 이하",
    "21-40%",
    "41-60%",
    "61-80%",
    "81-100%",
]

# '사교육비' 행 선택
df_grade_expense = df_grade_expense[df_grade_expense["과목 및 유형"] == "사교육비"]

# 데이터 변환 (성적 구간을 행으로 변환)
df_grade_expense = df_grade_expense.melt(
    id_vars=["과목 및 유형"], var_name="성적 구간", value_name="월평균 사교육비"
)

# '월평균 사교육비' 컬럼을 숫자로 변환
df_grade_expense["월평균 사교육비"] = df_grade_expense["월평균 사교육비"].astype(float)

# 데이터 확인
print(df_grade_expense.head())

# 성적 구간별 학생 1인당 월평균 사교육비 시각화
plt.figure(figsize=(10, 8))
sns.barplot(x="성적 구간", y="월평균 사교육비", data=df_grade_expense)
plt.title("성적 구간에 따른 학생 1인당 월평균 사교육비")
plt.xlabel("성적 구간")
plt.ylabel("월평균 사교육비 (만원)")
plt.xticks(rotation=0)  # x축 레이블을 가로로 설정
plt.show()

# '평균' 행 제거
df_income_expense = df_income_expense[df_income_expense["소득수준"] != "평균"]
df_grade_expense = df_grade_expense[df_grade_expense["성적 구간"] != "평균"]

# 상관관계 분석을 위해 데이터 병합
df_income_expense["소득수준_월평균 사교육비"] = df_income_expense["월평균 사교육비"]
df_grade_expense["성적구간_월평균 사교육비"] = df_grade_expense["월평균 사교육비"]

# 필요 열만 추출
df_income_expense = df_income_expense[["소득수준_월평균 사교육비"]]
df_grade_expense = df_grade_expense[["성적구간_월평균 사교육비"]]

# 데이터프레임 병합
df_merged = pd.concat(
    [
        df_income_expense["소득수준_월평균 사교육비"].reset_index(drop=True),
        df_grade_expense["성적구간_월평균 사교육비"].reset_index(drop=True),
    ],
    axis=1,
)
df_pairplot = pd.concat([df_income_expense, df_grade_expense], axis=1)


# 산점도 시각화
plt.figure(figsize=(6, 6))
sns.scatterplot(x="소득수준_월평균 사교육비", y="성적구간_월평균 사교육비", data=df_merged)
plt.title("소득수준과 성적 구간 간의 산점도")
plt.xlabel("소득수준 월평균 사교육비 (만원)")
plt.ylabel("성적구간 월평균 사교육비 (만원)")
plt.show()

# 선형 회귀선 포함한 산점도 시각화
plt.figure(figsize=(6, 6))
sns.regplot(
    x="소득수준_월평균 사교육비",
    y="성적구간_월평균 사교육비",
    data=df_merged,
    ci=None,
    scatter_kws={"s": 50},
)
plt.title("소득수준과 성적 구간 간의 선형 회귀선 포함 산점도")
plt.xlabel("소득수준 월평균 사교육비 (만원)")
plt.ylabel("성적구간 월평균 사교육비 (만원)")
plt.show()
