# 自動影像校準(Image Registration)
這項專案的開發，是為了解決電腦斷層掃描(Computed Tomography, 簡稱CT)與核磁共振成像(Nuclear Magnetic Resonance Imaging, 簡稱MR)，因為時間和地點導致相同物體所產生的偏移，為了使之後的訓練得到更標準的結果，所以開發了這項專案，來解決同物體所產生的偏差。

## 檔案

| 檔案名稱 | 描述 |
| -------- | -------- |
| [config](https://github.com/wenwen357951/-Image-Registration/blob/master/config.py) | 存放路徑的配置檔案 |
| [main](https://github.com/wenwen357951/-Image-Registration/blob/master/main.py) | 專案運行的主程式進入點 |
| [exe](https://github.com/wenwen357951/-Image-Registration/blob/master/exe.py) | 根據SimpleITK產生出的tfm校準檔案執行偏移 (deprecated) |
| [reg](https://github.com/wenwen357951/-Image-Registration/blob/master/reg.py) | 使用SimpleITK校準圖片輸出tfm校準檔 (deprecated) |
| [reg_itk](https://github.com/wenwen357951/-Image-Registration/blob/master/reg_itk.py) | 使用ITK校準圖片並輸出移動後圖片 |

## 校準方式
Ref: [https://itk.org/ITKExamples/src/Registration/Common/Perform2DTranslationRegistrationWithMeanSquares/Documentation.html](https://itk.org/ITKExamples/src/Registration/Common/Perform2DTranslationRegistrationWithMeanSquares/Documentation.html)
需要先讀入兩張圖像，分別是參考(固定)圖像(fixedImage)與目標(移動)圖像(movingImage)，使用均方誤差(Mean Square Error, 簡稱MSE)來判斷兩影像的差異，當求得的MSE的值越小，代表兩影像的差異越少。因使用MSE來進行運算，所以必須確保兩影像的寬度與高度必須一樣。

### Mean Square Error
在統計學中，均方誤差是對於無法觀察的參數<img src="https://latex.codecogs.com/svg.latex?\theta" title="\theta" />的一個估計函數<img src="https://latex.codecogs.com/gif.latex?\mathit{T}" title="\mathit{T}" />，其定義為：
<div style="text-align:center"><img align=center src="https://latex.codecogs.com/svg.latex?\mathrm{MSE(\mathit{T})=E((\mathit{T&space;-&space;\theta&space;})^2)}" title="\mathrm{MSE(\mathit{T})=E((\mathit{T - \theta })^2)}" /></div>
MSE的主要計算方式是將兩影像的每一個像素點進行相減，再將其平方加總後，取平均值來獲取MSE值。
