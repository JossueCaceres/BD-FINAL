# Instrucciones para Compilar el PDF

## Opción 1: Usar Overleaf (Recomendado)

1. Ve a [Overleaf](https://www.overleaf.com)
2. Crea un nuevo proyecto
3. Sube el archivo `avance.tex`
4. Sube también la imagen `ER-BD1.png` y `UtecLogo.jpeg`
5. Asegúrate de que el compilador esté configurado como **pdfLaTeX**
6. Compila el documento

## Opción 2: Instalar LaTeX localmente

### En macOS:
```bash
# Instalar MacTeX (puede tomar tiempo)
brew install --cask mactex

# O instalar BasicTeX (más liviano)
brew install --cask basictex

# Después de instalar, reinicia el terminal y ejecuta:
pdflatex avance.tex
```

### En Ubuntu/Debian:
```bash
sudo apt-get install texlive-full
pdflatex avance.tex
```

### En Windows:
- Descargar e instalar MiKTeX desde https://miktex.org/
- Usar TeXworks o similar para compilar

## Errores Comunes y Soluciones

1. **Error de UTF-8**: Asegúrate de que el archivo esté guardado en codificación UTF-8
2. **Imágenes faltantes**: Asegúrate de que `ER-BD1.png` y `UtecLogo.jpeg` estén en el mismo directorio
3. **Paquetes faltantes**: En distribuciones locales, instala los paquetes que falten

## Archivos Necesarios

- `avance.tex` (archivo principal)
- `ER-BD1.png` (diagrama ER)
- `UtecLogo.jpeg` (logo de la universidad)

## Compilación Exitosa

Si todo va bien, deberías obtener:
- `avance.pdf` (el documento final)
- `avance.aux`, `avance.log`, `avance.toc` (archivos auxiliares)
