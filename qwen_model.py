from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_PATH = r"D:\ai_analysis_model\model\Qwen1.5-0.5B-Chat"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, trust_remote_code=True).eval().to("cpu")

def generate_keyword(user_input):
    prompt = [
        {"role": "system", "content": "你是一个精通搜索引擎的关键词生成专家。"},
        {"role": "user", "content": f"请为以下意图生成适合Bing搜索的关键词：{user_input}。只返回关键词本身，不要任何解释。"}
    ]

    # 先生成 prompt 文本
    chat_text = tokenizer.apply_chat_template(prompt, tokenize=False)

    # 然后手动 tokenize 以便获取 input_ids 和 attention_mask
    inputs = tokenizer(chat_text, return_tensors="pt", padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # 推理
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("[DEBUG] 原始输出：", repr(result))

    # 提取关键词（保底只取最后一行）
    lines = result.strip().split("\n")
    keyword = lines[-1].strip()
    return keyword


if __name__ == "__main__":
    user_thought = "我想了解德国有哪些工业机器人代理商"
    keyword = generate_keyword(user_thought)
    print("生成的关键词：", keyword)
