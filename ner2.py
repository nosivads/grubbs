from transformers import TFAutoModelForTokenClassification, AutoTokenizer
import tensorflow as tf

model = TFAutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

sequence = (
    "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, "
    "therefore very close to the Manhattan Bridge."
)

inputs = tokenizer(sequence, return_tensors="tf")
tokens = inputs.tokens()

outputs = model(**inputs)[0]
predictions = tf.argmax(outputs, axis=2)