import re
from datetime import datetime
from poppler import load_from_data

class KarneData():
    """
    Karne data structure:
    {
        "university": university,
        "major": major,
        "student_id": student_id,
        "name": name,
        "surname": surname,
        "signup_date": signup_date,
        "print_date": print_date,
        "terms": [[{ 
                    "lecture_code": lecture_code[j],
                    "lecture_name": lecture_name[j],
                    "date_taken": date_taken[j],
                    "semester_taken": semester_taken[j],
                    "credit": credit[j],
                    "grade_letter": grade_letter[j],
                    "grade_multiplier": grade_multiplier[j],
                    "points": points[j]
                },
                ...
            ],
            ...
        ]
        "grad_date": grad_date
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
        student_id = re.findall('Öğrenci No : [0-9]{10}', pg_txt)[0].split(' : ')[1]
        name = re.findall('Adı : .+?(?= Mezuniyet Tarihi)', pg_txt)[0].split(' : ')[1]
        surname = re.findall('Soyadı : .+?(?= Bölüm\/Program)', pg_txt)[0].split(' : ')[1]
        signup_date = datetime.strptime(
            re.findall('Kayıt Tarihi : [0-9]{2}\.[0-9]{2}\.[0-9]{4}', pg_txt)[0].split(' : ')[1],
            '%d.%m.%Y').date()
        print_date = datetime.strptime(
            re.findall('Basım Tarihi : [0-9]{2}\.[0-9]{2}\.[0-9]{4}', pg_txt)[0].split(' : ')[1],
            '%d.%m.%Y').date()

        output = {
            "university": university,
            "major": major,
            "student_id": student_id,
            "name": name,
            "surname": surname,
            "signup_date": signup_date,
            "print_date": print_date
        }

        semester_array = []
        for i in range(8):
            lectures = re.findall(f'(?s)Dönemi : {i+1}\n(.*?)\nDönemi : {i+2}', pg_txt)[0]
            lecture_code = re.findall('^[\S]{3} ?[0-9]{3}', lectures, re.M)
            lecture_name = re.findall('(?:(?<=[\S]{3} [0-9]{3} )|(?<=[\S]{3}[0-9]{3} )).*(?= [0-9]{4})', lectures)
            date_taken = re.findall('[0-9]{4}-[0-9]{4}', lectures)
            semester_taken = re.findall('\([0-9]\-[\S]{3,5}\)', lectures)
            credit = re.findall('[0-9],0(?:(?= [A-F]{2})|(?= BL))', lectures)
            grade_letter = [x.strip(' ') for x in re.findall(' [A-F]{2} | BL ', lectures)]
            grade_multiplier = re.findall('[0-9]\.[0-9]{2}', lectures)
            points = re.findall('[0-9]{1,2},[0-9]{2}$', lectures, re.M)

            lectures_array = []
            for j in range(len(lecture_code)):
                lectures_dict = { "lecture_code": lecture_code[j],
                                    "lecture_name": lecture_name[j],
                                    "date_taken": date_taken[j],
                                    "semester_taken": semester_taken[j],
                                    "credit": credit[j],
                                    "grade_letter": grade_letter[j],
                                    "grade_multiplier": grade_multiplier[j],
                                    "points": points[j]
                                }
                lectures_array.append(lectures_dict)

            semester_array[i] = lectures_array
                
        output.update({"terms": semester_array})
        return output
