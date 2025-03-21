from flask import Flask, send_from_directory, url_for, render_template, redirect
import os
from lib.AESCipher import AESCipher
from lib.ApiRequest import getPdfpath
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import datetime

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PDF_FOLDER = 'd:\\download' # 실제 PDF원본 폴더

#os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/<asepth>', methods=['GET'])
def get_pdf(asepth):
    time = datetime.datetime.now()
    timetype = "%Y/%m/%d %H:%M:%S"
    timestr = time.strftime(timetype)
    # 폰트 등록
    pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
    # 암호화된 내용을 복호화
    aesdec = AESCipher().decrypt(asepth)
    # 복호화 한 내용을 API 에 맞게 replace
    #aesdec = "detail_seq=" + aesdec.replace("//", "&partner_code=") # 실제로쓰이는것
    aesdec = "detail_seq=482050365&partner_code=112555" # 임시
    # 상세 내역을 갖고 오는 API 호출
    pathobj = getPdfpath(aesdec)
    # 파일경로
    pathstr = pathobj["file_path"]
    # PDF 파일이 저장되는 폴더를 드라이브부터 지정후 결합
    pdf_folder = PDF_FOLDER+"\\"+ pathstr
    # 파일이름
    filename = pathobj["drawing_file_db"]
    # PDF 파일을 불러옴
    # 기존 PDF 파일 읽기
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
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename_output), "wb") as output_pdf:
        writer.write(output_pdf)
        writer.close()

    return render_template("viewer.html", title="123", link=os.path.join(app.config['UPLOAD_FOLDER'], filename_output))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500)