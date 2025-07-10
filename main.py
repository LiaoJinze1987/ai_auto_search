from search_engine import run_engine
from qwen_model import generate_keyword
from email_send import send_batch_emails

if __name__ == "__main__":
    user_thought = "我想知道欧洲有哪些儿童玩具代理商"
    keyword = generate_keyword(user_thought)
    print("生成的关键词：", keyword)
    keyword = f"{keyword} 电话号码 email"
    run_engine(keyword, max_sites=10, output_path = "data/search_results.json")
    #批量发送邮件
    input_path = "data/search_results.json"
    output_path = "data/send_results.json"
    send_batch_emails(input_path, output_path)