import json
import os
import random, spacy
from spacy.util import minibatch
from spacy.training.example import Example
from spacy.tokens import DocBin
def convert_labelstudio_to_spacy(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    spacy_format = []

    for item in data:
        text = item['data']['text']
        entities = []

        for ann in item.get('annotations', []):
            for result in ann.get('result', []):
                start = result['value']['start']
                end = result['value']['end']
                label = result['value']['labels'][0]
                entities.append((start, end, label))

        spacy_format.append((text, {"entities": entities}))

    with open(output_path, 'w') as f:
        json.dump(spacy_format, f)

def train_test_split_spacy():
    nlp = spacy.blank("en")
    doc_bin = DocBin().from_disk("local_output/spacy_format.spacy")
    docs = list(doc_bin.get_docs(nlp.vocab))
    random.shuffle(docs)

    train_docs = docs[:int(len(docs)*0.8)]
    dev_docs = docs[int(len(docs)*0.8):]

    DocBin(docs=train_docs).to_disk("local_output/train.spacy")
    DocBin(docs=dev_docs).to_disk("local_output/dev.spacy")
    return

def custom_training():
    TRAIN_DATA_PATH = './local_output/spacy_format.json'

    if os.path.exists(TRAIN_DATA_PATH) and os.path.getsize(TRAIN_DATA_PATH) > 0:
        try:
            with open(TRAIN_DATA_PATH, 'r') as file:
                train_data = json.load(file)

            nlp = spacy.load('en_core_web_md')
            
            if 'ner' not in nlp.pipe_names:
                ner = nlp.add_pipe('ner')
            else:
                ner = nlp.get_pipe('ner')

            # Add labels from the training data
            for _, annotations in train_data:
                for ent in annotations.get('entities', []):
                    if ent[2] not in ner.labels:
                        ner.add_label(ent[2])

            # Disable other pipes for training
            other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
            with nlp.disable_pipes(*other_pipes):
                optimizer = nlp.resume_training()
                epochs = 50
                for epoch in range(epochs):
                    random.shuffle(train_data)
                    losses = {}
                    batches = minibatch(train_data, size=2)
                    for batch in batches:
                        examples = []
                        for text, annotations in batch:
                            doc = nlp.make_doc(text)
                            example = Example.from_dict(doc, annotations)
                            examples.append(example)
                        nlp.update(examples, drop=0.5, losses=losses)
                    print(f'Epoch: {epoch}, Losses: {losses}')

            # Save trained model
            nlp.to_disk('custom_ner_model')
            print("Custom NER model saved to 'custom_ner_model'")
        
        except Exception as e:
            print(f"Error during training: {e}")
    else:
        print("Training data not found or empty. Skipping model training.")


def predict(text,trained_nlp):
    entities = {}
    doc = trained_nlp(text)
    for ent in doc.ents:
        entities[ent.label_] = ent.text
        
    return entities
# convert_labelstudio_to_spacy(r'./local_output/label_encoded_pdf.json', r'./local_output/spacy_format.json')
# train_test_split_spacy()
# custom_training()
# with open('./local_output/spacy_format.json', 'r') as file:
#         train_data = json.load(file)

# test_text = train_data[0][0]
# entities = predict(test_text)
# print(entities)
