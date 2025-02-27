import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils.data_dir import root_dir

model_name = f"{root_dir}/DeepSeek-R1-Distill-Qwen-7B"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def generate_response(prompt, max_new_tokens=1024):  # Format the prompt as a chat message
    messages = [{"role": "user", "content": prompt}]
    # Apply the chat template and tokenize the input
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    # Prepare the input for the model
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    # 确保tokenizer中有正确的pad_token和eos_token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # 设置正确的pad_token_id和eos_token_id
    model.config.pad_token_id = tokenizer.pad_token_id
    model.config.eos_token_id = tokenizer.eos_token_id
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,  # Control the length of the generated text
        pad_token_id=tokenizer.pad_token_id,  # 防止报填充和结束混淆错误
        eos_token_id=tokenizer.eos_token_id
    )
    # Decode the generated IDs to text
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


def chat(prompt):
    start_time = time.time()
    response = generate_response(prompt)
    end_time = time.time()
    print(f"Time taken for prompt：'{prompt}...{end_time - start_time: .2f}' seconds")
    print(f"answer：'{response}")
    return response
