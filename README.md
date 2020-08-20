# cobage

# Function inputs

essen_test(model_tb, dic_return, dataset_name, dataset_excel, growth_thresh_mult)

FN, FP, TN, TP = essen_test(model_iEK_griffin, "Yes both", "griffin", griffin_excel, grow_thresh)

model_tb : COBRA model
dic_return : Yes, or Yes both options. Return "fal_neg_dic, fal_pos_dic" or "fal_neg_dic, fal_pos_dic, true_neg_dic, true_pos_dic"
dataset_name : Type of dataset. "griifin" or "loerger"
dataset_excel :  dataset file
growth_thresh_mult : FBA growth threshold

# Griffin

## Inputs:

### Models

model_griffin : iEK1011_griffinEssen_media.json

### Essenciality set

griffin_file : ppat.1002251.s002.xlsx

#griffin essenciality threshold
grif_thres = 0.1

# Loerger

## Inputs:

### Models

model_loerger : iEK1011_deJesusEssen_media.json

### Essenciality set

loerger_file : mbo002173137st3.xlsx

#loerger essenciality threshold
ES being near 0
NE being near the mean
GD approximately 1/10 the mean
GA 5 times the mean


## Output


Matthew Correlation Coefficient (MCC)


