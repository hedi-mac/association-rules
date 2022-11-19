import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori_fp
import itertools
from mlxtend.frequent_patterns import association_rules

def binTabByID(idCad, df):
    allProducts = np.sort(pd.unique(df.tProduct))
    products = df.query('ID == '+idCad)['tProduct'].values.tolist()
    res = np.zeros([len(allProducts)])
    for i in range(0, len(allProducts)) :
        if products.__contains__(allProducts[i]) :
            res[i] = 1
    return res

def binTab(df):
    ids = pd.unique(df.ID)
    res = []
    for i in range(0, len(ids)):
        res.append(binTabByID("{}".format(ids[i]), df))
    return res

def a_priori(cross, MIN_SUP, MAX):
    s = cross.shape[0]
    allProducts = np.sort(pd.unique(df.tProduct))
    verif = True
    n = 0
    itemset = list(itertools.product(allProducts[:]))
    while verif :
        if n != 0 :
            t = []
            itemset = pd.unique(C.itemsets.values.tolist())
            for i in range(0, len(itemset)):
                for j in range(0, n):
                    t.extend(itemset[i][:])      
            itemset = pd.unique(list(itertools.combinations(pd.unique(t), n+1)))
        support = np.zeros((len(itemset)))
        for i in range(0, len(itemset)) :
            tab = []
            for j in range(0, len(itemset[i])) :
                tab.append(cross[itemset[i][j]].values.tolist())
            if n ==0 :
                support[i] = sum(cross[allProducts[i]].values.tolist()) / s
            else : 
                tab = [sum(x) for x in zip(*tab)]
                tab = list(filter(lambda x: x == n+1 , tab))
                support[i] = len(tab) / s
        C = pd.DataFrame({'itemsets': itemset, 'support': support})
        C = C.drop(C[C.support < MIN_SUP].index)
        if n == 0 :
            apriori = C 
        else :
            apriori = pd.concat([apriori, C], axis=0)
        n = n + 1
        if C.size == 0 or n == MAX:
            verif = False
    apriori = apriori.reset_index(drop=True)
    return apriori

df = pd.read_table('market_basket.txt', header=0, names=['ID', 'tProduct'])
print("first 10 lines : ")
print(df.head(10))
print("dataframe dimensions : ")
print(df.shape)

cross = pd.crosstab(df.ID, df.tProduct)
#30 premières transactions et les 3 premiers produits
print(cross.iloc[:30,:3])

#print(np.array(binTab(df)))

print()

print(apriori_fp( pd.crosstab(df.ID, df.tProduct), min_support=0.025, max_len=4, use_colnames=True))
MIN_SUP = 0.025 
MAX = 4
apriori_df = a_priori(cross, MIN_SUP, MAX)
# Afficher les 15 premiers itemsets : 
print(apriori_df.head(15))
# Vérifier si un sous-ensemble items est inclus dans l’ensemble x : 
def is_inclus(x,items):
    return items.issubset(x)
# Itemsets comprenant le produit 'Aspirin' :
ids = np.where(apriori_df.itemsets.apply(is_inclus, items={'Aspirin'}))
print(apriori_df.loc[ids])
# Itemsets contenant 'Aspirin' et 'Eggs' : 
ids = np.where(apriori_df.itemsets.apply(lambda x,ensemble:ensemble.issubset(x),ensemble={'Aspirin', 'Eggs'}))
print(apriori_df.loc[ids])
#Génération des règles d’associations : 
regles = association_rules(apriori_df, metric="confidence", min_threshold=0.75)
# 5 premières règles : 
print(regles.head(5))
# Règles avec un LIFT supérieur ou égal à 7 : 
print(regles[regles['lift'].ge(7)])
# Régles menant a '2pct_milk'
print(regles[regles['consequents'].eq({'2pct_Milk'})])

