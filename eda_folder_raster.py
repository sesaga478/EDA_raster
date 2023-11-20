import os,glob
import numpy as np
import rasterio
from rasterio.plot import show, show_hist
import matplotlib.pyplot as plt
from scipy import ndimage
import seaborn as sns

def eda_folder_raster(folder,ext):
  files = sorted(glob.glob(folder+'\*.'+ext))
  
  # Configuración de subplots
  
  # Recorrer todas las imágenes y crear diagrama
  for i, file in enumerate(files):
      fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(20, 4))
      try:
          img_path = os.path.join(folder, file)
  
          os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
          # Abrir la imagen con rasterio
          with rasterio.open(img_path) as src:
  
              src_r=src.read(masked=True)
  
              #GEOTIFF INFO
              mean = np.mean(src_r)
              count=np.count_nonzero(src_r)
              count_nozeros=np.count_nonzero(src_r)
              bands=src.count
              stdv = np.std(src_r)
              min_val = np.min(src_r)
              max_val = np.max(src_r)
              #crs = src.crs.to_epsg()
              crs = src.crs
              width = src.width
              height = src.height
              nodata = src.nodata
              dtype = src.dtypes[0]
              bounds = src.bounds
              transform = src.transform
              pixel=src.res
  
              data = src_r.reshape(src.count, -1).T
              name=file.split('\\')[-1]
              print(name)
              # Make recommendations for processing the geotiff file
              #axs[4].set_title("Reccomendations")
              axs[4].text(0.5, 0.8, "RECCOMENDATIONS",horizontalalignment='center', verticalalignment='center', fontsize=10)
              if stdv/mean > 0.2:
                  #print("- Apply a median filter to remove noise")
                  axs[4].text(0.5, 0.6, "- Apply a median filter\nto remove noise",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
              if max_val > 5000:
                  #print("- Apply radiometric calibration to improve accuracy")
                  axs[4].text(0.5, 0.8, "- Apply radiometric calibration\nto improve accuracy",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
              if mean < 50:
                  #print("- Apply histogram equalization to improve contrast")
                  axs[4].text(0.5, 0.4, " Apply histogram equalization\nto improve contrast",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
              if mean > 2000:
                  #print("- Adjust brightness and contrast to improve visibility")
                  axs[4].text(0.5, 0.4, "- Adjust brightness and contrast\nto improve visibility",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
              if max_val < 255:
                  #print("- Apply rescaling to improve dynamic range")
                  axs[4].text(0.5, 0.3, "- Apply rescaling\nto improve dynamic range",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
              if max_val > 65535:
                  #print("- Consider changing the data type to uint32 to avoid data loss")
                  axs[4].text(0.5, 0.3, "- onsider changing the data type\nto uint32 to avoid data loss",horizontalalignment='center', verticalalignment='center', fontsize=9)
                  axs[4].axis('off')
  
              #COL2: Visualización de la imagen
              show(src_r, transform=src.transform, ax=axs[1])
              axs[1].set_title("Original image")
              axs[1].axis('off')
  
              #COL3: Matriz de correlaciones
              corr = np.corrcoef(data.T)
              axs[2].imshow(corr, cmap='viridis')
              axs[2].set_title("Correlation matix")
              axs[2].axis('off')
              
              #COL4: Histograma de las bandas
              show_hist(src, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=axs[3])
              axs[3].get_legend().remove()
              axs[3].set_title("Histogram")
              axs[3].axis('off')
              
              src.close()
  
          #COL1: PROFILE, la distancia se divide por 2000, pues el ancho es de 2000mts
          axs[0].text(0.5, 0.5, f'IMAGE PROFILE\n\n{name}\n\nDtype: {dtype}; Bands: {bands}; NoData: {nodata}\nResolution: {pixel[0]:.2f} mts per pix\nCount (All): {count:,} pix\nCount: {count/bands:,.0f} pix\n\nDistance: {(count/bands/2000)*pixel[0]:,.0f} mts\nWidth: {width:,} pix; {width*pixel[0]:,.0f} mts\nHeight: {height:,} pix; {height*pixel[0]:,.0f} mts\n\nMean: {mean:.2f}; Stdv: {stdv:.2f}\nMin: {min_val}; Max: {max_val}',
                          horizontalalignment='center', verticalalignment='center', fontsize=9)
          #axs[0].set_title("Image Profile")
          axs[0].axis('off')
          
          folder_path=r'C:\Users\sebas\Documents'
          display(plt.show())
          plt.savefig(os.path.join(folder_path, '{}_EDA.png'.format(file.split('.')[0])))
          plt.close(fig)
          
      except:
          pass
