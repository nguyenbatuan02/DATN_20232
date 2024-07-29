import time
genai.configure(api_key="AIzaSyAjNdcFWOYN-1UhM2Q4tocy9T0KfImEEcM")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def mark(context, question, answer, index):
    prompt = f"""Chấm điểm trên thang điểm 10 dựa trên sự ngắn gọn và súc tích của câu trả lời sau dựa trên đoạn văn: {context}. Câu hỏi: {question}. Trả lời: {answer}. 
                Với những câu hỏi mà không có thông tin trả lời trong đoạn văn thì câu trả lời sé là: Không tim thấy thông tin câu trả lời.
                Chỉ trả lời duy nhất điểm số đạt được"""
    response = model.generate_content([prompt])
    # Giả sử rằng mô hình trả về điểm số ở cuối câu trả lời
    try:
        response_text = response.text.strip()
        score_part = response_text.split('/')[0]  # Lấy phần trước dấu "/"
        score = float(score_part)
        return score
    except (ValueError, IndexError):
        print(f"Không thể lấy điểm từ phản hồi cho mẫu {index}: {response.text}")
        return 0  # Hoặc xử lý lỗi theo cách khác

# Chấm điểm cho toàn bộ tập test1
total_score = 0
num_samples = len(test1)

for i, sample in enumerate(test1[1865:], start = 1865):
    context = sample['context']
    question = sample['question']
    answer = sample['answer']
    score = mark(context, question, answer, i)
    total_score += score
    time.sleep(2)

# Tính điểm trung bình
average_score = total_score / num_samples if num_samples > 0 else 0
print("Điểm trung bình cho tập test1 là:", average_score)