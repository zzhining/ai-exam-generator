# 🤖 AI 시험문제 출제 봇

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-exam-generator-2pg.streamlit.app/)

생성형 AI를 활용한 자동 시험문제 생성 도구입니다. 교사, 교육자, 학습자가 쉽고 빠르게 다양한 유형의 시험문제를 생성하고 관리할 수 있습니다.

## 🚀 라이브 데모

**[➡️ AI 시험문제 출제 봇 사용해보기](https://ai-exam-generator-2pg.streamlit.app/)**

## ✨ 주요 기능

### 🧠 AI 자동 문제 생성
- **다중 AI 지원**: OpenAI GPT, Anthropic Claude, Google Gemini
- **다양한 문제 유형**: 객관식, 주관식, O/X 문제
- **난이도 조절**: 쉬움, 보통, 어려움 선택 가능
- **맞춤형 생성**: 과목, 단원, 키워드 기반 문제 생성

### ✏️ 수동 문제 출제
- 직접 문제 작성 및 편집
- 선택지 및 정답 설정
- 해설 추가 기능

### 🗂️ 문제 은행 관리
- 생성된 문제 저장 및 관리
- 과목, 유형, 난이도별 필터링
- 문제 검색 및 편집/삭제 기능

### 📋 시험지 생성
- 저장된 문제로 시험지 구성
- 랜덤 선택 또는 수동 선택
- 시험지 미리보기 및 정답지 제공

### 💾 데이터 관리
- JSON 형태로 문제 데이터 저장/불러오기
- 문제 통계 및 분석
- 데이터 백업 및 복원

## 🎯 사용 대상

- **교사 및 교육자**: 수업용 시험문제 제작
- **학생**: 자습용 문제 생성 및 연습
- **교육 기관**: 평가 도구 개발
- **온라인 학습 플랫폼**: 콘텐츠 제작

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI APIs**: 
  - OpenAI GPT-3.5/4
  - Anthropic Claude
  - Google Gemini
- **Language**: Python 3.9+
- **Deployment**: Streamlit Community Cloud

## 📦 로컬 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/ai-exam-generator.git
cd ai-exam-generator
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 앱 실행
```bash
streamlit run test_creator.py
```

앱이 `http://localhost:8501`에서 실행됩니다.

## 🔑 API 키 설정

AI 문제 생성 기능을 사용하려면 다음 중 하나 이상의 API 키가 필요합니다:

### OpenAI API
1. [OpenAI Platform](https://platform.openai.com/api-keys)에서 계정 생성
2. API 키 발급
3. 앱 사이드바에서 API 키 입력

### Anthropic Claude API
1. [Anthropic Console](https://console.anthropic.com/)에서 계정 생성
2. API 키 발급
3. 앱 사이드바에서 API 키 입력

### Google Gemini API
1. [Google AI Studio](https://ai.google.dev/)에서 계정 생성
2. API 키 발급
3. 앱 사이드바에서 API 키 입력

> ⚠️ **보안 주의**: API 키는 개인정보이므로 타인과 공유하지 마세요. 앱에서는 세션 동안만 저장됩니다.

## 📖 사용 방법

### 1️⃣ AI 문제 생성
1. 사이드바에서 AI 제공업체 선택 및 API 키 입력
2. "AI 문제 생성" 메뉴 선택
3. 과목명, 문제 유형, 난이도, 문항 수 설정
4. 추가 요구사항 입력 (선택사항)
5. "AI 문제 생성" 버튼 클릭
6. 생성된 문제 미리보기 후 저장

### 2️⃣ 수동 문제 출제
1. "수동 문제 출제" 메뉴 선택
2. 문제 정보 입력 (유형, 과목, 난이도)
3. 문제 내용 및 정답 작성
4. 해설 추가 (선택사항)
5. "문제 저장" 버튼 클릭

### 3️⃣ 시험지 생성
1. "시험지 생성" 메뉴 선택
2. 시험 정보 입력 (제목, 과목, 시간)
3. 문제 선택 방법 설정 (랜덤/수동)
4. "시험지 생성" 버튼 클릭
5. 미리보기 확인 및 정답지 다운로드

## 📁 프로젝트 구조

```
ai-exam-generator/
├── test_creator.py      # 메인 애플리케이션
├── requirements.txt     # 의존성 패키지 목록
└── README.md           # 프로젝트 문서
```

## 🔧 주요 의존성

```txt
streamlit==1.29.0
openai==1.3.5
anthropic==0.8.1
requests==2.31.0
```

## 🌟 기능 예시

### AI 생성 문제 예시
**과목**: 고등학교 수학  
**유형**: 객관식  
**난이도**: 보통

**문제**: 함수 f(x) = x² - 4x + 3의 최솟값은?
1. ① -1
2. ② 0  
3. ③ 1
4. ④ 3
5. ⑤ 5

**정답**: ① -1  
**해설**: f(x) = (x-2)² - 1이므로 x=2일 때 최솟값 -1을 가집니다.

## 🚀 배포

이 앱은 Streamlit Community Cloud에서 호스팅됩니다.

## 📞 문의 및 지원

- **이슈 리포트**: [GitHub Issues](https://github.com/zzhining/ai-exam-generator/issues)
- **기능 요청**: [GitHub Discussions](https://github.com/zzhining/ai-exam-generator/discussions)

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## ⭐ 지원하기

이 프로젝트가 도움이 되었다면 ⭐을 눌러주세요!

---

**Made with ❤️ by 강쯔닝**

[![GitHub stars](https://img.shields.io/github/stars/zzhining/ai-exam-generator.svg?style=social&label=Star)](https://github.com/YOUR_USERNAME/ai-exam-generator)
[![GitHub forks](https://img.shields.io/github/forks/zzhining/ai-exam-generator.svg?style=social&label=Fork)](https://github.com/YOUR_USERNAME/ai-exam-generator/fork)
