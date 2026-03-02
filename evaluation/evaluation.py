import json
import pandas as pd
from bert_score import score
from ai_agent import generate_response
from drug_api import get_drug_label

with open('evaluation/test_set.json') as f:
    data = json.load(f)

responses_A = []
responses_B = []
ground_truths = []

for item in  data:
    question = item['question']
    drug = item['drug']
    ground_truth = item['ground_truth']

    context = get_drug_label(drug)

    response_A, _ = generate_response(question, context, forced_variant = 'A')
    response_B, _ = generate_response(question, context, forced_variant = 'B')

    responses_A.append(response_A)
    responses_B.append(response_B)
    ground_truths.append(ground_truth)


P_A, R_A, F1_A = score(responses_A, ground_truths, lang='en', model_type='distilbert-base-uncased')
P_B, R_B, F1_B = score(responses_B, ground_truths, lang='en', model_type='distilbert-base-uncased')

avg_A = F1_A.mean().item()
avg_B = F1_B.mean().item()

improvement = ((avg_B - avg_A) / avg_A) * 100

print(f'Baseline A F1: {avg_A:.4f}')
print(f'Baseline B F1: {avg_B:.4f}')
print(f'Relative Improvement: {improvement:.4f}')

df = pd.DataFrame({
    'question': [x['question'] for x in data],
    'F1_A': F1_A.tolist(),
    'F1_B': F1_B.tolist()
})

df.to_csv('evaluation/results.csv', index=False)

print('Results saved!')