import pandas as pd
import matplotlib.pyplot as plt

def compter_candidats(df):
    """
    [Question 2] 
    Compte le nombre de candidats à l'élection présidentielle 2022
    en excluant les bulletins blancs, nuls et abstentions.

    Paramètre
    ----------
    df : pandas.DataFrame
        DataFrame contenant les données électorales

    Retour
    ------
    str : phrase type avec le nombre de candidats
    """
    indice_exprimes = ~df["nom"].str.contains("BLANC|NUL|ABSTENTION", case=False, na=False)

    df_exprimes = df[indice_exprimes]

    candidats = df_exprimes["candidat"].nunique()

    return f"En 2022, il y avait {candidats} candidats à l'élection présidentielle."


def scores_nationaux_2(df):
    """
    [Question 3]
    Calcule le nombre de voix et le score (%) national par candidat
    (en excluant les votes blancs, nuls, et abstentions)
    """

    df_travail = df.copy()

    df_travail["voix"] = pd.to_numeric(df_travail["voix"], errors="coerce").fillna(0)
    
    valeurs_exclues = ["BLANCS", "NULS", "ABSTENTIONS"]
    mask_exprimes = ~df_travail["nom"].str.upper().isin(valeurs_exclues)

    df_exprimes = df_travail[mask_exprimes]

    scores = (
        df_exprimes
        .groupby("candidat")["voix"]
        .sum()
        .reset_index()
        .rename(columns={"voix": "votes"})
    )
    
    total_voix = scores["votes"].sum()
    scores["score"] = (scores["votes"] / total_voix) * 100
    
    scores = scores.sort_values(by="votes", ascending=False)
    
    return scores



def scores_departements(df):
    """
    [Question 4 ]
    Calcule les scores (%) aux présidentielles par département et candidat
    """

    df_travail = df.copy()
    df_travail["voix"] = pd.to_numeric(df_travail["voix"], errors="coerce").fillna(0)

    df_exprimes = df_travail.query(
        "nom.str.upper() not in ['BLANCS', 'NULS', 'ABSTENTIONS']", 
        engine="python"
    )

    res = (
        df_exprimes
        .groupby(["code_departement", "candidat"])["voix"]
        .sum()
        .reset_index()
        .rename(columns={"voix": "votes"})
    )

    total_par_dep = res.groupby("code_departement")["votes"].transform("sum")
    res["score"] = (res["votes"] / total_par_dep) * 100

    res = res.sort_values(by=["code_departement", "votes"], ascending=[True, False])

    return res


def comparaison_nationale(df):
    """
    [Question 5]
    Ajoute les scores nationaux aux scores départementaux
    """

    national = scores_nationaux_2(df).rename(
        columns={"votes": "votes_national", "score": "score_national"}
    )
    
    dep = scores_departements(df).rename(
        columns={"votes": "votes_departement", "score": "score_departement"}
    )

    res = dep.merge(national, on="candidat", how="left")

    return res

def calculer_surrepresentation(df):
    """
    Question[6]
    Calcule la variable de surreprésentation pour chaque candidat par département.
    La surreprésentation compare, en relatif, le score local au score national.
    """
    df_res = comparaison_nationale(df)

    df_res["surrepresentation"] = (
        (df_res["score_departement"] / df_res["score_national"]) - 1
    ) * 100

    return df_res


def tracer_top_surrepresentations(df_scores, nom_candidat, n=5):
    """
    Génère un graphique à barres horizontal avec Matplotlib.
    Identifie les départements où la surreprésentation est la plus forte.
    """
    top_df = (
        df_scores[df_scores["candidat"] == nom_candidat]
        .sort_values(by="surrepresentation", ascending=False, key = abs)
        .head(n)
    )

    top_df = top_df.iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(
        top_df["code_departement"], 
        top_df["surrepresentation"], 
        color="royalblue",
        edgecolor="black"
    )

    ax.set_title(f"Top {n} des surreprésentations : {nom_candidat}", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Surreprésentation (en % par rapport au national)", fontsize=11)
    ax.set_ylabel("Code Département", fontsize=11)

    ax.axvline(0, color='black', linewidth=0.8)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%',
            va='center', 
            fontsize=10
        )

    plt.tight_layout()
    return plt.show()