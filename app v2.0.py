import joblib
import pandas as pd
from sklearn.utils import shuffle
from flask import Flask, request, render_template
import json

app = Flask(__name__)
rules = joblib.load('rules')
y = joblib.load('MS')
master = joblib.load('master')
sample = joblib.load('sample')

cart_price=0

def rec (kodetoko,cart):
    while cart.count('')>0:
        cart.remove('')
    clst = y.at[kodetoko,'Cluster']
    temp = rules[clst]
    global cart_price 
    cart_price = 0
    list_rec = []
    for i in cart :
        cart_price += (master[master['Deskripsi']==i].iloc[0,1])
        for j in range(len(temp)):
            if i in temp['item_antecedent'][j]:
                list_rec+=(temp['item_consequent'][j])
    list_desk = []
    list_price = []
    for i in list_rec:
            if i in cart:
                pass
            else :
                list_desk.append(i)
                list_price.append(master[master['Deskripsi']==i].iloc[0,1])
    df_rec = pd.DataFrame()
    df_rec['Deskripsi']=list_desk
    df_rec['Sales (Harga Jual)']=list_price
    df_rec['Sales (Harga Jual)'] = df_rec['Sales (Harga Jual)'].astype(int)
    df_rec = shuffle(df_rec)
    df_rec.reset_index(drop=True)
    if len(df_rec)>10:
        desk = df_rec.iloc[:10,0]
        harga = df_rec.iloc[:10,1]
    else : 
        desk = df_rec.iloc[:,0]
        harga = df_rec.iloc[:,1]
    return list(set(list(zip(desk,harga))))

@app.route('/')
def recsys():
    return render_template('index.html')


@app.route('/rekomendasi', methods=['POST'])
def hasil():
    if request.method == 'POST':
        DataUser = request.form
        order1 = DataUser['order1']
        order2 = DataUser['order2']
        order3 = DataUser['order3']
        order4 = DataUser['order4']
        store = DataUser['store']
        recom = rec(store,[order1,order2,order3,order4])

        return render_template('result.html', tot = cart_price.astype(int) , recom = recom)

@app.route('/data')
def data():
    data = sample
    return render_template('sample.html', data=data.drop(['Find', 'Name', 'Level', 'New Category', 'Month', 'Day',
       'Cluster'],axis=1))

@app.route('/dataviz')
def dataviz():
    return render_template('dataviz.html')

if __name__ == "__main__":

    app.run(debug=True)