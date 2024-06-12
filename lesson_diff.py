import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")

# 마이너스 기호가 깨지는 문제 해결
plt.rcParams["axes.unicode_minus"] = False

# 파일 경로 설정
file_path_expense = "data/가구의_월평균_소득별_학생_1인당_월평균_사교육비_20240609023723.csv"
file_path_grade = "data/학생_성적_구간별_학생_1인당_월평균_사교육비_20240609023827.csv"

# 데이터 로드
df_expense = pd.read_csv(file_path_expense, encoding="utf-8", header=1)
df_grade = pd.read_csv(file_path_grade, encoding="utf-8", header=1)

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
df_grade.columns = [
    "과목 및 유형",
    "평균",
    "상위10% 이내",
    "11-30%",
    "31-60%",
    "61-80%",
    "81-100%",
]

# 데이터 처리(행 제거)
df_expense = df_expense.drop(index=0)
df_grade = df_grade.drop(index=0)

# '과목 및 유형' 열에서 유형과 과목 분리
df_expense[["유형", "과목"]] = df_expense["과목 및 유형"].str.split(": ", expand=True)
df_expense = df_expense.drop(columns=["과목 및 유형"])

df_grade[["유형", "과목"]] = df_grade["과목 및 유형"].str.split(": ", expand=True)
df_grade = df_grade.drop(columns=["과목 및 유형"])

# '유형'과 '과목'을 기준으로 그룹화하여 평균 사교육비 계산
df_expense_melted = df_expense.melt(
    id_vars=["유형", "과목"], var_name="소득수준", value_name="월평균 사교육비"
)
df_expense_melted = df_expense_melted[
    df_expense_melted["소득수준"] != "평균"
]  # '평균' 행 제거

# 숫자 변환
df_expense_melted["월평균 사교육비"] = (
    df_expense_melted["월평균 사교육비"].replace("-", "0").astype(float)
)

# 저소득층 지원을 위한 분석
low_income_levels = ["200만원 미만"]
df_low_income = df_expense_melted[df_expense_melted["소득수준"].isin(low_income_levels)]

# 평균 소득 가구의 데이터 추출
average_income_level = "500-600만원"
df_average_income = df_expense_melted[
    df_expense_melted["소득수준"] == average_income_level
]

# 저소득층 학생들의 과목별 평균 사교육비 계산
df_low_income_grouped = (
    df_low_income.groupby(["유형", "과목"])["월평균 사교육비"].mean().reset_index()
)

# 평균 소득 가구 학생들의 과목별 평균 사교육비 계산
df_average_income_grouped = (
    df_average_income.groupby(["유형", "과목"])["월평균 사교육비"].mean().reset_index()
)

# 저소득층 학생들이 가장 투자하지 못하는 사교육비 유형 찾기
df_support_needed = pd.merge(
    df_low_income_grouped,
    df_average_income_grouped,
    on=["유형", "과목"],
    suffixes=("_저소득층", "_평균"),
)
df_support_needed["차이"] = (
    df_support_needed["월평균 사교육비_평균"]
    - df_support_needed["월평균 사교육비_저소득층"]
)

# 중복 제거
df_support_needed = df_support_needed.drop_duplicates(subset=["과목", "차이"]).sort_values(by="차이", ascending=False)

# 데이터 시각화
plt.figure(figsize=(10, 8))
sns.barplot(data=df_support_needed, x="과목", y="차이", hue="유형")
plt.title("저소득층 학생들이 가장 투자하지 못하는 사교육비 유형")
plt.xlabel("과목")
plt.ylabel("사교육비 차이 (만원)")
plt.xticks(rotation=45)
plt.legend(title="유형", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

# 결과 출력
print("저소득층 학생들이 가장 투자하지 못하는 사교육비 유형:")
print(df_support_needed[["유형", "과목", "차이"]])
