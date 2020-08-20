# cobage

|         |                                                                       |
| ------- | --------------------------------------------------------------------- |
| Authors | Agustin Maria Pardo    |
| Github  | [AgustinPardo](https://github.com/AgustinPardo/)                     |
| Email   | <agustinmpardo@gmail.com>     


# Function inputs

### Usage

essen_test(model_tb, dic_return, dataset_name, dataset_excel, growth_thresh_mult)

FN, FP, TN, TP = essen_test(model_iEK_griffin, "Yes both", "griffin", griffin_excel, grow_thresh)

model_tb : COBRA model

dic_return : "Yes" or "Yes both" options select which dictionaries return.

dataset_name : Type of dataset. "griffin" or "loerger"

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


# Output
Count of FN, FP, TN, TP

|                                                   |                           |               |                   |     |
|:-------------------------------------------------:|:-------------------------:|:-------------:|:-----------------:|:---:|
|                                                   | Experimental data Griffin |               |                   |     |
| Model predictions iEK1011_griffinEssen_media.json |                           | True (Growth) | False (No Growth) |     |
|                                                   |     Positive (Growth)     |      579      |        161        |     |
|                                                   |    Negative (No Growth)   |       29      |        229        |     |
|                                                   |           Total           |               |                   | 998 |


Accuracy (Exactitud):

<a href="https://www.codecogs.com/eqnedit.php?latex=\dpi{120}&space;Accuracy&space;=&space;\frac{(TP&plus;TN)}{(TP&plus;TN&plus;FP&plus;FN)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\dpi{140}&space;Accuracy&space;=&space;\frac{(TP&plus;TN)}{(TP&plus;TN&plus;FP&plus;FN)}" title="Accuracy = \frac{(TP+TN)}{(TP+TN+FP+FN)}" /></a>

Matthew Correlation Coefficient (MCC):

<a href="https://www.codecogs.com/eqnedit.php?latex=\dpi{120}&space;MCC&space;=&space;\frac{TP*TN&space;-&space;FP*FN}{\sqrt{(TP&plus;FP)*(TP&plus;FN)*(TN&plus;FP)*(TN&plus;FN)}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\dpi{140}&space;MCC&space;=&space;\frac{TP*TN&space;-&space;FP*FN}{\sqrt{(TP&plus;FP)*(TP&plus;FN)*(TN&plus;FP)*(TN&plus;FN)}}" title="MCC = \frac{TP*TN - FP*FN}{\sqrt{(TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)}}" /></a>

Dictionaries of FN, FP, TN, TP
