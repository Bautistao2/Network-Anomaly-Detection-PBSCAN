# Network-Anomaly-Detection-PBSCAN
# 🚀 Network Anomaly Detection with PBSCAN & FastAPI  
🛡️ **Detección de Anomalías en Tráfico de Red usando PBSCAN y Machine Learning**  

> 💻 Un sistema avanzado basado en **DBSCAN**, **PCA** y **FastAPI** para detectar tráfico malicioso en tiempo real.  

---

## **📚 Descripción**  
🔍 Este proyecto implementa un **sistema inteligente** de detección de anomalías en tráfico de red utilizando **PBSCAN (DBSCAN optimizado)**.  
✔️ Permite preprocesar datos, reducir dimensiones con **PCA**, entrenar un modelo y hacer **predicciones en tiempo real** vía API.  
✔️ Basado en el dataset de **KDDCup99**, ampliamente usado en la seguridad informática para detectar intrusiones y ataques.  

### **Principales Características:**  
✅ **Preprocesamiento avanzado** con normalización y reducción de dimensiones (PCA).  
✅ **Entrenamiento de PBSCAN** para detectar patrones anómalos en la red.  
✅ **API en tiempo real** para evaluar nuevas conexiones y determinar si son sospechosas.  
✅ **Análisis gráfico** para visualizar anomalías y correlaciones.  

---

## **📂 Estructura del Proyecto**  

📁 `src/` → Código fuente principal  
📄 `data_preprocessing.py` → Preprocesamiento del dataset  
📄 `distancia.py` → Cálculo de **eps óptimo** para DBSCAN  
📄 `pbscan.py` → Implementación del modelo PBSCAN  
📄 `analizar_anomalias.py` → Análisis gráfico y estadístico de anomalías  
📄 `api.py` → API REST para predicciones en tiempo real  
📄 `main.py` → Ejecución principal del pipeline  
📁 `data/` → Dataset y resultados de anomalías  

---


## **⚙️ Instalación y Configuración**  

### **1️⃣ Clonar el Repositorio**  
```bash
git clone https://github.com/tuusuario/Network-Anomaly-Detection-PBSCAN.git
cd Network-Anomaly-Detection-PBSCAN
```