import streamlit as st
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Claude API client
api_key = st.secrets["ANTHROPIC_API_KEY"]
anthropic = Anthropic(api_key=api_key)

def claude_query(prompt):
    try:
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"Claude API 오류: {str(e)}")
        return None

def generate_example_sentence(language, difficulty):
    prompt = f"Generate a {difficulty} level sentence in {language}. The sentence should be appropriate for language learners and demonstrate key grammar points and vocabulary for that level."
    return claude_query(prompt)

def generate_lesson(language, difficulty, custom_text=None):
    st.subheader(f"{language} - {difficulty} 레벨 학습")
    
    if custom_text:
        original_text = custom_text
    else:
        original_text = generate_example_sentence(language, difficulty)
    
    st.write("원문:", original_text)
    
    # 번역
    translation_prompt = f"Translate the following {language} text to Korean: '{original_text}'"
    translated = claude_query(translation_prompt)
    if translated:
        st.write("번역:", translated)
    
    # 어휘 학습
    vocabulary_prompt = f"List and explain 5 key vocabulary words from this {language} sentence, suitable for {difficulty} level learners: '{original_text}' The answer must be in Korean."
    vocabulary_explanation = claude_query(vocabulary_prompt)
    if vocabulary_explanation:
        st.subheader("주요 어휘")
        st.write(vocabulary_explanation)
    
    # 문법 설명
    grammar_prompt = f"Explain the key grammar points in this {language} sentence, focusing on {difficulty} level: '{original_text}' The answer must be in Korean."
    grammar_explanation = claude_query(grammar_prompt)
    if grammar_explanation:
        st.subheader("문법 포인트")
        st.write(grammar_explanation)
    
    # 발음 가이드
    pronunciation_prompt = f"Provide a pronunciation guide for this {language} sentence: '{original_text}' The answer must be in Korean."
    pronunciation_guide = claude_query(pronunciation_prompt)
    if pronunciation_guide:
        st.subheader("발음 가이드")
        st.write(pronunciation_guide)
    
    # 문화적 참고 사항
    culture_prompt = f"Provide cultural context or interesting facts related to this {language} sentence: '{original_text}' The answer must be in Korean."
    cultural_notes = claude_query(culture_prompt)
    if cultural_notes:
        st.subheader("문화적 참고 사항")
        st.write(cultural_notes)
    
    # 퀴즈
    st.subheader("퀴즈")
    quiz_prompt = f"Generate 3 quiz questions in Korean about the following {language} sentence: '{original_text}' The questions should be suitable for {difficulty} level learners."
    questions = claude_query(quiz_prompt).split('\n')
    
    for i, question in enumerate(questions):
        st.write(f"질문 {i+1}: {question}")
        user_answer = st.text_input(f"답변 {i+1}", key=f"answer_{i}")

    if st.button("답변 제출"):
        all_answers = [st.session_state.get(f"answer_{i}", "") for i in range(3)]
        all_answers_text = "\n".join([f"Question {i+1}: {q}\nAnswer: {a}" for i, (q, a) in enumerate(zip(questions, all_answers))])
        evaluation_prompt = f"Evaluate these answers for the quiz about '{original_text}':\n\n{all_answers_text} Provide the evaluation in Korean."
        evaluation = claude_query(evaluation_prompt)
        st.write("평가 결과:", evaluation)

def main():
    st.title("언어 학습 보조 도구")
    language = st.selectbox("학습할 언어를 선택하세요:", ["영어", "스페인어", "일본어"])
    difficulty = st.radio("난이도를 선택하세요:", ["초급", "중급", "고급"])
    custom_text = st.text_input("직접 문장을 입력하세요 (선택사항):")
    if st.button("학습 시작"):
        generate_lesson(language, difficulty, custom_text)

if __name__ == "__main__":
    main()
