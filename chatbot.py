
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration


model_name = 'facebook/blenderbot-400M-distill'
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

def chat(input_text, history=None):
    if history is None:
        history = []
    
    history.append(input_text)
    
    inputs = tokenizer(history, return_tensors='pt', truncation=True, padding=True)
    

    reply_ids = model.generate(**inputs)
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    
    history.append(reply)
    
    return reply, history


history = []
inputs = [
    "Hello, how are you?",
    "What's the weather like today?",
    "Tell me a joke."
]

for input_text in inputs:
    response, history = chat(input_text, history)
    print(f"Input: {input_text}")
    print(f"Response: {response}\n")
