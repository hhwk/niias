from ollama import chat
from ollama import ChatResponse
from docx import Document
from PyPDF2 import PdfReader

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_path):
    reader = PdfReader(file_path)
    full_text = []
    for page in reader.pages:
        full_text.append(page.extract_text())
    return '\n'.join(full_text)

def main():
    file_path = 'GTA.docx' #Путь к файлу

    if file_path.endswith('.docx'):
        file_text = read_docx(file_path)
    elif file_path.endswith('.pdf'):
        file_text = read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please use a .docx or .pdf file.")

    system1 = ("Твоя задача — создать одно предложение, которое кратко описывает основную идею текста.")
    term1 = ("Отвечай только одним предложением на русском языке. Только одно предложение!")
    full_prompt1 = (f"Задача: {system1}\n\nТекст: {file_text}\n\nУсловие: {term1}")

    system2 = ("Кратко перескажи текст. Пересказывай текст на русском в формате полносвязного рассказа")
    term2 = ("Не надо форматировать текст. Игнорирую источники и авторов")
    full_prompt2 = f"Задача: {system2}\n\nТекст: {file_text}\n\nУсловие: {term2}"

                                        #deepseek-r1 - отвечает на английсмком + надо очищать от /think
                                        #llama3.2 - на второй вопрос дает такойже ответ как и на первый + втсавляет символы для кастомизации текста

                                        #mixtral - не хватает памяти
                                        #gemma3:27b - не хватает памяти

                                        #gemma3:12b -
                                        #qwen2.5 -
                                        #mistral -
    response1: ChatResponse = chat(model='qwen2.5', messages=[
        {'role': 'system',
         'content': system1},
        {'role': 'assistant',
         'content': term1},
        {'role': 'user', 'content': full_prompt1}
    ])
    print("Первый ответ:")
    print(response1.message.content)

    response2: ChatResponse = chat(model='qwen2.5', messages=[
        {'role': 'system', 'content': system2},
        {'role': 'assistant', 'content': term2},
        {'role': 'user','content': full_prompt2},
    ])
    print("\nВторой ответ:")
    print(response2.message.content)

    with open('output/20. qwen_GTA.txt', 'w', encoding='utf-8') as f:
        f.write("Первый ответ:\n")
        f.write(response1.message.content)
        f.write("\n\nВторой ответ:\n")
        f.write(response2.message.content)

if __name__ == "__main__":
    main()
