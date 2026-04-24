# -*- coding: utf-8 -*-
"""
Spyder Editor

統資三甲 412421446 陳彥嘉
期末報告
@topic: 2018年度A1交通事故分析
"""
# 2. 
import pandas as pd

a = r"C:\Users\Charles\OneDrive\桌面\2018年度A1交通事故資料.csv"
df = pd.read_csv(a, encoding='utf-8-sig')


drop_list = [
    '發生年度','發生月份','發生日期','發生時間','事故類別名稱', 
    '處理單位名稱警局層','發生地點','道路型態子類別名稱','事故位置子類別名稱', 
    '路面狀況-路面鋪裝名稱','路面狀況-路面缺陷名稱','道路障礙-障礙物名稱', # 刪除影響較小的障礙物
    '道路障礙-視距品質名稱','道路障礙-視距名稱','號誌-號誌種類名稱', 
    '號誌-號誌動作名稱','車道劃分設施-分向設施大類別名稱','車道劃分設施-分向設施子類別名稱', 
    '車道劃分設施-分道設施-快車道或一般車道間名稱','車道劃分設施-分道設施-快慢車道間名稱', 
    '車道劃分設施-分道設施-路面邊線名稱','事故類型及型態大類別名稱','事故類型及型態子類別名稱',
    '肇因研判大類別名稱-主要','肇因研判子類別名稱-主要','死亡受傷人數','當事者順位', 
    '當事者區分-類別-子類別名稱-車種', '保護裝備名稱', '行動電話或電腦或其他相類功能裝置名稱', 
    '當事者行動狀態大類別名稱', '當事者行動狀態子類別名稱', '車輛撞擊部位名稱', 
    '車輛撞擊部位子類別名稱','肇因研判大類別名稱-個別','肇因研判子類別名稱-個別','經度','緯度',
    '車輛撞擊部位子類別名稱-其他','車輛撞擊部位子類別名稱-最初','車輛撞擊部位大類別名稱-其他','車輛撞擊部位大類別名稱-最初'
    ]

df.drop(columns=drop_list,inplace=True, errors='ignore')
target_y='當事者區分-類別-大類別名稱-車種'
#df = df.dropna(subset=[target_y]).copy()
df = df.dropna(subset=[target_y]).copy()
df.info() 

#3 介紹所有自變數的原始資料型態? 變數定義? 是否有遺失值? 
#4 說明資料清理的理由(用什麼準則刪除變數?是否有新增衍生變數?如何處理各變數的遺失值?)
df['當事者事故發生時年齡'] = pd.to_numeric(df['當事者事故發生時年齡'], errors='coerce')
df['當事者事故發生時年齡'] = df['當事者事故發生時年齡'].fillna(df['當事者事故發生時年齡'].mean())
df['速限-第1當事者'] = df['速限-第1當事者'].fillna(df['速限-第1當事者'].mean())


from sklearn.preprocessing import OneHotEncoder

df["y_binary"] = df[target_y].apply(
    lambda x: 1 if "機車" in str(x) else 0)
y = df["y_binary"].values


print("目標變數分布：")
print(pd.Series(y).value_counts())

ohe = OneHotEncoder(sparse_output=False)


Weather = ohe.fit_transform(df[["天候名稱"]].fillna("未知"))
Weather = pd.DataFrame(Weather, index=df.index)
Weather.columns = ["Weather_" + str(s) for s in ohe.categories_[0]]


Light = ohe.fit_transform(df[["光線名稱"]].fillna("未知"))
Light = pd.DataFrame(Light, index=df.index)
Light.columns = ["Light_" + str(s) for s in ohe.categories_[0]]


RoadType = ohe.fit_transform(df[["道路類別-第1當事者-名稱"]].fillna("未知"))
RoadType = pd.DataFrame(RoadType, index=df.index)
RoadType.columns = ["RoadType_" + str(s) for s in ohe.categories_[0]]


RoadShape = ohe.fit_transform(df[["道路型態大類別名稱"]].fillna("未知"))
RoadShape = pd.DataFrame(RoadShape, index=df.index)
RoadShape.columns = ["RoadShape_" + str(s) for s in ohe.categories_[0]]


