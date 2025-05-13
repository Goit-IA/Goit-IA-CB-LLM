import os
import win32com.client

def convertir_word_a_pdf(ruta_archivo_word, ruta_destino_pdf):
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(ruta_archivo_word)
        doc.SaveAs(ruta_destino_pdf, FileFormat=17)  # 17 = formato PDF
        doc.Close()
        word.Quit()
        print(f"Convertido: {ruta_archivo_word} => {ruta_destino_pdf}")
    except Exception as e:
        print(f"Error al convertir {ruta_archivo_word}: {e}")

def convertir_carpeta_word_a_pdf(carpeta_words, carpeta_pdfs):
    os.makedirs(carpeta_pdfs, exist_ok=True)

    for archivo in os.listdir(carpeta_words):
        ruta_archivo = os.path.join(carpeta_words, archivo)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith(('.doc', '.docx')):
            nombre_sin_ext = os.path.splitext(archivo)[0]
            ruta_pdf = os.path.join(carpeta_pdfs, nombre_sin_ext + '.pdf')
            convertir_word_a_pdf(ruta_archivo, ruta_pdf)

if __name__ == "__main__":
    # Cambia estas rutas según tus carpetas
    CARPETA_WORDS = r"D:\PROJECTS - IA\Goit-IA-CB-LLM\words"
    CARPETA_PDFS = r"D:\PROJECTS - IA\Goit-IA-CB-LLM\pdfs"

    convertir_carpeta_word_a_pdf(CARPETA_WORDS, CARPETA_PDFS)