from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)

model_path = "./nlp_results/checkpoint-300"  # 불러올 모델의 경로
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Run text generation pipeline with our next model
prompt = "Hi! My OOTD is black long duck down. Thanks for watching my video."
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
input_text = f"<s>[INST] {prompt} [/INST]"
result = pipe(input_text, max_length=150)
print(result[0]['generated_text'][len(input_text):])
