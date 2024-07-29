Hướng dẫn thực thi:

Các file tinh chỉnh BARTpho viết dưới dạng Jupyter NoteBook, để thực thi chỉ cần chạy trên môi trường Kaggle với GPU là T100
- Với BARTpho tinh chỉnh trên tập dữ liệu Law-QA -> Chạy file bartpho_1.ipynb 
- Với BARTpho tinh chỉnh trên tập dữ liệu Law-QA + VIMQA -> Chạy file bartpho_2.ipynb 
- Với BARTpho tinh chỉnh trên tập dữ liệu Law-QA + VIMQA + YesNo_qna -> Chạy file bartpho_3.ipynb 
- Sinh câu trả lời của BARTpho cho các ví dụ -> Lưu checkpoint của mô hình sau khi tinh chỉnh, sau đó chạy file test_model.ipynb
- Đánh giá điểm Gemini cho chất lượng của câu trả lời do mô hình sinh ra -> Chạy file Gemini_score.py
- Thiết lập giao diện ChatBot pháp luật -> Chạy file interface.py