Surface = ohe.fit_transform(df[["路面狀況-路面狀態名稱"]].fillna("未知"))
Surface = pd.DataFrame(Surface, index=df.index)
Surface.columns = ["Surface_" + str(s) for s in ohe.categories_[0]]


Sex = ohe.fit_transform(df[["當事者屬-性-別名稱"]].fillna("未知"))
Sex = pd.DataFrame(Sex, index=df.index)
Sex.columns = ["Sex_" + str(s) for s in ohe.categories_[0]]

run = ohe.fit_transform(df[["肇事逃逸類別名稱-是否肇逃"]].fillna("未知"))
run= pd.DataFrame(run, index=df.index)
run.columns = ["run_" + str(s) for s in ohe.categories_[0]]

place = ohe.fit_transform(df[["事故位置大類別名稱"]].fillna("未知"))
place = pd.DataFrame(place, index=df.index)
place.columns = ["place_" + str(s) for s in ohe.categories_[0]]



X_new = pd.concat([
    df[['當事者事故發生時年齡', '速限-第1當事者',]], 
    Weather, Light, RoadType, RoadShape, Surface, Sex, run, place
], axis=1)
#'肇事逃逸類別名稱-是否肇逃','事故位置大類別名稱 '


X_new = X_new.fillna(0)


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

X_train, X_test, y_train, y_test = train_test_split(X_new, y,
                                                    test_size=0.2, random_state=20251224)

ss = StandardScaler()
X_train_std = ss.fit_transform(X_train)
X_test_std = ss.transform(X_test)

#8 決策樹部分-請使用全變數實測過度學 習 最小資料筆數=2,最小分割請從0.1~0.01 確認從哪裡開始過度學習
acc=[]
for i in range(10,0,-1):

    clf= DecisionTreeClassifier(criterion="gini",min_samples_leaf=2,
                                min_samples_split=i/100,random_state=20251224)
    #配適建模資料集
    clf.fit(X_train,y_train)
    #用clf.score 列出正確率
    print("train Acc=",clf.score(X_train,y_train))
    print("test Acc=",clf.score(X_test,y_test))
    print("Leaves of the tree=", clf.get_n_leaves())
    print("Depth of the tree=", clf.get_depth())
    acc.append([i/100,clf.score(X_train,y_train),clf.score(X_test,y_test),clf.get_n_leaves(),clf.get_depth()])

data=pd.DataFrame(acc)
data.columns=["split","training","testing","leaves","depth"]

clf = DecisionTreeClassifier(criterion="entropy", min_samples_split=0.08, random_state=20251224)
RF = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=20251224)
knn = KNeighborsClassifier(n_neighbors=10)
svm = SVC(kernel="rbf", probability=True, random_state=20251224)

#========================================================

# ====================================================================
# 修正評分項目 9, 10：變數挑選
# ====================================================================
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import cross_val_score

# --- 方法 A: SelectKBest (Chi-square) ---
# 卡方檢定要求輸入必須為非負數，使用 clip(lower=0) 確保安全
X_train_pos = X_train.clip(lower=0)
X_test_pos = X_test.clip(lower=0)

selector = SelectKBest(chi2, k=10)
X_train_chi = selector.fit_transform(X_train_pos, y_train)
X_test_chi = selector.transform(X_test_pos)

print("\n--- [方法 A: Chi-square 挑選後結果] ---")
clf_chi_ent = DecisionTreeClassifier(criterion="entropy", min_samples_split=0.08,
                                     min_samples_leaf=2, random_state=20251224)
clf_chi_ent.fit(X_train_chi, y_train)
print(f"Entropy (Chi2) 訓練 Acc: {clf_chi_ent.score(X_train_chi, y_train):.4f}")
print(f"Entropy (Chi2) 測試 Acc: {clf_chi_ent.score(X_test_chi, y_test):.4f}")

clf_chi_ent2 = DecisionTreeClassifier(criterion="gini", min_samples_split=0.08,
                                      min_samples_leaf=2, random_state=20251224)
