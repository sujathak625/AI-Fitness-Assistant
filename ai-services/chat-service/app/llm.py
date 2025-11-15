# llm.py (optional HF wrapper; will use safely if transformers is installed)
def hf_generate(prompt: str, top_k=1) -> str:
    """
    Lightweight wrapper: uses Hugging Face transformers/generation if installed.
    If HF/torch not available, raises Exception — caller will fallback.
    """
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    except Exception as e:
        raise

    # model you mentioned earlier — flan-t5-large is large; you can switch to a smaller model
    MODEL_NAME = "google/flan-t5-large"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device_map="auto" if hasattr(model, "device") else None)
    out = pipe(prompt, max_new_tokens=128, do_sample=False, clean_up_tokenization_spaces=True)
    return out[0]["generated_text"]
