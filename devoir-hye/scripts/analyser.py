import pandas as pd

train = pd.read_csv("data/HYE_train.tsv", sep="\t")
test_in = pd.read_csv("data/HYE_test_in-domain.tsv", sep="\t")
test_out = pd.read_csv("data/HYE_test_out-of-domain.tsv", sep="\t")

print("Q1 : 5 categories (pos) les plus frequentes dans le train")
print(train["pos"].value_counts().head(5))
print()

print("Q2 : proportion de formes composees (@ dans pos) et top 5 des etiquettes composees")
comp = train["pos"].str.contains("@")
n_comp = comp.value_counts()[True]
print(f"proportion : {n_comp / len(train):.4f} soit {n_comp} mots sur {len(train)}")
print(train[comp]["pos"].value_counts().head(5))
print()

print("Q3 : article suffixe et preposition զ")
dem = train["pos"].str.contains(r"@PRO\+Dem$")
z = train["lemma"].str.contains(r"^զ@")
print("pos finissant par @PRO+Dem :", dem.value_counts()[True])
print("lemma commençant par «զ@» :", z.value_counts()[True])
print()

print("Q4 : etiquettes du train absentes du tagset (avec effectifs)")
# .str.strip() : supprime l'espace finale de certains tags du tagset ("A ")
tags = pd.read_csv("data/HYE_tagset.txt", sep="\t", header=None,
                   usecols=[0], names=["tag"])
tags["tag"] = tags["tag"].str.strip()
tags["k"] = 1
c2 = tags.merge(tags, on="k", how="left")
comb2 = c2["tag_x"] + "@" + c2["tag_y"]
c3 = c2.merge(tags, on="k", how="left")
comb3 = c3["tag_x"] + "@" + c3["tag_y"] + "@" + c3["tag"]
valid = pd.concat([tags["tag"], comb2, comb3], ignore_index=True)
bad = train[~train["pos"].isin(valid)]["pos"].value_counts()
print(bad if len(bad) else "(aucune)")
print("note : PRO+Pos3 et ∅ figurent dans le gold mais pas dans le tagset ; "
      "ils sont signales ci-dessus sans etre comptes contre le modele.")
print()

print("Q5 : dictionnaire form -> pos majoritaire (train uniquement) puis scores")
train["combi"] = train["form"] + "|" + train["pos"]
vc = train["combi"].value_counts()
counts = pd.concat([vc], axis=1).rename(columns={vc.name: "n"})
counts["cle"] = counts.index
pairs = train[["form", "pos", "combi"]].drop_duplicates().rename(columns={"combi": "cle"})
dico = pairs.merge(counts, on="cle", how="left")
dico = dico.sort_values(["n", "pos"], ascending=[False, True]).drop_duplicates("form")
dico = dico[["form", "pos"]].rename(columns={"pos": "pred"})
top_pos = train["pos"].value_counts().head(1).index[0]
print("pos la plus frequente du train (repli pour formes inconnues) :", top_pos)
print("formes dans le dictionnaire :", len(dico))


def score(test):
    inconnues = test[~test["form"].isin(dico["form"])][["form"]].drop_duplicates()
    inconnues["pred"] = top_pos
    dico_complet = pd.concat([dico, inconnues], ignore_index=True)
    pred = test[["form"]].merge(dico_complet, on="form", how="left")["pred"]
    correct = pred == test["pos"]
    return correct.value_counts()[True] / len(test)


s_in = score(test_in)
s_out = score(test_out)
print("score in-domain :", round(s_in, 4))
print("score out-of-domain :", round(s_out, 4))
print(f"baisse : {s_in - s_out:.4f} (grec : 0,73 -> 0,51, baisse de 0,22)")
