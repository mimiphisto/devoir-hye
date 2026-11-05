import pandas as pd

train = pd.read_csv("data/HYE_train.tsv", sep="\t")
test_in = pd.read_csv("data/HYE_test_in-domain.tsv", sep="\t")
test_out = pd.read_csv("data/HYE_test_out-of-domain.tsv", sep="\t")
tagset = pd.read_csv("data/HYE_tagset.txt", sep="\t", header=None, usecols=[0], names=["tag"])

print("lignes : train", len(train), "| test_in", len(test_in), "| test_out", len(test_out))
print("pos avec espace de fin dans train :", int((train["pos"].str.strip() != train["pos"]).sum()))
print("lemma avec espace de fin dans train :", int((train["lemma"].str.strip() != train["lemma"]).sum()))
print("pos uniques dans train :", train["pos"].nunique())
print("∅ présent dans train :", bool((train["pos"] == "∅").any()))
print()

print("Q1 via groupby/size :")
print(train.groupby("pos").size().sort_values(ascending=False).head(5).to_string())
print()

mask = train["pos"].str.split("@").str.len() > 1
print("Q2 via split/len : proportion =", round(mask.mean(), 6), "| n =", int(mask.sum()), "/", len(train))
print(train.loc[mask, "pos"].value_counts().head(5).to_string())
print()

n_art = int(train["pos"].str.contains(r"@PRO\+Dem$", regex=True).sum())
n_z = int(train["lemma"].str.contains(r"^զ@", regex=True).sum())
print("Q3 via regex : @PRO+Dem final =", n_art, "| lemma ^զ@ =", n_z)
print()

valid_set = set(tagset["tag"].str.strip().unique())
uniq = pd.Series(train["pos"].unique())
ok = uniq.str.split("@").apply(lambda ps: set(ps).issubset(valid_set))
bad = uniq[~ok.values]
print("Q4 via apply sur labels uniques : etiquettes hors tagset =", bad.tolist())
print(train["pos"].value_counts().loc[bad].to_string())
print()

ct = pd.crosstab(train["form"], train["pos"])
dico = ct.idxmax(axis=1)
top_pos = train["pos"].value_counts().idxmax()
for name, test in [("in-domain", test_in), ("out-of-domain", test_out)]:
    pred = test["form"].map(dico).fillna(top_pos)
    score = (pred == test["pos"]).mean()
    inconnues = int(test["form"].isin(dico.index).eq(False).sum())
    print(f"Q5 via crosstab/idxmax/map [{name}] : score = {round(score, 6)} | formes inconnues = {inconnues}/{len(test)}")
print("baisse in - out =", round((test_in['form'].map(dico).fillna(top_pos) == test_in['pos']).mean()
                                - (test_out['form'].map(dico).fillna(top_pos) == test_out['pos']).mean(), 6))
