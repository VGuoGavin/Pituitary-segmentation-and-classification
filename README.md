# nnUNet 
Pituitary tumor document
| nnUNet_Segmentation
| nnUNet_Colab.ipynb is the nnUNet model running on Colab. From data preparation to training to prediction, the resulting model parameters are mainly saved in the checkpoint_final.pth file
| checkpoint_final.pth is the result of the version with the most epoches trained so far, which is about 80 epoches by 40%.
|fold_2 progress.png fold2 training process
![fold_2 progress](https://github.com/VGuoGavin/Pituitary-segmentation-and-classification/assets/53364849/38fd50f6-3a55-49f4-b712-c1e236ca1929)

| fold_4 progress.pngfold 4 training process
![fold_4 progress](https://github.com/VGuoGavin/Pituitary-segmentation-and-classification/assets/53364849/421058ea-9b1c-4d57-a694-5e28fd77653b)

| Classifier
| Radiomics-features.xlsx All features extracted under the first setting (refer to P ituitary_tumor.ipynb code)
| Radiomics-features2.xlsx See P ituitary_tumor.ipynb code for all features extracted in the second setting.
| Tools
|TianTan Tools.exe executable file, integrates several methods of data transformation, easy to directly obtain suitable for nnUNet training database
|tiantan.ico image used as logo
| TianTan.py is the source file from which the exe document is generated
| Pituitary_tumor.ipynb, which is the most important code of the entire project, including data processing, feature extraction, classifier design, etc. TianTan Tools is a part of the visualization code.
| Pituitary_tumor.pdf, and Pituitary_tumor.ipynb is transferred to pdf
| reference paper.pdf is a reference for feature extraction and classifier design in the first way

<img width="865" alt="tools" src="https://github.com/VGuoGavin/Pituitary-segmentation-and-classification/assets/53364849/bedef33d-ad55-495e-b153-9e673b435b55">
