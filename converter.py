import shutil
import sys
import os
from PIL import Image
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def convert_images_to_pdf(image_paths):
    index = 97
    for img_path in image_paths:
        image = Image.open(img_path)
        pdf_path = f"./questions_PDF_files/mmn_question_"+chr(index)+".pdf"

        # Create a new PDF document
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Set the size of the image in the PDF
        width, height = letter
        c.setPageSize((width, height))

        # Draw the image on the PDF
        c.drawImage(img_path, 0, 0, width, height)

        # Save the PDF and close the canvas
        c.save()
        index += 1


def clear_PDF_folder():
    path_to_files2 = './questions_PDF_files/'

    for root, dirs, file_names in os.walk(path_to_files2):
        for file_name in file_names:
            if os.path.exists(path_to_files2 + file_name):
                os.remove(path_to_files2 + file_name)


def main():
    num_args = len(sys.argv)

    clear_PDF_folder()

    path_to_files2 = './images/'
    images_list = [os.path.join(path_to_files2, file_name) for file_name in os.listdir(path_to_files2)]

    convert_images_to_pdf(images_list)

    output_directory = './output_PDF/'
    merger = PdfMerger()

    path_to_files = r'./questions_PDF_files/'
    for root, dirs, file_names in os.walk(path_to_files):
        for file_name in file_names:
            merger.append(path_to_files + file_name)

    if num_args > 1:
        merged_pdf_path = output_directory + sys.argv[1] + ".pdf"
    else:
        mmn_index = 10
        for file_names in os.walk(output_directory):
            mmn_index += len(file_names[2])
        mmn_index += 1
        merged_pdf_path = f"{output_directory}mmn{mmn_index}_2024a.pdf"

    merger.write(merged_pdf_path)
    merger.close()


if __name__ == '__main__':
    main()
