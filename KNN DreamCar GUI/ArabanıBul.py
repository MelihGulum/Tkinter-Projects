from tkinter import *
from tkinter import ttk
import tkinter.font
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.datasets import fetch_openml
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,MinMaxScaler,OneHotEncoder, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import NearestNeighbors

#Veri Setini yüklüyoruz.
allCarss = pd.read_excel('veriseti.xlsx')

#Veri setinde float tipindeki değişkenleri integer'a çeviriyoruz.
float_col = allCarss.select_dtypes(include=['float64']) # This will select float columns only
#print(list(float_col.columns.values))
for col in float_col.columns.values:
   allCarss[col] = allCarss[col].astype('int64')

#Drop/Option Menu için eşsiz değerleri alıyoruz.
marka_unique = allCarss["Marka"].unique()
motor_unique = allCarss["Motor-CC"].unique()
vites_unique = allCarss["Vites"].unique()
yakıt_unique = allCarss["Yakıt"].unique()

#motor-cc seçerken değerlerin artan sırayla gelmsi için sıralama yapıldı.
motor_unique = np.sort(motor_unique)


#Karşımıza çıkan ilk tkinter sayfası
root = Tk()
root.title("ARABANI BUL")
root.iconbitmap('car.ico')
app_height =550
app_width =900
#Tkinter 550*900 boyutunda ekranın hep 100*300 kısımında çıkacak.
root.geometry(f'{app_width}x{app_height}+{300}+{100}')
#Sayfa büyütüp, küçütülme ayarlarını kapadık.
root.resizable(False, False)
root.config(background ="light gray")

#Başlık için yazı tipi belirlendi.
font = tkinter.font.Font(family="Helvetica", size=25, weight="bold")
#Başlık etikeki
headerLabel = Label(root, text="HAYALİNDEKİ ARABANI BUL", font=font, bg="light gray",fg="black")
headerLabel.pack(side="top", fill="x", pady=30)

#Bilgilendirme etiketi
infoFont = tkinter.font.Font(family="Helvetica", size=13)
infoLabel = Label(root, text="Arabanı bulmak ister misin? Değerleri gir en yakın 5 arabayı bulalım.",
                  font=infoFont, bg="light gray")
infoLabel.pack()


priceLabel = Label(root, text="Fiyat = ",font=infoFont, bg="light gray")
priceLabel.place(x=100, y=150)
#Veri setinde max/min alıp Scale aralığı belirlendi.
priceScale = Scale(from_=allCarss["Fiyat"].min()*1000, to_=allCarss["Fiyat"].max()*1000,
                  orient=HORIZONTAL ,sliderlength=20,
                   bg="light gray")
priceScale.place(x=200, y=150)


yearLabel = Label(root, text="Yıl = ",font=infoFont, bg="light gray")
yearLabel.place(x=100, y=220)
#Veri setinde max/min alıp Scale aralığı belirlendi.
yearScale = Scale(from_=allCarss["Yıl"].min(), to_=allCarss["Yıl"].max(),
                  orient=HORIZONTAL ,sliderlength=20,
                    bg="light gray")
yearScale.place(x=200, y=220)


kılometerLabel = Label(root, text="Kilometre = ",font=infoFont, bg="light gray")
kılometerLabel.place(x=100, y=290)
#Veri setinde max/min alıp Scale aralığı belirlendi.
kılometreScale = Scale(from_=allCarss["Kilometre"].min()*1000, to_=allCarss["Kilometre"].max()*1000,
                       orient=HORIZONTAL ,sliderlength=20,
                    bg="light gray")
kılometreScale.place(x=200, y=290)

yakıtLabel = Label(root, text="Yakıt = ",font=infoFont, bg="light gray")
yakıtLabel.place(x=100, y=350)
#Tıklamada ne yazılacağı ve string bilgisi veriliyor
click = StringVar()
click.set('Yakıt')
#Eşsiz değerler ile bir option menu kuruluyor.
drop = OptionMenu(root, click, *yakıt_unique)
drop.place(x=200, y=350)