clf_chi_ent2.fit(X_train_chi, y_train)
print(f"gini (Chi2) 訓練 Acc: {clf_chi_ent.score(X_train_chi, y_train):.4f}")
print(f"gini (Chi2) 測試 Acc: {clf_chi_ent.score(X_test_chi, y_test):.4f}")


# --- 方法 B: Model Selection (Feature Importance) ---
# 這裡定義 clf_full_ent，解決你的 NameError
clf_full_ent = DecisionTreeClassifier(criterion="entropy", min_samples_split=0.08, min_samples_leaf=2, random_state=20251224)
clf_full_ent.fit(X_train, y_train)

importances = pd.Series(clf_full_ent.feature_importances_, index=X_new.columns)
top5_cols = importances.sort_values(ascending=False).head(5).index.tolist()

print("\n--- [方法 B: Model Selection 前 5 名重要變數] ---")
print(importances.sort_values(ascending=False).head(5))


# ====================================================================
# 修正評分項目 11：全變數 vs 挑選變數比較 (Depth=8)
# ====================================================================
print("\n--- [評分項目 11: 全變數 vs 挑選變數比較結果] ---")

# 建立兩棵樹進行對照，統一參數：深度=8
clf_all_vars = DecisionTreeClassifier(criterion="entropy", max_depth=8,
                                      min_samples_split=0.08, random_state=20251224)
clf_sel_vars = DecisionTreeClassifier(criterion="entropy", max_depth=8,
                                      min_samples_split=0.08, random_state=20251224)

# 全變數訓練
clf_all_vars.fit(X_train, y_train)
# 挑選後的 5 個變數訓練
clf_sel_vars.fit(X_train[top5_cols], y_train)

print(f"使用的重要變數: {top5_cols}")
print(f"全變數 (Depth=8) 測試正確率: {clf_all_vars.score(X_test, y_test):.4f}")
print(f"挑選後 (Depth=8) 測試正確率: {clf_sel_vars.score(X_test[top5_cols], y_test):.4f}")

# ====================================================================
# 評分項目 12：最終建議模型資訊
# ====================================================================
print("\n--- [評分項目 12: 建模建議] ---")
# 我們建議使用「變數挑選後」且「深度=8」的模型
suggested_model = clf_sel_vars 

print(f"建議模型：變數挑選決策樹 (Top 5 Features)")
print(f"樹的深度 (Depth): {suggested_model.get_depth()}")
print(f"葉子總數 (Number of Leaves): {suggested_model.get_n_leaves()}")
print(f"總節點數 (Tree Size): {suggested_model.tree_.node_count}")

# 正確率回顧
print(f"測試正確率: {suggested_model.score(X_test[top5_cols], y_test):.4f}")

#==
# 13
#==
from sklearn.tree import export_text
# 使用你選出的 top5 變數模型
tree_rules = export_text(clf_sel_vars, feature_names=top5_cols)
print(tree_rules)
#法則1： 年齡 大於 60 歲 的長者，若發生在 「交叉路口」 且 「夜間有照明」 的環境，模型也會判定為機車。
#白話解釋： 這反映了高齡騎士在市區交叉路口，即便視線良好，仍是機車事故的高風險族群。
#法則2： 當年齡介於 15 至 24 歲，且速限 超過 35 公里 時，極高機率判定為機車事故。
#白話解釋： 這是典型的「青少年騎士」法則，在中高流速的路段發生事故，身份幾乎都是機車族。


# ====================================================================
# 補充評分項目 14：最佳模型之交叉驗證 CV=5
# ====================================================================
# 針對全變數模型做 CV=5
cv_scores = cross_val_score(clf_all_vars, X_new, y, cv=5)
print(f"\n--- [評分項目 14: 交叉驗證] ---")
print(f"全資料全變數 CV=5 平均正確率: {cv_scores.mean():.4f}") #14

#========================================================
#16
from imblearn.over_sampling import SMOTE

# 1. 執行 SMOTE
sm = SMOTE(random_state=20251224)
X_res, y_res = sm.fit_resample(X_new, y)

