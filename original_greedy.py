import pandas as pd
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)

model_name = "NousResearch/llama-2-7b-chat-hf"

model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

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
                    max_length=int(test_length[i]) + 150)
    input_text = test_text[i]
    result = pipe(input_text)
    print(result[0]['generated_text'][len(input_text):])
    print()
    results.append(result[0]['generated_text'][len(input_text):])

print(f"len of result: {len(results)}")
rs_df = pd.DataFrame(results, columns=['text'])
rs_df.to_excel('./results/base.xlsx', index=False)