markaLabel = Label(root, text="Marka = ",font=infoFont, bg="light gray")
markaLabel.place(x=450, y=150)
#Tıklamada ne yazılacağı ve string bilgisi veriliyor
click_marka = StringVar()
click_marka.set('Marka')
#Eşsiz değerler ile bir option menu kuruluyor.
drop = OptionMenu(root, click_marka, *marka_unique)
drop.place(x=525, y=145)


motorLabel = Label(root, text="Motor = ",font=infoFont, bg="light gray")
motorLabel.place(x=450, y=220)
#Tıklamada ne yazılacağı ve string bilgisi veriliyor
click_motor = StringVar()
click_motor.set('Motor')
#Eşsiz değerler ile bir option menu kuruluyor.
drop_motor = OptionMenu(root, click_motor, *motor_unique)
drop_motor.place(x=525, y=220)


vitesLabel = Label(root, text="Vites = ",font=infoFont, bg="light gray")
vitesLabel.place(x=450, y=290)
#Tıklamada ne yazılacağı ve string bilgisi veriliyor
click_vites = StringVar()
click_vites.set('Vites')
#Eşsiz değerler ile bir option menu kuruluyor.
drop_vites = OptionMenu(root, click_vites, *vites_unique)
drop_vites.place(x=525, y=290)

#Görseli yüklüyoruz, yeniden boyutlandırıp
#tkinter gereği bir label'a atadıktan sonra konumlandırıyoruz.
knight_rider =(Image.open("knight_rider.jpg"))
resized_knight_rider = knight_rider.resize((230,140),Image.ANTIALIAS )
knight_riders= ImageTk.PhotoImage(resized_knight_rider)
knight_riderss = Label(image=knight_riders)
knight_riderss.place(x=655,y=183)

