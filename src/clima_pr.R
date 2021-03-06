#Interpola��o utilizando R para Vari�veis de Clima no estado do Paran�

# Instalado pacotes

# install.packages("rgdal")

#Importando bibliotecas
library(geobr)
library(ggplot2)
library(sf)
library(stars)
library(rnaturalearth)
library(rgeos)
library(gstat)
library(fields)
library(ggspatial)
library(rgdal)

# Baixando mapa do Paran�
pr<- read_state(code_state = 'PR') 

# Selecionando �rea de trabalho
setwd("//wsl.localhost/Ubuntu-20.04/home/laryssastephanie/workspace/sprint-3-tmg/sprint-3/Arquivos_R")

#Lendo arquivo csv - Trocar o mes para outubro, novembro ou dezembro
dados.pr <- read.csv('../data/dados_hist_clima_concatenados/INMET_S_PR_MEDIA_OUTUBRO_01-01-2006_A_30-11-2021.CSV')

#Deixando so dados georeferenciados
dados.pr.sf <- st_as_sf(dados.pr,coords = c('LONGITUDE', 'LATITUDE'), crs=4674)

# Criando a grade/malha
grade.pr <- st_make_grid(pr,cellsize = c(.06,.06)) %>% 
  st_as_sf()

grade.pr = grade.pr[pr, ]

#PLOTANDO A GRADE
ggplot() +
  geom_sf(data=grade.pr, size=.15, show.legend = FALSE) +
  labs(subtitle="Paran�, Brasil", size=8) +
  theme_bw()

names(dados.pr)

#IDW
modelo <- gstat(formula = TEMPERATURA.DO.AR...BULBO.SECO..HORARIA..�.C.~1,
                data = as(dados.pr.sf,'Spatial'),
                set = list(idp=10))

#realizando a interpola��o
temp.int <- predict(modelo,as(grade.pr,'Spatial')) %>%
  st_as_sf()

#PLOTANDO OS PONTOS DO CSV
ggplot(dados.pr.sf)+
  geom_sf(aes(color = TEMPERATURA.DO.AR...BULBO.SECO..HORARIA..�.C.), cex= 2.0)+
  geom_sf(data = pr, fill='transparent')+
  scale_color_gradientn(colors = tim.colors(20))+
  scale_fill_gradientn(colors = tim.colors(20))+
  annotation_scale(location='bl')+
  annotation_north_arrow(location='tl',
                         style = north_arrow_nautical,
                         height = unit(1.8,"cm"),
                         width = unit(1.8,"cm"))+
  theme_bw()+
  labs(title="Dados Observados",
       color= "Temperatura do Ar")

# PLOTANDO DADOS INTERPOLADOS
ggplot(temp.int)+
  geom_sf(aes(fill=var1.pred,col=var1.pred))+
  geom_sf(data = pr, fill='transparent')+
  scale_color_gradientn(colors = tim.colors(20))+
  scale_fill_gradientn(colors = tim.colors(20))+
  annotation_scale(location='bl')+
  annotation_north_arrow(location='tl',
                         style = north_arrow_nautical,
                         height = unit(1.8,"cm"),
                         width = unit(1.8,"cm"))+
  theme_bw()+
  labs(title = "Dados Interpolados",
       color = "Temp. do Ar",
       fill= "Temp. do Ar")



#Exportando interpola��o 

#Transformando temp.int para espacial
espacial <- as(temp.int,'Spatial')

#Exportando shapefile
writeOGR(espacial, ".", "temp_outubro_pr", 
         driver = "ESRI Shapefile")

#Abrindo shapefile
shapefile <- read_sf('temp_outubro_pr.shp')


# PLOTANDO DADOS INTERPOLADOS importados
ggplot(shapefile)+
  geom_sf(aes(fill=var1_pred,col=var1_pred))+
  geom_sf(data = pr, fill='transparent')+
  scale_color_gradientn(colors = tim.colors(20))+
  scale_fill_gradientn(colors = tim.colors(20))+
  annotation_scale(location='bl')+
  annotation_north_arrow(location='tl',
                         style = north_arrow_nautical,
                         height = unit(1.8,"cm"),
                         width = unit(1.8,"cm"))+
  theme_bw()+
  labs(title = "Dados Interpolados",
       color = "Temperatura do Ar - Outubro",
       fill= "Temperatura do Ar - Outubro")
