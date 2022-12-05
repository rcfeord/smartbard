from transformers import BertTokenizer, BertForMaskedLM
import torch
import pandas as pd

def rhyme_word_pred(masked_lim: str, top_k=50) -> tuple:
    """
    takes a limerick with masked words
    uses BERT to predicted possible replacement words in mask location
    """
    tz = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    model.eval()

    tokenized_text = tz.tokenize(masked_lim)
    indexed_tokens = tz.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    masked_pos = [i for i,d in enumerate(tokenized_text) if d=='[MASK]']

    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    rhyme_list = ()
    for msk_ind in masked_pos:
        probs = torch.nn.functional.softmax(predictions[0, msk_ind], dim=-1)
        top_k_weights, top_k_indices = torch.topk(probs, top_k, sorted=True)

        temp_list = []
        for i, pred_idx in enumerate(top_k_indices):

            predicted_token = tz.convert_ids_to_tokens([pred_idx])[0]
            token_weight = top_k_weights[i]
            temp_tpl = (predicted_token, float(token_weight))

            temp_list.append(temp_tpl)

    rhyme_list = rhyme_list + (temp_list,)

    return rhyme_list
