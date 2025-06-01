import bentoml

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    pipeline,
)

tokenizer = AutoTokenizer.from_pretrained(
    'glekk/xlm-roberta-base-ukrainian-ner-ukrner',
)
model = AutoModelForTokenClassification.from_pretrained(
    'glekk/xlm-roberta-base-ukrainian-ner-ukrner',
)

pipe = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple",
)

bentoml.transformers.save_model(
  "ner-pipe",
  pipe,
  signatures={
    "__call__": {"batchable": True}
  }
)