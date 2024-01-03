from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import string
from nltk.tokenize import word_tokenize
from io import BytesIO


def split_text_into_lines(text, max_width, pdf):
    lines = []
    current_line = ""

    for word in text.split():
        if current_line and pdf.stringWidth(current_line + " " + word, "Helvetica", 12) < max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines


def generate_pdf_report(data, common_words, df, bar_plot_path, hist_plot_path):
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer,pagesize=letter)

    pointer = 750
    margen = 50

    max_text_size = pdf._pagesize[0] - (margen * 2)

    original_text = data

    # Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(margen, pointer, "Text Analysis Report")

    pointer = pointer - 30

    # Original Text Section
    pdf.setFont("Helvetica", 12)
    pdf.drawString(margen, pointer, "Original Text:")

    pointer = pointer - 30
    pdf.setFont("Helvetica", 12)


    for paragraph in original_text:
        para = split_text_into_lines(paragraph,max_text_size,pdf)
        for phrase in para:
            pdf.drawString(margen,pointer,phrase)
            pointer = pointer - 15

            if pointer<=80:
                pdf.showPage()
                pointer = 750

        pointer = pointer - 20

    pdf.showPage()

    pointer = 740

    # Analitic Results Section
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(margen, pointer, "Analytical Results:")

    pointer = pointer-20
    
    # Mean and Mode
    pdf.setFont("Helvetica", 12)
    df['word_lengths'] = df['transformed'].apply(lambda x: [len(word) for word in x])     
    pdf.drawString(margen, pointer, f"Considering the length of characters in the words of the text:")
     
    pointer = pointer - 20
     
    pdf.drawString(margen, pointer, f"You can conclude that, on average, the words in the text contain {round(df['word_lengths'].explode().mean())} characters.")
    pointer = pointer - 20
    pdf.drawString(margen, pointer, f"Additionally, it can be observed that the majority of words are {df['word_lengths'].explode().mode()[0]} characters long.")

    pointer = pointer - 40
    # Common Words
    pdf.setFont("Helvetica", 12)
    pdf.drawString(margen, pointer, "Considering the most common words, we can see the following:")
    pdf.setFont("Helvetica", 12)

    pointer = pointer - 20
    pdf.drawString(margen, pointer, f"{'Word': <15} {'Frequency'}")
    pointer = pointer - 20

    for word, frequency in common_words:
        pdf.drawString(margen, pointer, f"{word: <15} {frequency}")
        pointer = pointer - 20

    # Visualizations
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(margen, pointer-20, "Visualizations:")

    pointer = pointer - 50

    # Bar Chart
    pdf.setFont("Helvetica", 12)
    pdf.drawString(margen, pointer, "Bar Chart:")
    pdf.drawInlineImage(bar_plot_path, margen, pointer-280, width=400, height=250)

    pointer = pointer - 320

    if pointer<=150:
        pdf.showPage()
        pointer = 750

    # Histogram
    pdf.setFont("Helvetica", 12)
    pdf.drawString(margen, pointer, "Histogram Chart:")
    pdf.drawInlineImage(hist_plot_path, margen, pointer -290, width=400, height=250)

    pdf.save()

    return pdf_buffer.getvalue()


def tokenize(text):
    return word_tokenize(text)

def remove_punctuation(tokens):
    return [token for token in tokens if token not in string.punctuation]

def convert_to_lowercase(tokens):
    return [token.lower() for token in tokens]

