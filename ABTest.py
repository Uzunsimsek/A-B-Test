
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

#Varsayım ve hipotezler için gerekli kütüphaneler
from scipy.stats import shapiro
import scipy.stats as stats
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter("ignore", category=ConvergenceWarning)

pd.pandas.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.0f' % x)

#control grubunun yüklenmesi
abcontrol=pd.read_excel("8.Hafta/Dataset/ab_testing_data.xlsx",sheet_name="Control Group")
dfc=abcontrol.copy()
dfc.head()


#test grubunun eklenmesi
abtest=pd.read_excel("8.Hafta/Dataset/ab_testing_data.xlsx",sheet_name="Test Group")
dft=abtest.copy()
dft.head()

metriklerC=[dfc["Impression"],dfc["Click"],dfc["Purchase"],dfc["Earning"]]
metriklerT=[dft["Impression"],dft["Click"],dft["Purchase"],dft["Earning"]]

# fonksiyon ile birlikte tüm değişkenler için kontrol test grubu oluşturuyorum
def birlestir():
IA_B=[]
CA_B=[]
PA_B=[]
EA_B=[]
    for col in metriklerC:
        ImpC=pd.DataFrame(metriklerC[0])
        ClickC=pd.DataFrame(metriklerC[1])
        PurchC=pd.DataFrame(metriklerC[2])
        EarnC=pd.DataFrame(metriklerC[3])
    for col in metriklerT:
        ImpT=pd.DataFrame(metriklerT[0])
        ClickT=pd.DataFrame(metriklerT[1])
        PurchT=pd.DataFrame(metriklerT[2])
        EarnT=pd.DataFrame(metriklerT[3])
    IA_B=pd.concat([ImpC,ImpT],axis=1)
    CA_B=pd.concat([ClickC,ClickT],axis=1)
    PA_B=pd.concat([PurchC,PurchT],axis=1)
    EA_B=pd.concat([EarnC,EarnT],axis=1)
    IA_B.columns=["Control","Test"]
    CA_B.columns=["Control","Test"]
    PA_B.columns=["Control","Test"]
    EA_B.columns=["Control","Test"]

birlestir()

IA_B.head()

Gruplar=[IA_B,CA_B,PA_B,EA_B]
Gruplar[0]
type(Gruplar)


# shapiro(IA_B.Control)
# stats.mannwhitneyu(IA_B["Control"],IA_B["Test"])
# stats.levene(IA_B.Control, IA_B.Test)[1]

def testler():
    for col in Gruplar:
        a=shapiro(col.Control)[1]
        if a < 0.05:
            print(col.name,'%.4f' % a, ":", "P-Value 0.05'ten küçük olduğu için normal dağılım varsayımı sağlanmamaktadır" ,end="\n\n")
            test_istatistigi, pvalue = stats.mannwhitneyu(col["Control"], col["Test"])
            print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
        else:
            print('%.4f' % a, ":","P-Value 0.05'ten büyük olduğu için Normal dağılım varsayımı sağlanmaktadır!")
            b=stats.levene(col.Control, col.Test)[1]
            if b > 0.05:
                print('%.4f' % b, ":","Varyans Homejendir! Hipotezi Uygulayabilirsin",end="\n\n")
                test_istatistigi, pvalue = stats.ttest_ind(col["Control"], col["Test"], equal_var=True)
                print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
                if pvalue < 0.05:
                    print("P Value değeri 0.05'ten küçük olduğu için anlamlı bir fark vardır",end="\n\n")

                else:
                    print("P Value değeri 0.05'ten büyük olduğu için anlamlı bir fark yoktur",end="\n\n")
            else:
                print('%.4f' % b,"Varyans Homejen değildir!",end="\n\n")
                test_istatistigi, pvalue = stats.ttest_ind(col["Control"], col["Test"], equal_var=True)
                print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue),end="\n\n")


testler()


def metriccalculate():
    for col in metriklerC:
    for kol in metriklerT:
        if kol.name == col.name:
        print(kol.name,"Test:",('%.0f' % kol.sum()),col.name,"Control:",('%.0f' % col.sum()),"---" " Fark:", '%.0f' %  (kol-col).sum())

metriccalculate()

# Impression Test: 4820496 Impression Control: 4068458 Fark: 752039
# Click Test: 158702 Click Control: 204026 Fark: -45324
# Purchase Test: 23284 Purchase Control: 22036 Fark: 1248
# Earning Test: 100596 Earning Control: 76343 Fark: 24253


# Future Engineering

#CTR metriği aslında yapılan reklam çalışmasını ölçmek için en iyi metrik
dfc["CTR"]=dfc["Impression"] / dfc["Click"]
#Control grubunun CTR ortalamasını hesaplıyoruz
dfc["CTR"].mean()
#CTR ortalaması 21

#Aynı işlemi Test Grubu için de yapıyorum
dft["CTR"]=dft["Impression"] / dft["Click"]
dft["CTR"].mean()
#CTR ortalaması 32
(dft["CTR"].mean()/dfc["CTR"].mean())-1
# 0.492
#Test Grubunun CTR oranı Control grubuna göre %49 daha fazla

dfc.head()

#Siteye gelen kullanıcıların satın alma oranını buluyorum
dfc["CR"]=dfc["Click"]/dfc["Purchase"]
dfc["CR"].mean()
# Control grubunun CR 'ı % 9.8

#Siteye gelen kullanıcıların satın alma oranını buluyorum
dft["CR"]=dft["Click"]/dft["Purchase"]
dft["CR"].mean()
# Test grubunun CR 'ı % 7.3
# Control grubunun CR oranı test grubuna göre %26 daha az

#Sepet tutarını buluyorum. Çünkü Earning'te anlamlı bir fark varken Purchasede anlamlı fark yoktu.
dfc["AOV"]=dfc["Earning"]/dfc["Purchase"]
dfc["AOV"].mean()
# 3.6 sepet tutarı


dft["AOV"]=dft["Earning"]/dft["Purchase"]
dft["AOV"].mean()
# 4.6 sepet tutarı

dfc["Purchase"].sum()
dft["Purchase"].sum()

# Yapılan alışveriş sayıları yakın fakat sepet tutarı farkılılığından dolayı Test grubunun earningi daha fazla

dfc.head()
dft.head()

Grup_A=np.arange(len(dfc))
Grup_A=pd.DataFrame(Grup_A)
Grup_A[:]="Control"
dfc=pd.concat([dfc,Grup_A],axis=1)
dfc.head()

Grup_B=np.arange(len(dft))
Grup_B=pd.DataFrame(Grup_B)
Grup_B[:]="Test"
dft=pd.concat([dft, Grup_B],axis=1)
dft.head()

TestControl=pd.concat([dfc,dft])
TestControl.rename(columns={0:"TestOrControl"},inplace=True)
TestControl.head()
TestControl.tail()

# TestControl.to_csv("ABtest.csv")



















