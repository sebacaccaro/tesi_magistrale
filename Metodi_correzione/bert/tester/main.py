from transformers import pipeline, AutoModel, AutoTokenizer, AutoConfig

""" config = AutoConfig.from_pretrained(pretrained_model_name_or_path="./")

italian_model = AutoModel.from_pretrained(
    pretrained_model_name_or_path="./", config=config)
"""
italian_tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path="./model")

""" unmasker = pipeline(
    'fill-mask', model='dbmdz/bert-base-italian-xxl-cased', top_k=10) """

unmasker = pipeline(
    'fill-mask', model="./model", top_k=20, tokenizer=italian_tokenizer)

while(True):
    lol = unmasker(input(">> ").replace("*", "[MASK]"))
    for sent in sorted(lol, key=lambda x: -x['score']):
        print(f"{sent['token_str']} \t\t\t {sent['score']}")
    print()


# ogni iniziativa atq a sostenere iticntificamentc e con una corretta informazione la valdità dei metodi naturali
# ogni iniziativa atta a sostenere * e con una corretta informazione la valdità dei metodi naturali