# 2. 【核心修正】強行轉回 Pandas 並把名字給它
# X_resample 拿回原本 X_new 的欄位名
X_resample = pd.DataFrame(X_res, columns=X_new.columns)

# y_resample 拿回原本 y 的名字（如果原本沒名字就叫 'target'）
target_name = y.name if hasattr(y, 'name') else 'target'
y_resample = pd.Series(y_res, name=target_name)


print(y_resample.value_counts())

#========================================================


voting_soft = VotingClassifier(estimators=[
    ("K最近鄰",knn),("決策數",clf),("隨機森林",RF),("支援向量機",svm)],
    voting="soft", n_jobs=-1)

voting_soft.fit(X_train_std, y_train)

print("=" * 30)
print("各模型單獨測試正確率：")
clf.fit(X_train_std, y_train)
RF.fit(X_train_std, y_train)
knn.fit(X_train_std, y_train)
svm.fit(X_train_std, y_train)
#==================================================
#DT
print(f"DT測試正確率: {suggested_model.score(X_test[top5_cols], y_test):.4f}")
#===================================================
#svm 18 - 23 用線性 acc比較高
X_train_std=ss.transform(X_train)
X_test_std=ss.transform(X_test)

from sklearn.svm import LinearSVC
m=LinearSVC(C=0.1,class_weight="balanced")
m.fit(X_train_std,y_train)

print("訓練資料集正確率=",m.score(X_train_std, y_train))
print("測試資料集正確率=",m.score(X_test_std, y_test))

y_pred_train=m.predict(X_train_std)
print("訓練分錯幾個=",(y_train!=y_pred_train).sum())
y_pred_test=m.predict(X_test_std)
print("測試分錯幾個=",(y_test!=y_pred_test).sum())

from sklearn.metrics import f1_score
print("訓練F1_score=",f1_score(y_train,y_pred_train,average="weighted"))
print("訓練F1_score=",f1_score(y_test,y_pred_test,average="weighted"))

m1=LinearSVC(C=0.2,class_weight="balanced")
m1.fit(X_train_std,y_train)

print("訓練資料集正確率=",m1.score(X_train_std, y_train))
print("測試資料集正確率=",m1.score(X_test_std, y_test))

y_pred_train=m1.predict(X_train_std)
print("訓練分錯幾個=",(y_train!=y_pred_train).sum())
y_pred_test=m1.predict(X_test_std)
print("測試分錯幾個=",(y_test!=y_pred_test).sum())

from sklearn.metrics import f1_score
print("訓練F1_score=",f1_score(y_train,y_pred_train,average="weighted"))
print("訓練F1_score=",f1_score(y_test,y_pred_test,average="weighted"))

from sklearn.svm import SVC
svm=SVC(gamma=0.1,C=1.0,kernel="rbf",probability=True,random_state=20251217)
svm2=SVC(gamma=0.1,C=2.0,kernel="rbf",probability=True,random_state=20251217)

svm.fit(X_train_std,y_train)
print("核函數 SVM_train Acc=",svm.score(X_train_std,y_train))
print("核函數 SVM_test Acc=",svm.score(X_test_std,y_test))
svm2.fit(X_train_std,y_train)
print("核函數 SVM_train Acc=",svm2.score(X_train_std,y_train))
print("核函數 SVM_test Acc=",svm2.score(X_test_std,y_test))

#====================================================
#rf
from sklearn.ensemble import RandomForestClassifier
RF=RandomForestClassifier(n_estimators=100, max_depth=8,
                          random_state=20251224)
RF.fit(X_train,y_train)
print("隨機森林 100 train acc=",RF.score(X_train,y_train))
print("隨機森林 100 test acc=",RF.score(X_test,y_test))

from sklearn.ensemble import RandomForestClassifier
RF2=RandomForestClassifier(n_estimators=200, max_depth=8,
                          random_state=20251224)

RF2.fit(X_train,y_train)
print("隨機森林 200 train acc=",RF2.score(X_train,y_train))
print("隨機森林 200 test acc=",RF2.score(X_test,y_test))

