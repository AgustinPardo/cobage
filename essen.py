#! python3

import cobra
from cobra.manipulation import remove_genes
from cobra import Model, Reaction, Metabolite
from cobra.flux_analysis import  single_gene_deletion, single_reaction_deletion,double_gene_deletion, double_reaction_deletion
import math
import pandas as pd
import sys
import matplotlib.pyplot as plt
# from cobra.flux_analysis import production_envelope
# from cobra.flux_analysis import sample
import matplotlib
import numpy as np
from matplotlib_venn import venn3
from matplotlib_venn import venn2
import json
import seaborn as sns

def essen_test(model_tb, dic_return, dataset_name, dataset_excel, growth_thresh_mult):
    
    model = model_tb
    
    fal_pos_dic, fal_neg_dic = {}, {}
    true_neg_dic, true_pos_dic = {}, {}
    
    growth_rates = single_gene_deletion(model)
    indexes=[]
    for x in growth_rates.index: indexes.append(list(i for i in x)[0])

    growth_rates["genes"]=indexes

    orig_growth_thres = growth_thresh_mult*model.optimize().objective_value
    
    true_pos, true_neg, fal_pos, fal_neg = 0, 0, 0, 0
    
    # set grif essen threshold -- iSM810 paper uses 0.1 as "confident essential"
    grif_thres = 0.1
        
    for index, row in dataset_excel.iterrows():
        
        if dataset_name == "griffin":
            gene = str(row["Locus"])
            try:
                growth=growth_rates[growth_rates.genes.isin([gene])].growth[0]                            
                try:                    
                    # True Positive - predicts that it grows (not essential) and is correct.
                    if float(row["p value"]) > grif_thres and growth > orig_growth_thres:
                        true_pos = true_pos + 1
                        true_pos_dic.update({gene: [growth, float(row["p value"])]})

                    # False Positive - predicts that it grows (not essential) when it actually essential
                    elif float(row["p value"]) < grif_thres and growth > orig_growth_thres:
                        fal_pos = fal_pos + 1
                        fal_pos_dic.update({gene: [growth, float(row["p value"])]})
                    
                    # True Negative - predicts that the gene is essential (no growth) and is correct
                    elif float(row["p value"]) < grif_thres and growth < orig_growth_thres:
                        true_neg = true_neg + 1
                        true_neg_dic.update({gene: [growth, float(row["p value"])]})

                    elif float(row["p value"]) > grif_thres and growth < orig_growth_thres:
                        fal_neg = fal_neg + 1
                        fal_neg_dic.update({gene: [growth, float(row["p value"])]})    
                    else:
                        # Hay algunos que tiene growth = nan
                        pass
                        #print(str(gene))
                
                        
                except:
                    pass
                    # print ("Algo mas lo rompio")
                    # print(gene)
                    # print(row.get("p value"))
                    # print(grif_thres) 
                    # print(growth) 
                    # print(orig_growth_thres)
            except:
                   pass
                    # print("Ese gen no esta en el modelo: "+str(gene))
                        
        elif dataset_name == "loerger":
            gene = str(row["ORF ID"])
            """
            ES being near 0
            NE being near the mean
            GD approximately 1/10 the mean
            GA 5 times the mean
            """
            try:
                growth=growth_rates[growth_rates.genes.isin([gene])].growth[0] 
                # growth = growth_rates.loc[gene, "flux"]
                try:           
                    # TP
                    if (row["Final Call"] == "NE" or row["Final Call"] == "GA") and growth > orig_growth_thres:
                        true_pos = true_pos + 1
                        true_pos_dic.update({gene: [growth]})
                           
                    # FN
                    elif (row["Final Call"] == "NE" or row["Final Call"] == "GA") and growth < orig_growth_thres:
                        fal_neg = fal_neg + 1
                        fal_neg_dic.update({gene: [growth]})
                            
                    # TN
                    elif (row["Final Call"] == "ES" or row["Final Call"] == "ESD" or row["Final Call"] == "GD") and growth < orig_growth_thres:
                    # if (row["Final Call"] == "ES") and growth < orig_growth_thres:
                        true_neg = true_neg + 1
                        true_neg_dic.update({gene: [growth]})
                            
                    # FP
                    elif (row["Final Call"] == "ES" or row["Final Call"] == "ESD" or row["Final Call"] == "GD") and growth > orig_growth_thres:
                    # if (row["Final Call"] == "ES") and growth > orig_growth_thres:
                        fal_pos = fal_pos + 1
                        fal_pos_dic.update({gene: [growth]})
                    else:
                        # Hay algunos que tiene growth = nan
                        pass
                        # print(str(gene))
                except:
                    pass
                    # print("algo mas rompio a loerger")
            except:
                pass
                # print("Este gen no esta en el mdoelo: "+str(gene))
                
            
    # ---Analyze and Print results ---
    print ("TP - TN - FP - FN")
    print (true_pos, true_neg, fal_pos, fal_neg)
    
    # percent of correct predictions
    perc_correct = (true_pos+true_neg)/(true_pos+true_neg+fal_pos+float(fal_neg))
    print ("percent correct: ", perc_correct)
    

    # mcc calculation
    MCC_root = math.sqrt((true_pos + fal_pos)*(true_pos + fal_neg)*(true_neg + fal_pos)*(true_neg + fal_neg))
    MCC = (true_pos*true_neg - fal_pos*fal_neg)/MCC_root
    print ("Matthew Correlation Coefficient", MCC)
    if dic_return == "Yes":
        return fal_neg_dic, fal_pos_dic
    elif dic_return == "Yes both":
        return fal_neg_dic, fal_pos_dic, true_neg_dic, true_pos_dic
 

#No esta disponible
#model_iEK.solver = "gurobi"


loerger_file = "/home/agustin/workspace/Paper_IEK1011/DeJesus/mbo002173137st3.xlsx"   
loerger_excel = pd.read_excel(loerger_file,skiprows = 1,keep_default_na=False)

griffin_file = "/home/agustin/workspace/Paper_IEK1011/griffin/ppat.1002251.s002.xlsx"   
griffin_excel = pd.read_excel(griffin_file,skiprows = 9,keep_default_na=False)

model_loerger_file_path="/home/agustin/workspace/Paper_IEK1011/supplementaryMaterial/12918_2018_557_MOESM3_ESM/iEK1011_deJesusEssen_media.json"
model_iEK_loerger = cobra.io.load_json_model(model_loerger_file_path)

model_griffin_file_path="/home/agustin/workspace/Paper_IEK1011/supplementaryMaterial/12918_2018_557_MOESM3_ESM/iEK1011_griffinEssen_media.json"
model_iEK_griffin = cobra.io.load_json_model(model_griffin_file_path)

grow_thresh = 0.2

print ("iEK1011_griffin")
print(model_iEK_griffin.solver.configuration)
FN_dic_iEK, FP_dic_iEK, TN_dic_iEK, TP_dic_iEK = essen_test(model_iEK_griffin, "Yes both", "griffin", griffin_excel, grow_thresh)
print ("iEK1011_loerger")
print(model_iEK_loerger.solver.configuration)
FN_dic_iEK, FP_dic_iEK, TN_dic_iEK, TP_dic_iEK = essen_test(model_iEK_loerger, "Yes both", "loerger", loerger_excel, grow_thresh)
