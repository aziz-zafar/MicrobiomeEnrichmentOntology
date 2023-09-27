import pandas as pd
import numpy as np
import spacy 
import fuzzywuzzy
from fuzzywuzzy import fuzz


KEGG_pathways = pd.read_csv("KEGG_human_pathways.csv")

MetaCyc_pathways = pd.read_csv("All-instances-of-Pathways-in-MetaCyc.txt", sep = '\t')

print(KEGG_pathways)
print(MetaCyc_pathways)

nlp = spacy.load("en_core_sci_md")

#MetaCyc_pathways['Pathways'] = MetaCyc_pathways['Pathways'].str.replace(r'\(.*\)-', '')
top_matches_fuzz = {}
top_matches_nlp = {}

for pathway_a in KEGG_pathways["Label"]:
    similarity_scores_fuzz = []
    similarity_scores_nlp = []
    doc1 = nlp(pathway_a)

    for pathway_b in MetaCyc_pathways["Pathways"]:
        #perform pairwise scoring, and retain top 5.
        similarity_fuzz = fuzz.token_sort_ratio(pathway_a, pathway_b) / 100
        similarity_scores_fuzz.append((pathway_b, similarity_fuzz))

        doc2 = nlp(pathway_b)
        similarity_nlp = doc1.similarity(doc2)
        similarity_scores_nlp.append((pathway_b, similarity_nlp))

    similarity_scores_fuzz.sort(key=lambda x: x[1], reverse=True)
    similarity_scores_nlp.sort(key=lambda x: x[1], reverse=True)

    top_matches_fuzz[pathway_a] = similarity_scores_fuzz[:5]
    top_matches_nlp[pathway_a] = similarity_scores_nlp[:5]


df_top_matches = pd.DataFrame(top_matches_fuzz)  # 

df_top_matches = df_top_matches.T
df_top_matches.columns = [f"TopMatch{i+1}" for i in range(5)]

df_top_matches.to_csv("top_matches_fuzz.csv", index=True)



