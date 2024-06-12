import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

# 필요한 데이터만 추출
df_expense_needed = df_expense[
    df_expense["과목 및 유형"].str.contains("과목: 일반교과 사교육|국어|영어|수학|사회, 과학")
]
df_grade_needed = df_grade[
    df_grade["과목 및 유형"].str.contains("과목: 일반교과 사교육|국어|영어|수학|사회, 과학")
]

# 열 이름 변경
df_expense_needed = df_expense_needed.rename(columns={"평균": "평균(만원)"})
df_grade_needed = df_grade_needed.rename(columns={"평균": "평균(만원)"})

# 성적 중간 학생들의 일반교과 사교육비 비교
mid_grade_levels = ["31-60%"]

# 필요한 데이터 추출
df_mid_grade = df_grade_needed[["과목 및 유형"] + mid_grade_levels]
df_mid_grade = (
    df_mid_grade.melt(id_vars=["과목 및 유형"], var_name="성적구간", value_name="사교육비(만원)")
    .groupby("과목 및 유형")["사교육비(만원)"]
    .mean()
    .reset_index()
)

# 저소득층 지원을 위한 분석
low_income_levels = ["200만원 미만"]
average_income_level = "500-600만원"

df_low_income = df_expense_needed[["과목 및 유형", "200만원 미만"]].rename(
    columns={"200만원 미만": "사교육비(만원)"}
)
df_average_income = df_expense_needed[["과목 및 유형", "500-600만원"]].rename(
    columns={"500-600만원": "사교육비(만원)"}
)

# 저소득층과 평균 소득 가구의 사교육비 차이 계산
df_income_diff = pd.merge(
    df_low_income, df_average_income, on="과목 및 유형", suffixes=("_저소득층", "_평균")
)
df_income_diff["차이"] = (
    df_income_diff["사교육비(만원)_평균"] - df_income_diff["사교육비(만원)_저소득층"]
)
df_income_diff = df_income_diff.sort_values(by="차이", ascending=False)

# 데이터 병합
df_grade_diff = df_mid_grade.rename(columns={"사교육비(만원)": "차이_성적"})
df_income_diff = df_income_diff.rename(columns={"차이": "차이_소득"})
df_correlation = pd.merge(df_grade_diff, df_income_diff, on="과목 및 유형")

# 상관관계 계산
correlation = df_correlation[["차이_성적", "차이_소득"]].corr()
print("상관관계 분석 결과:")
print(correlation)

# 예측 모델 (간단한 선형 회귀)
X = df_correlation[["차이_성적"]].values.reshape(-1, 1)
y = df_correlation["차이_소득"].values

# 모델 훈련
model = LinearRegression()
model.fit(X, y)

# 예측
y_pred = model.predict(X)

# 예측 결과 출력
df_correlation["예측된 차이"] = y_pred
print("예측된 저소득층 학생과 중간 성적 학생의 사교육비 차이:")
print(df_correlation[["과목 및 유형", "차이_성적", "차이_소득", "예측된 차이"]])

# 성능 평가를 위한 MSE와 R2 계산
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Linear Regression MSE: {mse}, R2: {r2}")

# 결과 시각화
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color="blue", label="Actual")
plt.plot(X, y_pred, color="red", label="Predicted")
plt.title("예측된 저소득층 학생과 중간 성적 학생의 사교육비 차이 예측")
plt.xlabel("성적이 중간인 학생들이 투자한 사교육비 차이 (만원)")
plt.ylabel("소득에 따른 사교육비 차이 (만원)")
plt.legend()
plt.tight_layout()
plt.show()

# 페어플롯 그래프 출력
sns.pairplot(df_correlation, height=2)
plt.show()
