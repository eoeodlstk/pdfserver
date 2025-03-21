from flask import Flask, send_from_directory, url_for, render_template, redirect
import os
from lib.AESCipher import AESCipher
from lib.ApiRequest import getpdfpath
from lib.PdfReWrite import pdfrewrite
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


#os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/<asepth>', methods=['GET'])
def get_pdf(asepth):

    # 폰트 등록
    pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
    # 암호화된 내용을 복호화
    aesdec = AESCipher().decrypt(asepth)
    # 복호화 한 내용을 API 에 맞게 replace
    #aesdec = "detail_seq=" + aesdec.replace("//", "&partner_code=") # 실제로쓰이는것
    aesdec = "detail_seq=482050365&partner_code=112555" # 임시
    # 상세 내역을 갖고 오는 API 호출
    pathobj = getpdfpath(aesdec)
    filename_output = pdfrewrite(pathobj, app.config['UPLOAD_FOLDER'])

    return render_template("viewer.html", title="123", link=os.path.join(app.config['UPLOAD_FOLDER'], filename_output))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500)