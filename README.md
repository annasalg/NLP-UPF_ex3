# README

Code repository for Anna Lívia Salgueiro, Laura Moset Estruch & Luísa Schaefer Trindade's exercise for the course Natural Language Processing at UPF (2024)

### Requirements

The code is written using Python 3.10 in Colab's version published on 2024-02-21. Thus, the authors recommend also using Colab for easier and better performance.
You can access the original Colab with this [link](https://colab.research.google.com/drive/1Mlpy9tu9RCccgUC20B2u6Z0vEEPCrnZi?usp=sharing).
The .py files are also provided, the *get_dataset.py* helps you obtain the necessary *recipes_data.csv*, create the data frame and perform the appropriate modifications for the program to work. This file should only need to be run once, unless the user wants to change the number of recipes used. The *main.py* file includes the main program. You can find the needed packages to run them below. 

**Packages required:**
   * gdown=='4.7.3'
   * zipfile
  * pandas=='1.5.3'
   * re=='2.2.1'
   * tdqm
   * spacy=='3.7.4'
      * en_core_web_sm

### Data
The txt files are automatically downloaded when the code is run using _gdown_. The dataset used for this exercise is called Recipe Dataset (over 2M) Food, adapted by Wilmer Arlt Strömberg, retrieved from kaggle.com (available in this [link](https://www.kaggle.com/datasets/wilmerarltstrmberg/recipe-dataset-over-2m)), which was originally created by the Poznań University of Technology (PUT) as RecipeNLG.
>[!NOTE]
>If there is any problem with the download, please feel free to contact one of the authors.
