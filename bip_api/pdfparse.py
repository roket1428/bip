import re
from datetime import datetime
from poppler import load_from_data

class KarneParser():
    """
    Karne data structure:
    {
        "university": str,
        "major": str,
        "student_id": int,
        "name": str,
        "surname": str,
        "signup_date": Date(),
        "print_date": Date(),
        "gno": float,
        "credit_sum": float,
        "points_sum": float,
        "terms": [[{ 
                    "lecture_code": str,
                    "lecture_name": str,
                    "date_taken": Date(),
                    "semester_taken": Date(),
                    "credit": float,
                    "grade_letter": str,
                    "grade_multiplier": float,
                    "points": float
                },
                ...
            ],
            ...
        ]
    }
    """
    def __init__(self, file_data):
        self.pdf = load_from_data(file_data)
        self.page_1 = self.pdf.create_page(0)
        self.page_2 = self.pdf.create_page(1)

    def filter_txt(self, pg_txt):
        pg_txt = re.sub(r' +', ' ', pg_txt)
        pg_txt = re.sub(r'\n+ ?', '\n', pg_txt)
        pg_txt = re.sub(r'(?s)1 \/ 2.+?(?=Dönemi)', '', pg_txt)
        pg_txt = re.sub(r'Ders.*\n', '', pg_txt)
        pg_txt = re.sub(r'[\s\S]*KARNE\n', '', pg_txt)
        pg_txt = re.sub(r'\nGenel Not', '\nDönemi : 9\nGenel Not', pg_txt)
        pg_txt = re.sub(r'(?s)(?<=Genel Toplam [0-9]{3},[0-9] [0-9]{3},[0-9]{2}).+', '', pg_txt)
       
        return pg_txt

    def parse(self):
        pg_txt = self.filter_txt(self.page_1.text() + self.page_2.text())

        university = re.findall('Fakülte\/Yüksekokul : .*', pg_txt)[0].split(' : ')[1]
        major = re.findall('Bölüm\/Program : .*', pg_txt)[0].split(' : ')[1]
        student_id = int(re.findall('Öğrenci No : [0-9]{10}', pg_txt)[0].split(' : ')[1])
        name = re.findall('Adı : .+?(?= Mezuniyet Tarihi)', pg_txt)[0].split(' : ')[1]
        surname = re.findall('Soyadı : .+?(?= Bölüm\/Program)', pg_txt)[0].split(' : ')[1]
        signup_date = datetime.strptime(
            re.findall('Kayıt Tarihi : [0-9]{2}\.[0-9]{2}\.[0-9]{4}', pg_txt)[0].split(' : ')[1],
            '%d.%m.%Y').date()
        print_date = datetime.strptime(
            re.findall('Basım Tarihi : [0-9]{2}\.[0-9]{2}\.[0-9]{4}', pg_txt)[0].split(' : ')[1],
            '%d.%m.%Y').date()
        gno = float(re.findall(r'(?<=Genel Not Ortalaması )[0-9],[0-9]{2}', pg_txt)[0].replace(",", "."))
        credits_sum = float(re.findall(r'(?<=Genel Toplam )[0-9]{3},[0-9]', pg_txt)[0].replace(",", "."))
        points_sum = float(re.findall(r'(?<=Genel Toplam [0-9]{3},[0-9] )[0-9]{3},[0-9]{2}', pg_txt)[0].replace(",", "."))

        output = {
            "university": university,
            "major": major,
            "student_id": student_id,
            "name": name,
            "surname": surname,
            "signup_date": signup_date,
            "print_date": print_date,
            "gno": gno,
            "credits_sum": credits_sum,
            "points_sum": points_sum
        }

        semester_array = [None] * 8
        for i in range(8):
            lectures = re.findall(f'(?s)Dönemi : {i+1}\n(.*?)\nDönemi : {i+2}', pg_txt)[0]
            lecture_code = [x.replace(" ", "") for x in re.findall('^[\S]{3} ?[0-9]{3}', lectures, re.M)]
            lecture_name = re.findall('(?:(?<=[\S]{3} [0-9]{3} )|(?<=[\S]{3}[0-9]{3} )).*(?= [0-9]{4})', lectures)
            date_taken = re.findall('[0-9]{4}-[0-9]{4}', lectures)
            semester_taken = re.findall('\([0-9]\-[\S]{3,5}\)', lectures)
            credits = [float(x.replace(",", ".")) for x in re.findall('[0-9],0(?:(?= [A-F]{2})|(?= BL))', lectures)]
            grade_letter = [x.strip(' ') for x in re.findall(' [A-F]{2} | BL ', lectures)]
            grade_multiplier = [float(x.replace(",", ".")) for x in re.findall('[0-9]\.[0-9]{2}', lectures)]
            points = [float(x.replace(",", ".")) for x in re.findall('[0-9]{1,2},[0-9]{2}$', lectures, re.M)]

            lectures_array = []
            for j in range(len(lecture_code)):
                lectures_dict = { "lecture_code": lecture_code[j],
                                    "lecture_name": lecture_name[j],
                                    "date_taken": date_taken[j],
                                    "semester_taken": semester_taken[j],
                                    "credits": credits[j],
                                    "grade_letter": grade_letter[j],
                                    "grade_multiplier": grade_multiplier[j],
                                    "points": points[j]
                                }
                lectures_array.append(lectures_dict)

            semester_array[i] = lectures_array
                
        output.update({"terms": semester_array})
        return output

