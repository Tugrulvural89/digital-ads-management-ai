import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Verileri bir sözlük olarak tanımlayın
data = {
    'reklam': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
    'gosterim': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    'tiklama': [20, 25, 18, 22, 21, 28, 30, 25, 27, 29],
    'gelir': [100, 120, 90, 110, 105, 140, 150, 125, 135, 145]
}

# Sözlüğü pandas DataFrame'ine dönüştürün
df = pd.DataFrame(data)

# CTR sütununu hesaplayın
df['ctr'] = df['tiklama'] / df['gosterim'] * 100

# Reklam sütununu sayısal değerlere dönüştürün (A: 0, B: 1)
df['reklam'] = df['reklam'].map({'A': 0, 'B': 1})

# Bağımlı ve bağımsız değişkenleri tanımlayın
X = df[['gosterim', 'gelir', 'ctr']]
y = df['reklam']

# Verileri eğitim ve test kümelerine ayırın
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Lojistik Regresyon modelini eğitin
model = LogisticRegression()
model.fit(X_train, y_train)

# Test kümesinde tahmin yapın
y_pred = model.predict(X_test)

# Tahmin olasılıklarını alın
y_pred_proba = model.predict_proba(X_test)

# Gradyan artırma modelini eğitin
model_gb = GradientBoostingClassifier()
model_gb.fit(X_train, y_train)

# Test kümesinde tahmin yapın
y_pred_gb = model_gb.predict(X_test)

# Tahmin olasılıklarını alın
y_pred_proba_gb = model_gb.predict_proba(X_test)

# Lojistik Regresyon için metrikleri hesapla
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba[:, 1])

print("Lojistik Regresyon Metrikleri:")
print(f"  Doğruluk: {accuracy:.4f}")
print(f"  Hassasiyet: {precision:.4f}")
print(f"  Duyarlılık: {recall:.4f}")
print(f"  F1-skoru: {f1:.4f}")
print(f"  AUC: {auc:.4f}")

# Gradyan Artırma için metrikleri hesapla
accuracy_gb = accuracy_score(y_test, y_pred_gb)
precision_gb = precision_score(y_test, y_pred_gb)
recall_gb = recall_score(y_test, y_pred_gb)
f1_gb = f1_score(y_test, y_pred_gb)
auc_gb = roc_auc_score(y_test, y_pred_proba_gb[:, 1])

print("\nGradyan Artırma Metrikleri:")
print(f"  Doğruluk: {accuracy_gb:.4f}")
print(f"  Hassasiyet: {precision_gb:.4f}")
print(f"  Duyarlılık: {recall_gb:.4f}")
print(f"  F1-skoru: {f1_gb:.4f}")
print(f"  AUC: {auc_gb:.4f}")

# İlk 5 satırı göster
print("\nİlk 5 satır:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Sütunları ve tiplerini göster
print("\nSütun bilgileri:")
print(df.info())

# Her bir reklam için tıklama olasılığını tahmin edin
reklam_a_olasilik = model.predict_proba([[1000, 100, 2]])[:, 1]  # Reklam A için örnek değerler
reklam_b_olasilik = model.predict_proba([[1000, 140, 2.8]])[:, 1]  # Reklam B için örnek değerler

print("\nReklam A Tıklama Olasılığı:", reklam_a_olasilik[0])
print("Reklam B Tıklama Olasılığı:", reklam_b_olasilik[0])

# Daha iyi performans gösteren reklamı belirleyin
if reklam_a_olasilik > reklam_b_olasilik:
    print("\nLojistik Regresyona göre Reklam A daha iyi performans gösteriyor.")
else:
    print("\nLojistik Regresyona göre Reklam B daha iyi performans gösteriyor.")

# Gradyan Artırma modeli için aynı işlemi tekrarlayın
reklam_a_olasilik_gb = model_gb.predict_proba([[1000, 100, 2]])[:, 1]
reklam_b_olasilik_gb = model_gb.predict_proba([[1000, 140, 2.8]])[:, 1]

print("\nReklam A Tıklama Olasılığı (Gradyan Artırma):", reklam_a_olasilik_gb[0])
print("Reklam B Tıklama Olasılığı (Gradyan Artırma):", reklam_b_olasilik_gb[0])

if reklam_a_olasilik_gb > reklam_b_olasilik_gb:
    print("\nGradyan Artırmaya göre Reklam A daha iyi performans gösteriyor.")
else:
    print("\nGradyan Artırmaya göre Reklam B daha iyi performans gösteriyor.")



# cost preditcion

import pandas as pd

# Örnek kampanya verileri
data = {
    'gun': list(range(1, 11)),
    'butce': [100, 120, 150, 130, 110, 140, 160, 180, 170, 150],
    'tiklama': [20, 24, 30, 26, 22, 28, 32, 36, 34, 30],
    'gelir': [1000, 1200, 1500, 1300, 1100, 1400, 1600, 1800, 1700, 1500],
    'gosterim': [10000, 12000, 15000, 13000, 11000, 14000, 16000, 18000, 17000, 15000],
}

# DataFrame oluştur
df = pd.DataFrame(data)

# CTR sütununu hesapla
df['ctr'] = df['tiklama'] / df['gosterim'] * 100

# İlk 5 satırı göster
print("\nİlk 5 satır:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Sütunları ve tiplerini göster
print("\nSütun bilgileri:")
print(df.info())



from sklearn.linear_model import LinearRegression

# Bağımsız değişkenler (X) ve bağımlı değişkenler (y)
X = df[['butce']]
y = df[['tiklama', 'gelir', 'gosterim', 'ctr']]

# Modeli eğit
model = LinearRegression()
model.fit(X, y)

# Yeni bütçe değerleri (örnek olarak 200 ve 250)
yeni_butce = pd.DataFrame({'butce': [200, 250]})

# Tahminleri yap
tahminler = model.predict(yeni_butce)

# Tahminleri bir DataFrame'e dönüştür
tahmin_df = pd.DataFrame(tahminler, columns=['tiklama', 'gelir', 'gosterim', 'ctr'])

# Yeni bütçe değerlerini ekle
tahmin_df['butce'] = yeni_butce['butce']

# Sonuçları yazdır
print("\nYeni Bütçe ile Tahminler:")
print(tahmin_df.to_markdown(index=False, numalign="left", stralign="left"))
