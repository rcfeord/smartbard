from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model

def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer

def generate_text(sequence, max_length, min_length):
    model_path = "../smartbard/gpt2_model/saved_model/" #FIXME: path
    model = load_model(model_path)
    tokenizer = load_tokenizer(model_path)
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    final_outputs = model.generate(
        ids,
        do_sample=True,
        min_length=min_length,
        max_length=max_length,
        # num_beams=10,
        # early_stopping=True,
        eos_token_id=50258,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,
    )
    output_phrase = tokenizer.decode(final_outputs[0], skip_special_tokens=False)
    return output_phrase

def gpt2_generate(sequence: str) -> str:
    max_len = int(100) # 20
    min_len = int(40)
    output_phrase = generate_text(sequence, max_len, min_len)
    return output_phrase
