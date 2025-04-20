from flask import Blueprint, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

chat_bp = Blueprint('chat', __name__)

# 加载模型和tokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(device)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({'error': '缺少问题内容'}), 400
    
    try:
        # 生成回答
        inputs = tokenizer(question, return_tensors='pt').to(device)
        outputs = model.generate(**inputs, max_new_tokens=1024)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(answer)
        
        return jsonify({
            'question': question,
            'answer': answer
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500