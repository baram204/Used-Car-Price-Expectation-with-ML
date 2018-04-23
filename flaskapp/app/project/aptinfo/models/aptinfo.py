from project import db

class AptInfo(db.Model):
    __tablename__ = '아파트정보'

    index= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    법정동코드 = db.Column(db.String(10), unique=False, nullable=False, default='')
    아파트코드 = db.Column(db.String(10), unique=False, nullable=False, default='')
    아파트이름 = db.Column(db.String(51), unique=False, nullable=False, default='')
    마을코드 =  db.Column(db.Integer, unique=False, nullable=False, default=0)
    법정동주소 = db.Column(db.String(200), unique=False, nullable=False, default='')
    도로명주소 = db.Column(db.String(200), unique=False, nullable=False, default='')

    단지분류 = db.Column(db.String(51), unique=False, nullable=False, default='')

    동수 = db.Column(db.String(100), unique=False, nullable=False, default='')
    세대수 = db.Column(db.Integer, unique=False, nullable=False, default=0)

    전용면적60이하아파트코드 = db.Column(db.String(52), unique=False, nullable=False, default='')
    전용면적60이하세대수 = db.Column(db.Integer, unique=False, nullable=False, default=0)
    전용면적60이상85이하아파트코드 = db.Column(db.String(52), unique=False, nullable=False, default='')
    전용면적60이상85이하세대수 = db.Column(db.Integer, unique=False, nullable=False, default=0)
    전용면적85이상135이하아파트코드 = db.Column(db.String(52), unique=False, nullable=False, default='')
    전용면적85이상135이하세대수 = db.Column(db.Integer, unique=False, nullable=False, default=0)
    전용면적135초과아파트코드 = db.Column(db.String(52), unique=False, nullable=False, default='')
    전용면적135초과세대수 = db.Column(db.Integer, unique=False, nullable=False, default=0)

    분양형태	= db.Column(db.String(52), unique=False, nullable=False, default='')
    난방방식	= db.Column(db.String(52), unique=False, nullable=False, default='')
    복도유형	= db.Column(db.String(52), unique=False, nullable=False, default='')

    연면적	= db.Column(db.Float, unique=False, nullable=False, default=0)

    시공사 = db.Column(db.String(100), unique=False, nullable=False, default='')
    시행사 = db.Column(db.String(100), unique=False, nullable=False, default='')

    관리사무소연락처	= db.Column(db.String(53), unique=False, nullable=False, default='')
    관리사무소팩스	= db.Column(db.String(53), unique=False, nullable=False, default='')
    홈페이지주소	= db.Column(db.String(100), unique=False, nullable=False, default='')

    일반관리방식 = db.Column(db.String(54), unique=False, nullable=False, default='')
    일반관리인원 = db.Column(db.String(52), unique=False, nullable=False, default='')
    일반관리계약업체  	= db.Column(db.String(100), unique=False, nullable=False, default='')

    경비관리방식	= db.Column(db.String(54), unique=False, nullable=False, default='')
    경비관리인원	= db.Column(db.String(52), unique=False, nullable=False, default='')
    경비관리계약업체 	= db.Column(db.String(100), unique=False, nullable=False, default='')

    청소관리방식	= db.Column(db.String(54), unique=False, nullable=False, default='')
    청소관리인원	= db.Column(db.String(52), unique=False, nullable=False, default='')
    음식물처리방법 	= db.Column(db.String(100), unique=False, nullable=False, default='')

    소독관리방식	= db.Column(db.String(54), unique=False, nullable=False, default='')
    연간소독횟수  = db.Column(db.String(54), unique=False, nullable=False, default='')
    소독방법	= db.Column(db.String(54), unique=False, nullable=False, default='')

    승강기관리형태  	= db.Column(db.String(55), unique=False, nullable=False, default='')
    승객용승강기 = db.Column(db.String(54), unique=False, nullable=False, default='')
    화물용승강기 = db.Column(db.String(54), unique=False, nullable=False, default='')
    비상승강기 = db.Column(db.String(54), unique=False, nullable=False, default='')
    주차관제홈네트워크  	= db.Column(db.String(58), unique=False, nullable=False, default='')

    건물구조  	= db.Column(db.String(100), unique=False, nullable=False, default='')
    세대전기계약방식  	= db.Column(db.String(55), unique=False, nullable=False, default='')
    화재수신반방식  	= db.Column(db.String(55), unique=False, nullable=False, default='')


    지상주차장대수 = db.Column(db.String(57), unique=False, nullable=False, default='')
    지하주차장대수 = db.Column(db.String(57), unique=False, nullable=False, default='')

    cctv대수  	= db.Column(db.String(57), unique=False, nullable=False, default='')
    부대복리시설  	= db.Column(db.String(70), unique=False, nullable=False, default='')
    수전용량  	= db.Column(db.String(57), unique=False, nullable=False, default='')
    전기안전관리자법정선임여부  	= db.Column(db.String(57), unique=False, nullable=False, default='')
    급수방식  	= db.Column(db.String(57), unique=False, nullable=False, default='')



    버스정류장 	= db.Column(db.String(51), unique=False, nullable=False, default='')
    편의시설  	= db.Column(db.String(100), unique=False, nullable=False, default='')
    교육시설  	= db.Column(db.String(100), unique=False, nullable=False, default='')


    사용승인일	= db.Column(db.String(51), unique=False, nullable=False, default='')
    주거전용면적 = db.Column(db.Float, unique=False, nullable=False, default=0)

    인근지하철역	= db.Column(db.String(50), unique=False, nullable=False, default='')
    인근지하철호선	= db.Column(db.String(50), unique=False, nullable=False, default='')
    지하철까지시간 	= db.Column(db.String(50), unique=False, nullable=False, default='')


    def __repr__(self):
        rtform = """<AptInfo(아파트코드 = '%s',
        마을코드 = '%s',
        법정동주소 = '%s',
        도로명주소 = '%s',
        세대수 = '%s',
        전용면적60이하세대수 = '%s',
        전용면적60이상85이하세대수 = '%s',
        전용면적85이상135이하세대수 = '%s',
        전용면적135초과세대수 = '%s',
        전용면적60이하아파트코드 = '%s',
        전용면적60이상85이하아파트코드 = '%s',
        전용면적85이상135이하아파트코드 = '%s',
        전용면적135초과아파트코드 = '%s',
        아파트이름 = '%s',
        분양형태 = '%s',
        난방방식 = '%s',
        연면적 = '%s',
        동수 = '%s',
        시공사 = '%s',
        시행사 = '%s',
        관리사무소연락처 = '%s',
        관리사무소팩스 = '%s',
        홈페이지주소 = '%s',
        단지분류 = '%s',
        일반관리방식 = '%s',
        일반관리인원 = '%s',
        일반관리계약업체 = '%s',
        경비관리방식 = '%s',
        경비관리인원 = '%s',
        경비관리계약업체 = '%s',
        청소관리방식 = '%s',
        청소관리인원 = '%s',
        음식물처리방법 = '%s',
        소독관리방식 = '%s',
        연간소독횟수 = '%s',
        소독방법 = '%s',
        건물구조 = '%s',
        세대전기계약방식 = '%s',
        화재수신반방식 = '%s',
        승강기관리형태 = '%s',
        지상주차장대수 = '%s',
        지하주차장대수 = '%s',
        cctv대수 = '%s',
        부대복리시설 = '%s',
        수전용량 = '%s',
        전기안전관리자법정선임여부 = '%s',
        급수방식 = '%s',
        승객용승강기 = '%s',
        화물용승강기 = '%s',
        비상승강기 = '%s',
        주차관제홈네트워크 = '%s',
        버스정류장 = '%s',
        편의시설 = '%s',
        교육시설 = '%s',
        복도유형 = '%s',
        사용승인일 = '%s',
        주거전용면적 = '%s',
        인근지하철역 = '%s',
        인근지하철호선 = '%s',
        지하철까지시간 = '%s',)>"""

        return rtform % (
            self.아파트코드,
            self.마을코드,
            self.법정동주소,
            self.도로명주소,
            self.세대수,
            self.전용면적60이하세대수,
            self.전용면적60이상85이하세대수,
            self.전용면적85이상135이하세대수,
            self.전용면적135초과세대수,
            self.전용면적60이하아파트코드,
            self.전용면적60이상85이하아파트코드,
            self.전용면적85이상135이하아파트코드,
            self.전용면적135초과아파트코드,
            self.아파트이름,
            self.분양형태,
            self.난방방식,
            self.연면적,
            self.동수,
            self.시공사,
            self.시행사,
            self.관리사무소연락처,
            self.관리사무소팩스,
            self.홈페이지주소,
            self.단지분류,
            self.일반관리방식,
            self.일반관리인원,
            self.일반관리계약업체,
            self.경비관리방식,
            self.경비관리인원,
            self.경비관리계약업체,
            self.청소관리방식,
            self.청소관리인원,
            self.음식물처리방법,
            self.소독관리방식,
            self.연간소독횟수,
            self.소독방법,
            self.건물구조,
            self.세대전기계약방식,
            self.화재수신반방식,
            self.승강기관리형태,
            self.지상주차장대수,
            self.지하주차장대수,
            self.cctv대수,
            self.부대복리시설,
            self.수전용량,
            self.전기안전관리자법정선임여부,
            self.급수방식,
            self.승객용승강기,
            self.화물용승강기,
            self.비상승강기,
            self.주차관제홈네트워크,
            self.버스정류장,
            self.편의시설,
            self.교육시설,
            self.복도유형,
            self.사용승인일,
            self.주거전용면적,
            self.인근지하철역,
            self.인근지하철호선,
            self.지하철까지시간)

