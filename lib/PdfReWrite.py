from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import os

PDF_FOLDER = 'd:\\download' # 실제 PDF원본 폴더

def pdfrewrite(pathobj, upload_folder):
  # PDF 파일을 불러옴
  # 기존 PDF 파일 읽기
  time = datetime.datetime.now()
  timetype = "%Y/%m/%d %H:%M:%S"
  timestr = time.strftime(timetype)

  # 파일경로
  pathstr = pathobj["file_path"]
  # PDF 파일이 저장되는 폴더를 드라이브부터 지정후 결합
  pdf_folder = PDF_FOLDER + "\\" + pathstr
  # 파일이름
  filename = pathobj["drawing_file_db"]
  reader = PdfReader(pdf_folder+"\\"+filename)

  page = reader.pages[0]
  media_box = page.mediabox
  width = float(media_box.width)
  height = float(media_box.height)

  writer = PdfWriter()

  # 새로운 underlay 텍스트 추가
  packet = BytesIO()
  c = canvas.Canvas(packet, pagesize=(width, height))
  c.setFont("NanumGothic", 10)

  # 좌측 상단 워터마크 설정
  text = c.beginText()
  y_position = height - 15
  text.setFillColorRGB(1, 0, 0) # 빨간색
  text.setTextOrigin(5, y_position)  # 텍스트 시작 위치 (좌측 상단)
  text.textLine("요청자 : "+pathobj[""])  # 첫 번째 줄
  text.textLine("출력시간 : " + timestr)  # 두 번째 줄
  c.drawText(text)

  #좌측하단 워트마크  설정
  text2 = c.beginText()
  text2.setFillColorRGB(0.5, 0.5, 0.5) #회색
  text2.setTextOrigin(5, 5)  # 텍스트 시작 위치 (좌측 하단)
  text2.textLine("dkdkdkdkdk")  # 첫 번째 줄
  c.drawText(text2)

  # 좌측하단 워트마크  설정
  text3 = c.beginText()
  text3.setFillColorRGB(1, 0, 0) # 빨간색
  x_position = width - 80
  text3.setTextOrigin(x_position, 5)  # 텍스트 시작 위치 (우측 하단)
  text3.textLine("Status : "+pathobj[""])  # 첫 번째 줄
  c.drawText(text3)

  c.save()
  # ReportLab의 canvas 데이터를 PDF와 결합
  packet.seek(0)
  underlay = PdfReader(packet)

  # 각 페이지에 텍스트 underlay 적용
  for page in reader.pages:
      page.merge_page(underlay.pages[0])  # 기존 페이지에 새 레이어 병합
      writer.add_page(page)

  # 파일명 뒤에 _output 붙여서 새로 저장
  filename_output=filename.replace(".pdf","_output.pdf")

  # 결과 PDF 저장
  with open(os.path.join(upload_folder, filename_output), "wb") as output_pdf:
      writer.write(output_pdf)
      writer.close()

  return filename_output