import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from collections import Counter

# Cargar datos
data = pd.read_csv("spam_assassin.csv")
# Preprocesamiento
data["text"] = data["text"].str.lower()
data["text"] = data["text"].str.replace("[^a-zA-Z0-9]", " ", regex=True)
data["text"] = data["text"].str.replace("\s+", " ", regex=True)
data["text"] = data["text"].str.strip()
# === Análisis de palabras y peso de repetición ===
word_counts = []
unique_word_counts = []
repetition_weights = []

for text in data["text"]:
    words = text.split()
    total_words = len(words)
    word_counts.append(total_words)

    counter = Counter(words)
    unique_words = len(counter)
    unique_word_counts.append(unique_words)

    # Peso por repetición: (total - únicas) / total
    repetition_weight = (total_words - unique_words) / total_words if total_words > 0 else 0
    repetition_weights.append(repetition_weight)

# Agregar análisis al DataFrame
data["word_count"] = word_counts
data["unique_word_count"] = unique_word_counts
data["repetition_weight"] = repetition_weights

# Vectorización
vectorizer = TfidfVectorizer(stop_words="english")
features = vectorizer.fit_transform(data["text"])
results = data["target"]

# Dividir datos en entrenamiento y prueba
features_train, features_test, results_train, results_test = train_test_split(
    features, results, test_size=0.2, random_state=42
)
data_train, data_test = train_test_split(data, test_size=0.2, random_state=42)

# Modelo de Naive Bayes
model = MultinomialNB()
model.fit(features_train, results_train)

# Predicción
results_pred = model.predict(features_test)

# Evaluación del modelo
print("Precisión del modelo: ", accuracy_score(results_test, results_pred))
# Identificar correos clasificados como spam
spam_indices = [i for i, pred in enumerate(results_test) if pred == 1]
print("Índices de correos clasificados como spam:")
print(spam_indices)
# Imprimir solo los pesos de repetición de esos correos
print("\nPesos de repetición de los correos clasificados como SPAM:")
for i in spam_indices:
    peso = data_test.iloc[i]["repetition_weight"]
    print(f"Correo #{i} - Peso de repetición: {peso:.4f}")