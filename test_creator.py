import streamlit as st
import json
import random
import requests
from datetime import datetime
import openai
import anthropic
from typing import List, Dict

# 페이지 설정
st.set_page_config(
    page_title="AI 시험문제 출제 봇",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_exam' not in st.session_state:
    st.session_state.current_exam = None
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {}

def create_question(question_type, subject, difficulty, question_text, options=None, answer=None, explanation=None):
    """문제 생성 함수"""
    question = {
        'id': len(st.session_state.questions) + 1,
        'type': question_type,
        'subject': subject,
        'difficulty': difficulty,
        'question': question_text,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if question_type == '객관식':
        question['options'] = options
        question['correct_answer'] = answer
    elif question_type == '주관식':
        question['answer'] = answer
    elif question_type == 'O/X':
        question['correct_answer'] = answer
    
    if explanation:
        question['explanation'] = explanation
    
    return question

def generate_with_openai(api_key, prompt):
    """OpenAI API로 문제 생성"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 전문적인 시험 문제 출제자입니다. 요청된 형식에 맞춰 정확하고 교육적인 문제를 생성해주세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API 오류: {str(e)}")
        return None

def generate_with_anthropic(api_key, prompt):
    """Anthropic Claude API로 문제 생성"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Anthropic API 오류: {str(e)}")
        return None

def generate_with_gemini(api_key, prompt):
    """Google Gemini API로 문제 생성"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        st.error(f"Gemini API 오류: {str(e)}")
        return None

def create_prompt(question_type, subject, difficulty, num_questions, additional_info=""):
    """프롬프트 생성"""
    base_prompt = f"""
다음 조건에 맞는 {question_type} 문제 {num_questions}개를 생성해주세요:

- 과목: {subject}
- 난이도: {difficulty}
- 추가 요구사항: {additional_info}

각 문제는 다음 JSON 형식으로 작성해주세요:
"""
    
    if question_type == "객관식":
        format_example = """
{
  "question": "문제 내용",
  "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
  "correct_answer": "①",
  "explanation": "해설 내용"
}
"""
    elif question_type == "O/X":
        format_example = """
{
  "question": "문제 내용",
  "correct_answer": "O",
  "explanation": "해설 내용"
}
"""
    else:  # 주관식
        format_example = """
{
  "question": "문제 내용",
  "answer": "정답 내용",
  "explanation": "해설 내용"
}
"""
    
    return base_prompt + format_example + f"\n\n{num_questions}개의 문제를 JSON 배열 형태로 반환해주세요."

def parse_ai_response(response_text, question_type):
    """AI 응답 파싱"""
    try:
        # JSON 추출 시도
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_text = response_text[start_idx:end_idx]
        else:
            # 단일 객체인 경우
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_text = f"[{response_text[start_idx:end_idx]}]"
        
        questions_data = json.loads(json_text)
        return questions_data
    except Exception as e:
        st.error(f"응답 파싱 오류: {str(e)}")
        return None

def main():
    st.title("🤖 AI 시험문제 출제 봇")
    st.markdown("생성형 AI를 활용한 자동 시험문제 생성 도구")
    st.markdown("---")
    
    # 사이드바 메뉴
    with st.sidebar:
        st.header("메뉴")
        menu = st.selectbox(
            "기능 선택",
            ["AI 문제 생성", "수동 문제 출제", "문제 은행", "시험지 생성", "설정"]
        )
        
        st.markdown("---")
        
        # API 키 설정
        st.subheader("🔑 API 키 설정")
        
        ai_provider = st.selectbox(
            "AI 제공업체",
            ["OpenAI (GPT)", "Anthropic (Claude)", "Google (Gemini)"]
        )
        
        api_key = st.text_input(
            f"{ai_provider} API 키",
            type="password",
            help="API 키는 세션 동안만 저장됩니다."
        )
        
        if api_key:
            st.session_state.api_keys[ai_provider] = api_key
            st.success("API 키가 설정되었습니다!")
    
    # AI 문제 생성 탭
    if menu == "AI 문제 생성":
        st.header("🧠 AI 자동 문제 생성")
        
        # API 키 확인
        if ai_provider not in st.session_state.api_keys:
            st.warning("먼저 사이드바에서 API 키를 설정해주세요.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input(
                "과목명",
                placeholder="예: 고등학교 수학, 중학교 영어, 한국사"
            )
            
            question_type = st.selectbox(
                "문제 유형",
                ["객관식", "주관식", "O/X"]
            )
            
            difficulty = st.select_slider(
                "난이도",
                options=["쉬움", "보통", "어려움"],
                value="보통"
            )
        
        with col2:
            num_questions = st.number_input(
                "생성할 문제 수",
                min_value=1,
                max_value=20,
                value=5
            )
            
            additional_info = st.text_area(
                "추가 요구사항 (선택사항)",
                placeholder="특정 단원, 문제 스타일, 키워드 등을 입력하세요",
                height=100
            )
        
        # 문제 생성 버튼
        if st.button("🚀 AI 문제 생성", type="primary"):
            if not subject:
                st.error("과목명을 입력해주세요.")
                return
            
            with st.spinner("AI가 문제를 생성하고 있습니다..."):
                # 프롬프트 생성
                prompt = create_prompt(question_type, subject, difficulty, num_questions, additional_info)
                
                # AI API 호출
                api_key = st.session_state.api_keys[ai_provider]
                
                if "OpenAI" in ai_provider:
                    response = generate_with_openai(api_key, prompt)
                elif "Anthropic" in ai_provider:
                    response = generate_with_anthropic(api_key, prompt)
                elif "Google" in ai_provider:
                    response = generate_with_gemini(api_key, prompt)
                
                if response:
                    # 응답 파싱
                    questions_data = parse_ai_response(response, question_type)
                    
                    if questions_data:
                        st.success(f"{len(questions_data)}개의 문제가 생성되었습니다!")
                        
                        # 생성된 문제 미리보기 및 저장
                        for i, q_data in enumerate(questions_data):
                            with st.expander(f"문제 {i+1} 미리보기"):
                                st.write(f"**문제:** {q_data.get('question', '')}")
                                
                                if question_type == '객관식':
                                    options = q_data.get('options', [])
                                    for j, option in enumerate(options):
                                        st.write(f"{['①', '②', '③', '④'][j]} {option}")
                                    st.write(f"**정답:** {q_data.get('correct_answer', '')}")
                                
                                elif question_type == 'O/X':
                                    st.write(f"**정답:** {q_data.get('correct_answer', '')}")
                                
                                else:  # 주관식
                                    st.write(f"**정답:** {q_data.get('answer', '')}")
                                
                                if q_data.get('explanation'):
                                    st.write(f"**해설:** {q_data.get('explanation', '')}")
                        
                        # 일괄 저장 버튼
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("모든 문제 저장"):
                                for q_data in questions_data:
                                    if question_type == '객관식':
                                        question = create_question(
                                            question_type, subject, difficulty,
                                            q_data.get('question', ''),
                                            q_data.get('options', []),
                                            q_data.get('correct_answer', ''),
                                            q_data.get('explanation', '')
                                        )
                                    elif question_type == 'O/X':
                                        question = create_question(
                                            question_type, subject, difficulty,
                                            q_data.get('question', ''),
                                            None,
                                            q_data.get('correct_answer', ''),
                                            q_data.get('explanation', '')
                                        )
                                    else:  # 주관식
                                        question = create_question(
                                            question_type, subject, difficulty,
                                            q_data.get('question', ''),
                                            None,
                                            q_data.get('answer', ''),
                                            q_data.get('explanation', '')
                                        )
                                    st.session_state.questions.append(question)
                                
                                st.success("모든 문제가 저장되었습니다!")
                                st.rerun()
                        
                        with col2:
                            # 원본 응답 보기
                            with st.expander("AI 원본 응답 보기"):
                                st.code(response)
    
    # 수동 문제 출제 탭
    elif menu == "수동 문제 출제":
        st.header("✏️ 수동 문제 출제")
        
        col1, col2 = st.columns(2)
        
        with col1:
            question_type = st.selectbox(
                "문제 유형",
                ["객관식", "주관식", "O/X"]
            )
            
            subject = st.text_input("과목명", placeholder="예: 수학, 영어, 과학")
            
            difficulty = st.select_slider(
                "난이도",
                options=["쉬움", "보통", "어려움"],
                value="보통"
            )
        
        with col2:
            question_text = st.text_area(
                "문제 내용",
                height=100,
                placeholder="문제를 입력하세요..."
            )
        
        # 문제 유형별 추가 입력
        if question_type == "객관식":
            st.subheader("선택지 입력")
            col1, col2 = st.columns(2)
            
            with col1:
                option1 = st.text_input("① 번", key="opt1")
                option2 = st.text_input("② 번", key="opt2")
            
            with col2:
                option3 = st.text_input("③ 번", key="opt3")
                option4 = st.text_input("④ 번", key="opt4")
            
            correct_answer = st.selectbox("정답", ["①", "②", "③", "④"])
            options = [option1, option2, option3, option4]
        
        elif question_type == "O/X":
            correct_answer = st.radio("정답", ["O", "X"])
            options = None
        
        else:  # 주관식
            correct_answer = st.text_area("정답", height=80)
            options = None
        
        explanation = st.text_area("해설 (선택사항)", height=80)
        
        # 문제 저장
        if st.button("문제 저장", type="primary"):
            if question_text and subject and correct_answer:
                question = create_question(
                    question_type, subject, difficulty, 
                    question_text, options, correct_answer, explanation
                )
                st.session_state.questions.append(question)
                st.success("문제가 저장되었습니다!")
                st.rerun()
            else:
                st.error("필수 항목을 모두 입력해주세요.")
    
    # 문제 은행 탭
    elif menu == "문제 은행":
        st.header("🗂️ 문제 은행")
        
        if not st.session_state.questions:
            st.info("저장된 문제가 없습니다. 먼저 문제를 출제해주세요.")
            return
        
        # 필터링 옵션
        col1, col2, col3 = st.columns(3)
        
        with col1:
            subjects = list(set([q['subject'] for q in st.session_state.questions]))
            subject_filter = st.selectbox("과목 필터", ["전체"] + subjects)
        
        with col2:
            types = list(set([q['type'] for q in st.session_state.questions]))
            type_filter = st.selectbox("유형 필터", ["전체"] + types)
        
        with col3:
            difficulties = list(set([q['difficulty'] for q in st.session_state.questions]))
            difficulty_filter = st.selectbox("난이도 필터", ["전체"] + difficulties)
        
        # 문제 목록 표시
        filtered_questions = st.session_state.questions
        
        if subject_filter != "전체":
            filtered_questions = [q for q in filtered_questions if q['subject'] == subject_filter]
        if type_filter != "전체":
            filtered_questions = [q for q in filtered_questions if q['type'] == type_filter]
        if difficulty_filter != "전체":
            filtered_questions = [q for q in filtered_questions if q['difficulty'] == difficulty_filter]
        
        st.write(f"총 {len(filtered_questions)}개의 문제")
        
        for i, question in enumerate(filtered_questions):
            with st.expander(f"문제 {question['id']}: {question['subject']} ({question['type']}) - {question['difficulty']}"):
                st.write(f"**문제:** {question['question']}")
                
                if question['type'] == '객관식':
                    for j, option in enumerate(question['options']):
                        if option:
                            st.write(f"{['①', '②', '③', '④'][j]} {option}")
                    st.write(f"**정답:** {question['correct_answer']}")
                
                elif question['type'] == 'O/X':
                    st.write(f"**정답:** {question['correct_answer']}")
                
                else:  # 주관식
                    st.write(f"**정답:** {question['answer']}")
                
                if 'explanation' in question and question['explanation']:
                    st.write(f"**해설:** {question['explanation']}")
                
                # 삭제 버튼
                if st.button(f"삭제", key=f"del_{question['id']}"):
                    st.session_state.questions = [q for q in st.session_state.questions if q['id'] != question['id']]
                    st.rerun()
    
    # 시험지 생성 탭
    elif menu == "시험지 생성":
        st.header("📋 시험지 생성")
        
        if not st.session_state.questions:
            st.info("저장된 문제가 없습니다. 먼저 문제를 출제해주세요.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            exam_title = st.text_input("시험지 제목", value="중간고사")
            exam_subject = st.text_input("과목명")
            exam_time = st.number_input("시험 시간 (분)", min_value=10, max_value=300, value=60)
        
        with col2:
            num_questions = st.number_input(
                "문제 수", 
                min_value=1, 
                max_value=len(st.session_state.questions), 
                value=min(10, len(st.session_state.questions))
            )
            
            selection_method = st.radio(
                "문제 선택 방법",
                ["랜덤 선택", "수동 선택"]
            )
        
        if selection_method == "수동 선택":
            st.subheader("문제 선택")
            selected_questions = []
            
            for question in st.session_state.questions:
                if st.checkbox(
                    f"문제 {question['id']}: {question['subject']} - {question['question'][:50]}...",
                    key=f"select_{question['id']}"
                ):
                    selected_questions.append(question)
        
        if st.button("시험지 생성", type="primary"):
            if selection_method == "랜덤 선택":
                selected = random.sample(st.session_state.questions, min(num_questions, len(st.session_state.questions)))
            else:
                selected = selected_questions[:num_questions]
            
            if selected:
                st.session_state.current_exam = {
                    'title': exam_title,
                    'subject': exam_subject,
                    'time': exam_time,
                    'questions': selected,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("시험지가 생성되었습니다!")
                
                # 시험지 미리보기
                st.markdown("---")
                st.subheader("📄 시험지 미리보기")
                
                st.markdown(f"""
                # {exam_title}
                **과목:** {exam_subject}  
                **시험시간:** {exam_time}분  
                **총 문항:** {len(selected)}문제  
                **작성일:** {datetime.now().strftime("%Y년 %m월 %d일")}
                
                ---
                """)
                
                for i, question in enumerate(selected, 1):
                    st.markdown(f"**{i}. {question['question']}**")
                    
                    if question['type'] == '객관식':
                        for j, option in enumerate(question['options']):
                            if option:
                                st.markdown(f"　{['①', '②', '③', '④'][j]} {option}")
                    
                    st.markdown("")
                
                # 정답지
                with st.expander("정답지 보기"):
                    for i, question in enumerate(selected, 1):
                        if question['type'] == '객관식':
                            st.write(f"{i}. {question['correct_answer']}")
                        elif question['type'] == 'O/X':
                            st.write(f"{i}. {question['correct_answer']}")
                        else:
                            st.write(f"{i}. {question['answer']}")
    
    # 설정 탭
    elif menu == "설정":
        st.header("⚙️ 설정")
        
        # 데이터 관리
        st.subheader("데이터 관리")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("전체 문제 삭제"):
                st.session_state.questions = []
                st.success("모든 문제가 삭제되었습니다.")
        
        with col2:
            # JSON 파일로 다운로드
            if st.session_state.questions:
                questions_json = json.dumps(st.session_state.questions, ensure_ascii=False, indent=2)
                st.download_button(
                    label="문제 데이터 다운로드",
                    data=questions_json,
                    file_name="questions.json",
                    mime="application/json"
                )
        
        # 파일 업로드
        st.subheader("문제 데이터 불러오기")
        uploaded_file = st.file_uploader("JSON 파일 선택", type=['json'])
        
        if uploaded_file is not None:
            try:
                questions_data = json.load(uploaded_file)
                st.session_state.questions.extend(questions_data)
                st.success(f"{len(questions_data)}개의 문제를 불러왔습니다.")
                st.rerun()
            except Exception as e:
                st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
        
        # 통계
        if st.session_state.questions:
            st.subheader("문제 통계")
            
            total_questions = len(st.session_state.questions)
            subjects = [q['subject'] for q in st.session_state.questions]
            types = [q['type'] for q in st.session_state.questions]
            difficulties = [q['difficulty'] for q in st.session_state.questions]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 문제 수", total_questions)
            
            with col2:
                most_common_subject = max(set(subjects), key=subjects.count)
                st.metric("가장 많은 과목", most_common_subject)
            
            with col3:
                most_common_type = max(set(types), key=types.count)
                st.metric("가장 많은 유형", most_common_type)

if __name__ == "__main__":
    main()