class KarneParserNG():
    """
    KarneNG data structure:
    {
        "university": str,
        "major": str,
        "student_id": int,
        "name": str,
        "surname": str,
        "signup_date": Date(),
        "print_date": Date(),
        "gno": float,
        "credit_sum": float,
        "points_sum": float,
        "terms": {
                "[0-9]{1,2}YY": { 
                    "[A-Z]{3} ?[0-9]{3}": {
                        "lecture_name": str,
                        "date_taken": str,
                        "semester_taken": str,
                        "credits": float,
                        "akts": float,
                        "grade_letter": str,
                    },
                    ...
                },
                ...
            }
        "exempt": {
            "[A-Z]{3} ?[0-9]{3}": {
                "lecture_name": str,
                "credits": float,
                "akts": float,
                "grade_letter": str
            }
        }
    }
    """
    def __init__(self, data):
        self.pdf = load_from_data(data)
        self.page_1 = self.pdf.create_page(0)
        self.page_2 = self.pdf.create_page(1)
        self.page_3 = self.pdf.create_page(2)

    def parse(self):
        pg_txt = self.filter_txt(self.page_1.text() + self.page_2.text() + self.page_3.text())
        
        university = None
        major = None
        student_id = None
        # üni ve bölüm ismi 2 satır kapladığı için indexlere ihtiyacımız var
        lines = pg_txt.split('\n')
        for i, v in enumerate(lines):
            uni_match = re.search(r'Birim:', v)
            maj_match = re.search(r'Bölüm:', v)
            if uni_match != None:
                # ilk parametre tc olduğu için kullanmıyoruz
                university = lines[i-1] + ' ' + v.split('%_%_%')[1].split(':')[1]
            elif maj_match != None:
                # filtrelenmiş metinde öğrenci no bölüm ile aynı satırda geliyor
                student_id = int(v.split('%_%_%')[0].split(':')[1])
                major = lines[i-1] + ' ' + v.split('%_%_%')[1].split(':')[1]

        name_match = re.findall('Adı Soyadı:.*', pg_txt)[0].split(':')[1].split(' ')
        name = " ".join(name_match[:-1])
        surname = name_match[-1]
        signup_date = datetime.strptime(
            re.findall(r'Kayıt Tarihi:.*', pg_txt)[0].split(':')[1], '%d.%m.%Y').date()
        print_date = datetime.strptime(
            re.findall(r'[0-9]/[0-9]/[0-9]{4}', pg_txt)[0], '%d/%m/%Y').date()
        gno = float(re.findall(r'Not Ortalaması:.*$', pg_txt, re.M)[0].split(':')[1])

        sum_match = re.findall(r'Birikimli.*', pg_txt)[0].split('#_#_#')
        if sum_match[1] != '':
            inner_vars = sum_match[1].split('%_%_%')
            credits_sum = float(inner_vars[1].split('|')[1])
            points_sum = float(inner_vars[3])
        else:
            inner_vars = sum_match[0].split('%_%_%')
            credits_sum = float(inner_vars[1].split('|')[1])
            points_sum = float(inner_vars[3])

        exempt_dict = {}
        exempt_match = re.findall(r'(?s)(?<=Muaf Dersleri#_#_#\n).*?(?=\n1\.)', pg_txt)
        if exempt_match != []:
            exempt_filtered = re.sub(r"[0-9]{0,}#_#_#", "", exempt_match[0])
            exempt_rows = exempt_filtered.split('\n')
            for row in exempt_rows:
                exempt_cols = row.split('%_%_%')
                exempt_dict[exempt_cols[0]] = {
                    "lecture_name": exempt_cols[1],
                    "credits": float(exempt_cols[2].split(' / ')[0]),
                    "akts": float(exempt_cols[2].split(' / ')[1]),
                    "grade_letter": exempt_cols[3]
                }

        term_match = re.findall(r'(?s)[0-9]{1,2}. YarıYıl.*?(?=\nYYEND)', pg_txt)
        term_dict = {}
        for term in term_match:
            term_rows = term.split('\n')

            # dönem indeksleri ilk satırda bulunuyor
            term_head = term_rows[0].split('#_#_#')
            
            # dosyada dönemler bazen olması gereken sırada çıkmıyor örn: 11-12-14-15-13
            # bu yüzden dönemlerin doğal sırası yerine sırayı regex ile elde etmek gerekiyor
            term_index_col0 = re.findall(r"^[0-9][0-9]?(?=\.)", term_head[0])[0] + "YY"
            term_date_taken_col0 = re.findall(r"(?<=-)[0-9]{4}", term_head[0])[0]
            term_semester_taken_col0 = re.findall(r"(?<=-)[^\r\t\f\n\0-9]{3,5}", term_head[0])[0]

            # 2. sütun var ise dizi 3 elemanlı olacak: ['s1', 's2', '']
            is_second_col_exists = True
            if len(term_head) != 3:
                term_index_col1 = None
                term_date_taken_col1 = None
                term_semester_taken_col1 = None
                is_second_col_exists = False
            else:
                term_index_col1 = re.findall(r"^[0-9][0-9]?(?=\.)", term_head[1])[0] + "YY"
                term_date_taken_col1 = re.findall(r"(?<=-)[0-9]{4}", term_head[1])[0]
                term_semester_taken_col1 = re.findall(r"(?<=-)[^\r\t\f\n\0-9]{3,5}", term_head[1])[0]
            
            col0_dict = {}
            col1_dict = {}
            for row in term_rows[1:]:
                term_columns = row.split('#_#_#')
                col0_data = term_columns[0].split('%_%_%')
                if col0_data[0] != '':
                    if len(col0_data) == 1:
                        # 'KAYIT YENİLEMEDİ' girdisi
                        col0_dict["NOK000"] = {
                            "lecture_name": col0_data[0],
                            "date_taken": None,
                            "semester_taken": None,
                            "credits": None,
                            "akts": None,
                            "grade_letter": None
                        }
                    else:
                        # bazı derslerin harf notları yok >:(
                        try:
                            grade_letter = col0_data[3]
                        except:
                            grade_letter = "XX"

                        col0_dict[col0_data[0]] = {
                            "lecture_name": col0_data[1],
                            "date_taken": term_date_taken_col0,
                            "semester_taken": term_semester_taken_col0,
                            "credits": float(col0_data[2].split('|')[0]),
                            "akts": float(col0_data[2].split('|')[1]),
                            "grade_letter": grade_letter
                        }
                if is_second_col_exists:
                    col1_data = term_columns[1].split('%_%_%')
                    if col1_data[0] != '':
                        if len(col1_data) == 1:
                            col1_dict["NOK000"] = {
                                "lecture_name": col1_data[0],
                                "date_taken": None,
                                "semester_taken": None,
                                "credits": None,
                                "akts": None,
                                "grade_letter": None
                            }
                        else:
                            try:
                                grade_letter = col1_data[3]
                            except:
                                grade_letter = "XX"
                            col1_dict[col1_data[0]] = {
                                "lecture_name": col1_data[1],
                                "date_taken": term_date_taken_col1,
                                "semester_taken": term_semester_taken_col1,
                                "credits": float(col1_data[2].split('|')[0]),
                                "akts": float(col1_data[2].split('|')[1]),
                                "grade_letter": grade_letter
                            }
            term_dict[term_index_col0] = col0_dict
            if is_second_col_exists:
                term_dict[term_index_col1] = col1_dict

        output = {
            "university": university,
            "major": major,
            "student_id": student_id,
            "name": name,
            "surname": surname,
            "signup_date": signup_date,
            "print_date": print_date,
            "gno": gno,
            "credits_sum": credits_sum,
            "points_sum": points_sum,
            "terms": term_dict
        }

        if exempt_match != []:
            output["exempt"] = exempt_dict
        else:
            output["exempt"] = None

        return output

    def filter_txt(self, pg_txt):

        
        # aramayı bozan 'Tabii olduğu müfredat' satırını sil
        pg_txt = re.sub(r"^ *?Tabii.*", "", pg_txt, flags=re.M)
        
        # yarıyıl başlığı ile ders kodları yada 'KAYIT YENİLEMEDİ' arasındaki herşeyi sil (bilgi sütunları)
        pg_txt = re.sub(r"(?s)(?<=[0-9]{4}-[0-9]{4}\n).+?(?:(?=[A-Z]{3} ?[0-9]{3})|(?=KAYIT))", "", pg_txt)

        # garip satır başı karakterini normale döndür
        pg_txt = re.sub(r"\x0c", "\n", pg_txt)
        
        # çoklu satır başlarını düzelt
        pg_txt = re.sub(r"\n+", "\n", pg_txt)

        # belge sonundaki gereksiz kısımı at
        pg_txt = re.sub(r"(?s) +Yüz Puan.*", "", pg_txt)

        # dönem sınırlarından önceki gereksiz bilgileri sil
        pg_txt = re.sub(r".*Alınan Kredi.*\n", "", pg_txt)
        pg_txt = re.sub(r".*Yarıyıl.*\n", "", pg_txt)

        # zorunlu tarih dersi 2 satır kaplıyor onu düzelt
        pg_txt = re.sub(r"TARİHİ I\n +", "TARİHİ I       ", pg_txt)
        pg_txt = re.sub(r"\n +(?=[0-9]\.[0-9]{2})", "       ", pg_txt)

        # satır başlarındaki küçük boşlukları sil x <= 3
        pg_txt = re.sub(r"^ {1,3}", "", pg_txt, flags=re.M)

        # ders kodu öncesi tag '#_#_#' koy
        pg_txt = re.sub(r" (?=[^\r\n\t\f\v\0-9]{3} ?[0-9]{3})", "#_#_#", pg_txt)

        # dönem isimleri arasına tag '#_#_#' koy
        pg_txt = re.sub(r"(?<=Güz [0-9]{4}-[0-9]{4})[ ]{0,}", "#_#_#", pg_txt)

        # dönem sınırlarına YYEND tagı koy
        pg_txt = re.sub(r".*Birikimli.*\n(?!Genel)", "YYEND\n", pg_txt)
        pg_txt = re.sub(r"(?=\nBirikimli)", "\nYYEND", pg_txt)
        
        # 'Müfredatı' satırından sonraki satırları seç
        start_pattern = re.compile(r"Müfredatı")
        match_pattern = start_pattern.search(pg_txt)
        start = match_pattern.end()

        # 2 satırlı ders isimleri ya da açıklamalar gibi gereksiz satırları sil
        pg_tmp = re.sub(r"\n {3,}(?!.*:|.*#).*\b.*\b\.?$", "", pg_txt[start:], flags=re.M)

        # açıklamanın sağ taraftaki veriyi alt satıra yollama uç durumunu düzelt
        lines = pg_tmp.split('\n')
        lengths = [len(line) for line in lines]
        len_avg = sum(lengths) / len(lengths)
        is_lower_than_avg = False
        fmt_lines = []
        index_shift = 0
        for index, line in enumerate(lines):
            if is_lower_than_avg:
                match = re.match(r"^ +", line)
                if match != None and match.end() > 20:
                    fmt_line = re.sub(r"\n +", "       ", lines[index-1] + '\n' + line)
                    if fmt_lines != []:
                        fmt_lines.remove(line)
                        fmt_lines[index-1-index_shift] = fmt_line
                    else:
                        fmt_lines = [l for l in lines if l != line]
                        fmt_lines[index-1] = fmt_line
                    index_shift += 1
            if len(line) < len_avg:
                is_lower_than_avg = True
            else:
                is_lower_than_avg = False

        if fmt_lines != []:
            pg_tmp = '\n'.join(fmt_lines)
        # YYEND satırı dışındaki tüm satırların sonuna #_#_# tagı koy
        pg_tmp = re.sub(r"(?<!YYEND)\n", "#_#_#\n", pg_tmp)

        # kopya tagları düzelt
        pg_tmp = re.sub(r"#_#_##_#_#", "#_#_#", pg_tmp)

        # eğer muaf olduğu dersler varsa bilgi sütununu sil
        pg_tmp = re.sub(r".*Ders Kodu.*\n", "", pg_tmp)

        # '#_#_#' tagının solundaki boşlukları sil
        pg_tmp = re.sub(r"(?<=\w) +(?=#_#_#)", "", pg_tmp)
        pg_txt = pg_txt[:start] + pg_tmp
        
        # iki nokta etrafındaki boşklukları sil
        pg_txt = re.sub(r" {0,}: {0,}", ":", pg_txt)

        # iki sütunda kayıt yenilemedi ise
        pg_txt = re.sub(r"(?<=YENİLEMEDİ) +(?=KAYIT)", "#_#_#", pg_txt)

        # yan çizgi etrafındaki boşklukları sil
        pg_txt = re.sub(r" {1,}- {1,}(?![\S] )", "%_%_%", pg_txt)

        # verileri %_%_% tagı ile değişkenlere böl
        pg_txt = re.sub(r"(?<=[\w]|\)) {5,}(?=[\w])", "%_%_%", pg_txt)

        # sol tarafta tek kalan yarıyıllara da tagı ekle
        pg_txt = re.sub(r"(?<=Güz [0-9]{4}-[0-9]{4})(?=\n)", "%_%_%", pg_txt)

        # tüm soldan boşlukları sil
        pg_txt = re.sub(r"^ +", "", pg_txt, flags=re.M)

        return pg_txt
