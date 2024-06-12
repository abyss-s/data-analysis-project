```mermaid
flowchart TD
    A[문제 인식] --> B[주제 설정]
    B --> C[데이터 수집]
    C --> D[교과목별 사교육비 지출 격차 분석] -->|lesson_diff.py| E[유형별 사교육비 지출 격차 분석]
    E -->|subject_diff.py| F[지역별 사교육비 지출 격차 분석]
    F -->|region_and_ebs.py| G[성적 구간별 사교육비 현황 분석]
    G -->|grade_diff.py| H[상관관계 분석]
    H -->|correlation.py| I[선형 회귀 모델 구축]
    I -->|predict_model.py| J[저소득층 지원 교육비 예측 및 평가]
    J -->|predict_and_visualize.py| K[결론 및 참여후기]