from sklearn.ensemble import RandomForestClassifier
RF3=RandomForestClassifier(n_estimators=300, max_depth=8,
                          random_state=20251224)

RF3.fit(X_train,y_train)
print("隨機森林 300 train acc=",RF3.score(X_train,y_train))
print("隨機森林 300 test acc=",RF3.score(X_test,y_test))

from sklearn.ensemble import RandomForestClassifier
RF4=RandomForestClassifier(n_estimators=500, max_depth=8,
                          random_state=20251224)

RF4.fit(X_train,y_train)
print("隨機森林 500 train acc=",RF4.score(X_train,y_train))
print("隨機森林 500 test acc=",RF4.score(X_test,y_test))

#====================================================


#因為測試資料及代表母體 也就是未知資料 在標準化的時候不應加入 只有訓練資料標準化
X_train[["當事者事故發生時年齡"]]=ss.fit_transform(X_train[["當事者事故發生時年齡"]])
X_test[["當事者事故發生時年齡"]]=ss.transform(X_test[["當事者事故發生時年齡"]])


X_train[["速限-第1當事者"]]=ss.fit_transform(X_train[["速限-第1當事者"]])
X_test[["速限-第1當事者"]]=ss.transform(X_test[["速限-第1當事者"]])


from sklearn.neighbors import KNeighborsClassifier
knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train,y_train)
#KNN的訓練資料及的正確率是沒有價值的  因為在算正確率的時候找對最像的會是自己
#因此估算自己會多投一票正確的結果 因此會高估訓練資料及的正確率
print("訓練資料集的正確率=",knn.score(X_train,y_train))
print("測試資料集的正確率=",knn.score(X_test,y_test))

#利用迴圈來找最好的K
acc=[]
#用i控制最近鄰
for i in range(1,2604): #2941
    knn=KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    print("K=",i,"測試正確率=",knn.score(X_test, y_test))
    acc.append(knn.score(X_test, y_test))
    
print("測試正確率最高的是=",max(acc))
#因為acc是從0開始編號 k=1會在acc[0]
#所以迴圈從0~480 但是bestK要加個1
bestK=0

for i in range (0,2603):
        if acc[i]==max(acc):
            bestK=i+1
            
print("測試正確率最高的是=",max(acc),"k=",bestK)


#====================================================

print("決策樹 train Acc=",clf.score(X_train_std,y_train))
print("決策樹 test Acc=",clf.score(X_test_std,y_test))
print("RF200 train Acc=",RF.score(X_train_std,y_train))
print("RF200 test Acc=",RF.score(X_test_std,y_test))
print("KNN_train acc=",knn.score(X_train_std,y_train))
print("KNN_test acc=",knn.score(X_test_std,y_test))
print("核函數 SVM_train Acc=",svm.score(X_train_std,y_train))
print("核函數 SVM_test Acc=",svm.score(X_test_std,y_test))


from sklearn.ensemble import VotingClassifier
voting_hard=VotingClassifier(estimators=[
   ("支援向量機",svm),("決策數",clf),("K最近鄰",knn),("隨機森林",RF)],
    voting="hard",n_jobs=-1)

voting_hard.fit(X_train_std,y_train)

print("voting hard_train acc=",voting_hard.score(X_train_std,y_train))
print("voting hard_test acc=",voting_hard.score(X_test_std,y_test))


#做voting 按照測試資料集的高低 排序模型順序
from sklearn.ensemble import VotingClassifier
voting_soft=VotingClassifier(estimators=[
    ("支援向量機",svm),("決策數",clf),("K最近鄰",knn),("隨機森林",RF)],
    voting="soft",n_jobs=-1)

voting_soft.fit(X_train_std,y_train)

print("voting Soft_train acc=",voting_soft.score(X_train_std,y_train))
print("voting Soft_test acc=",voting_soft.score(X_test_std,y_test))
#===============================================
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, scale


