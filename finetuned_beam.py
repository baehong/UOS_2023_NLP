import pandas as pd
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)

model_path = "./nlp_results/checkpoint-300"  # 불러올 모델의 경로
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

test_df = pd.read_excel('./datasets/test_dataset.xlsx')

# 'text', 'length'열 받아오기
test_text = test_df['text']
test_length = test_df['length']

# Run text generation pipeline with our next model
results = []
print(len(test_text))
for i in range(len(test_text)):
    pipe = pipeline(task="text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_length=int(test_length[i]) + 150,
                    temperature=0.7,
                    top_k=50,
                    top_p=0.9,
                    num_beams=5)
    input_text = test_text[i]
    result = pipe(input_text)
    print(result[0]['generated_text'][len(input_text):])
    print()
    results.append(result[0]['generated_text'][len(input_text):])

print(f"len of result: {len(results)}")
rs_df = pd.DataFrame(results, columns=['text'])
rs_df.to_excel('./results/beam.xlsx', index=False)