def predict2():

    font2 = tkinter.font.Font(family="Helvetica", size=10, weight="bold")
    headerLabel = Label(root, text="HAYALİNİZDEKİ ARABA", font=font2, bg="light gray", fg="black")
    headerLabel.place(x=350,y=370)

    # Tablo yaparak kullanıcıdan alınan değerler arayüzde görüntüleniyor.
    tree = ttk.Treeview(root,height=1)
    tree['columns'] = ("Fiyat", "Yıl", "Kilometre", "Marka", "Motor","Yakıt", "Vites")
    #Tablo sütunları
    tree.column("#0", width=10)
    tree.column("Fiyat", anchor=W, width=60)
    tree.column("Yıl", anchor=W, width=60)
    tree.column("Kilometre", anchor=W, width=80)
    tree.column("Marka", anchor=W, width=80)
    tree.column("Motor", anchor=W, width=80)
    tree.column("Yakıt", anchor=W, width=80)
    tree.column("Vites", anchor=W, width=110)
    #Tablo Başlıkları
    tree.heading("#0", text="ID", anchor=W)
    tree.heading("Fiyat", text="Fiyat", anchor=W)
    tree.heading("Yıl", text="Yıl", anchor=W)
    tree.heading("Kilometre", text="Kilometre", anchor=W)
    tree.heading("Marka", text="Marka", anchor=W)
    tree.heading("Motor", text="Motor", anchor=W)
    tree.heading("Yakıt", text="Yakıt", anchor=W)
    tree.heading("Vites", text="Vites", anchor=W)
    #Tablo sitili
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25)
    #Tabloya kullanıcıdan aldığımız değerler(get() fonksiyonu ile) ekrana yazdırılır.
    tree.insert(parent="", index='end', iid=0, text="Parent", values=(
                priceScale.get(),yearScale.get(),kılometreScale.get(),
                click_marka.get(),click_motor.get(),
                click.get() ,click_vites.get()  ))

    tree.place(x=200,y=400)


    allCarss = pd.read_excel('veriseti.xlsx')


    bestCarIndex = len(allCarss)
    pd.set_option('display.max_columns', None)

    d = {'Fiyat': [priceScale.get()], 'Kilometre': [kılometreScale.get()], 'Yıl': [yearScale.get()],
         'Vites': [click_vites.get()],'Yakıt': [click.get()],
         'Motor': [click_motor.get()], 'Marka': [click_marka.get()]}
    bestCar = pd.DataFrame(data=d)


    selectedFeatures = ["Fiyat", "Yıl", "Kilometre", "Marka",
                        "Motor","Yakıt", "Vites","Model"]

    allCarss = allCarss[selectedFeatures]
    allCarss = allCarss.append(bestCar, verify_integrity=True, ignore_index=True)

    numeric_features = ['Fiyat',"Motor", 'Kilometre']
    categorical_features = ["Yıl", "Vites", "Yakıt","Marka", "Model"]
    X = allCarss[selectedFeatures]
    preprocess = make_column_transformer(
        (MinMaxScaler(), numeric_features),
        (OneHotEncoder(), categorical_features)
    )

    X = pd.DataFrame(preprocess.fit_transform(X).toarray())
    neigh = NearestNeighbors(algorithm='kd_tree', n_neighbors=5, radius=1.0, leaf_size=30,
                             metric='minkowski', p=2, metric_params=None, n_jobs=None)
    neigh.fit(X)
    result = neigh.kneighbors(X.tail(1))[1][0]

    # print(result)
    result = np.setdiff1d(result, np.array(bestCarIndex))
    # print(result)
    distance = neigh.kneighbors(X.tail(1), n_neighbors=5, return_distance=True)
    distance = np.setdiff1d(distance, np.array(bestCarIndex))
    # print(distance)

    new = allCarss.iloc[result, :]
    #new.insert(6, "Uzaklık", [distance[1], distance[2], distance[3], distance[4]], True)
    #print(new)

    #Benzer araçların çıkacağı ayrı bir ekran
    new_window = Toplevel()
    new_window.title("ARABANI BUL")
    new_window.iconbitmap('car.ico')
    app2_height = 150
    app2_width = 680
    new_window.geometry(f'{app2_width}x{app2_height}+{450}+{318}')
    new_window.resizable(False, False)
    new_window.config(background="light gray")

    font2 = tkinter.font.Font(family="Helvetica", size=10, weight="bold")
    headerLabel = Label(new_window, text="BENZER ARAÇLAR", font=font2, bg="light gray", fg="black")
    headerLabel.pack(side="top", fill="x")

    #benzer araçların yazılması için vir tablo oluşturuyoruz.
    tree1 = ttk.Treeview(new_window,height=4)
    tree1.pack()

    tree1['columns'] = new.columns.values.tolist()
    tree1.column("#0", width=50,anchor=W)
    tree1.heading("#0", text="ID", anchor=W)

    #benzer araçları 193. sartırda bir dataframe alıyoruz. Bu dataframe'den
    #değerleri koloyca çekmek için bu iki for döngüsü yazıldı.
    for i in new.columns.values.tolist():
        tree1.column(i, width=80,anchor=W)
        tree1.heading(i, text=i,anchor=W)
    tree.heading("#0", text="ID", anchor=W)
    for index, row in new.iterrows():
        tree1.insert("", 'end', text=index, values=list(row))
    #print(new.iterrows())

    return result


#Bu buton predict fonksiyonunu aktifleştirir. Tabloları ve KNN ile benzerliği bize verir.
predictButton = Button(root, text="Arabayı Bul", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE,command=predict2)
predictButton.place(x=350, y=490)

#Uygulamayı sistem komutu yardımıyla buton ile kapatma
predictButton = Button(root, text="   Kapat!   ", padx=30, pady=10, borderwidth=2, activebackground="gray", bg="#546879",
                          relief=GROOVE,command=root.quit)
predictButton.place(x=500, y=490)

root.mainloop()