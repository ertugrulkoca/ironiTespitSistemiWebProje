import time
import pandas as pd
import re
import string
from flask import Flask,jsonify
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from keras.models import model_from_json
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS


start_time = time.time()
app = Flask(__name__)
CORS(app)
@app.route('/<string:examples>', methods=['GET'])
def api(examples):
    def text_cleaning(metin):
        metin = metin.lower()
        p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        metin = p.sub('', metin)
        metin = " ".join(filter(lambda x:x[0]!='@', metin.split()))
        emoji = re.compile("["u"\U00002702-\U000027B0"u"\U000024C2-\U0001F251"u"\U0001F1E0-\U0001F1FF"  # bayraklar
                           u"\U0001F600-\U0001FFFF"  # emojiler
                           u"\U0001F680-\U0001F6FF"  # harita sembolleri
                           u"\U0001F300-\U0001F5FF"  # piktogram
                           "]+"
                               ,flags=re.UNICODE)
        
        metin = emoji.sub(r'', metin)
        metin = metin.lower()
        metin = re.sub(r"\'d", " would", metin)
        metin = re.sub(r"\'ve", " have", metin)
        metin = re.sub(r"\'ll", " will", metin)  
        metin = re.sub(r"\'ve", " have", metin)  
        metin = re.sub(r"\'re", " are", metin)
    
        metin = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-]", "", metin)
        return metin
    
    

    
    def kelime_tokenize(df):
        derlem = list()
        satirlar = df["Tweet_text"].values.tolist()
    
        for satir in satirlar:
            satir = text_cleaning(satir)
            # datasetten gelen cümleyi tokenize etmek için;
            tokenler = word_tokenize(satir)
            # noktalama işaretlerini kaldırmak için;
            tablo = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(tablo) for w in tokenler]
            # alfabetik olmayan karakterlerin temizlenmesi;
            words = [word for word in stripped if word.isalpha()]
            stop_words = set(stopwords.words("english"))
            # stop wordslerin kaldırılması;
            words = [w for w in words if not w in stop_words]
            derlem.append(words)
        return derlem
    
    def models():
        with open('model/tokenizer_100d.json') as f:
            tokenizer = tokenizer_from_json(f.read())
    
        
        with open('model/model_architecture_100d.json', 'r') as f:
            model = model_from_json(f.read())
    
        
        model.load_weights('model/model_weights_100d.h5')
    
        return model, tokenizer
    model , tokenizer_obj = models()
    
    
    
    x_final = pd.DataFrame({"Tweet_text":[examples]})
    examples2=kelime_tokenize(x_final)
    test_sequences = tokenizer_obj.texts_to_sequences(examples2)
    test_review_pad = pad_sequences(test_sequences, maxlen=20, padding='post')
    
    
    result = model.predict(test_review_pad)
    result*=100
    if result[0][0]>=50: denemetext= "It's a irony!" 
    else: denemetext= "It is not a irony!"
    yuzde = str(result[0][0])
    return jsonify({"cevap":[{'sonuc':denemetext,'yuzde':yuzde}]})

app.run(port=5000,use_reloader=False)