# ====== 複製 X_new 來做 K-means (不含 y) ======
X_no_y = X_new.copy()
X_no_y['當事者事故發生時年齡'] = scale(X_no_y['當事者事故發生時年齡'])
X_no_y['速限-第1當事者'] = scale(X_no_y['速限-第1當事者'])

# ====== 複製 X_new 來做 K-means (含 y) ======
X_with_y = X_no_y.copy()
X_with_y['y_binary'] = df['y_binary'].values

# =========================
# 計算 SSE (Elbow) 比較
# =========================
SSE_no_y = []
SSE_with_y = []

for k in range(1, 11):
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=20251224)
    km.fit(X_no_y)
    SSE_no_y.append(km.inertia_)
    
    km.fit(X_with_y)
    SSE_with_y.append(km.inertia_)

plt.plot(range(1, 11), SSE_no_y, marker="o", label="不含 y")
plt.plot(range(1, 11), SSE_with_y, marker="s", label="含 y")
plt.xlabel("K")
plt.ylabel("SSE")
plt.title("Elbow Method 比較")
plt.legend()
plt.show()

print("SSE 不含 y =", SSE_no_y)
print("SSE 含 y =", SSE_with_y)

# =========================
# 假設最佳群數 K=4
# =========================
K_best = 4

# 不含 y
km_no_y = KMeans(n_clusters=K_best, n_init=10, random_state=20251224)
labels_no_y = km_no_y.fit_predict(X_no_y)
sil_no_y = silhouette_score(X_no_y, labels_no_y)
print("\n不含 y 輪廓係數 =", format(sil_no_y, ".4f"))

# 含 y
km_with_y = KMeans(n_clusters=K_best, n_init=10, random_state=20251224)
labels_with_y = km_with_y.fit_predict(X_with_y)
sil_with_y = silhouette_score(X_with_y, labels_with_y)
print("含 y 輪廓係數 =", format(sil_with_y, ".4f"))

# =========================
# 交叉矩陣 & 多數決正確率
# =========================
def pseudo_accuracy(labels, df_binary):
    df_tmp = pd.DataFrame()
    df_tmp['群組'] = labels
    df_tmp['車種二元'] = df_binary.map({0: "非機車", 1: "機車"})
    ctab = pd.crosstab(df_tmp['車種二元'], df_tmp['群組'])
    print("\nK-means 分群 × 機車/非機車 交叉矩陣：")
    print(ctab)
    correct = sum(ctab.max())
    total = ctab.values.sum()
    acc = correct / total
    return acc

acc_no_y = pseudo_accuracy(labels_no_y, df['y_binary'])
print("不含 y 用分群來預測分類的正確率 =",(512+718+133+487)/2882)

acc_with_y = pseudo_accuracy(labels_with_y, df['y_binary'])
print("含 y 用分群來預測分類的正確率 =", (492+718+507+133)/2882)



df_str=df.astype(str) #全部轉成字串
df_hot=pd.get_dummies(df_str) #

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

frequent_itemset=apriori(df_hot,min_support=0.1,use_colnames=True)
frequent_itemset["length"]=frequent_itemset["itemsets"].apply(len)
rules=association_rules(frequent_itemset, metric="lift",min_threshold=1.1)




#把df_hot欄位中 pep欄位所有的值都改成小寫lower()
moto_cols=[c for c in df_hot.columns if "moto" in c.lower()] 
#^ 把符合的條件丟到一個list
print("moto相關欄位=",moto_cols)
targets_y=None 

for c in moto_cols:
    if "1" in c.lower():
        target_y = c 
        break

if target_y is not None:
    print("目前我們要找的目標欄位moto=",1)
    rules_moto=rules[rules["consequents"].apply(lambda x:target_y in [str(i) for i in x])]


kmeans=KMeans(n_clusters=4,init="k-means++",random_state=20251224)
kmeans.fit(X_new)
df1=pd.DataFrame(kmeans.cluster_centers_)
df1.columns=X_new.columns


df1.index = [
    '群組 0：高風險路口群', 
    '群組 1：快車道', 
    '群組 2：高齡者生活圈群', 
    '群組 3：夜間/特定環境群'
]
#============================================================================




