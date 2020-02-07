import re
import requests
course_ids = range(6158,6185)

class Course():
    def __init__(self,course_id:int):
        self.listen_code = "3KNOTl"
        self.base_URL = "https://school.jledu.com/front/demand/play/"
        self.page_URL = ''
        self.page_data = ''
        self.mp4_URL = ''
        self.title = ''
        self.course_id = course_id

    def 凎(self):
        self.page_URL = self.base_URL + str(self.course_id) + "/" + self.listen_code + "/"
        
        #GET mp4_URL AND TITLE
        r = requests.get(self.page_URL)
        text = r.text
        self.mp4_URL = re.findall("https.*mp4",text)[0]
        self.title = re.findall("<p class=\"title\">.*</p>",text)[0][17:][:-4]

        #GENERATE HEADERS
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': self.page_URL
        }

        #DOWNLOAD AND SAVE FILE
        local_path = "F:\\netClass\\"
        local_file_name = local_path + self.title + ".mp4"
        print("Downloading {}.mp4".format(self.title))
        r = requests.get(self.mp4_URL,headers=self.headers)
        print("Saving {}.mp4".format(self.title))
        with open(local_file_name, 'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    for course_id in course_ids:
        cour = Course(course_id)
        cour.凎()