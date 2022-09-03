import csv
import re
from icalendar import Calendar, Event
from datetime import datetime, timedelta
###setup###
start_day = datetime.strptime('2022/9/1', '%Y/%m/%d')
week_num = 19
time_table = [
    (),
    ('08:00', '08:45'),							
    ('08:50', '09:35'),							
    ('09:50', '10:35'),		
    ('10:40', '11:25'),					
    ('11:30', '12:15'),							
    ('14:00', '14:45'),
    ('14:50', '15:35'),			
    ('15:50', '16:35'),		
    ('16:40', '17:25'),					
    ('17:30', '18:15'),							
    ('19:00', '19:45'),	
    ('19:50', '20:35'),					
    ('20:40', '21:25'),						
    ('21:30', '22:15'),
]
###########
indexs = ['', '星期一','星期二','星期三','星期四','星期五','星期六','星期日']
startday_index = start_day.weekday()+1

class Course:
    def __init__(self, name, teacher, start_week, end_week, day, start_time, end_time, location):
        """
        Args:
            name (str): 课程名称
            teacher (str): 任课教师
            start_week (int): 开始周（包含）
            end_week (int): 结束周（包含）
            day (int): 星期（星期一：1，星期日：7）
            start_time (tuple): 课程开始时间，元组第一个元素为小时，第二个元素为分钟
            end_time (tuple): 课程结束时间，元组第一个元素为小时，第二个元素为分钟
            location (str): 上课位置
        """        
        self.name = name
        self.teacher = teacher
        self.start_week = start_week
        self.end_week = end_week
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        
class CourseCalendar:
    def __init__(self):
        self.courses = []
    def read_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as fp:
            reader = csv.reader(fp)
            for row in reader:
                if row[2]=='在线课程':
                    continue
                name = row[1]
                teacher = row[7]
                #一周多节课的情况
                if name == '':
                    name = self.courses[-1].name
                    teacher = self.courses[-1].teacher
                text = row[10]
                course_info = re.findall('([0-9]+)-([0-9]+)周 ([\u4e00-\u9fa5]+)\[([0-9]+)-([0-9]+)节\](.*)', text)[0]
                #[('2', '17', '星期四', '6', '7', '（三）402')]
                course = Course(name,
                                teacher, 
                                int(course_info[0]), 
                                int(course_info[1]), 
                                indexs.index(course_info[2]), 
                                time_table[int(course_info[3])][0].split(':'), 
                                time_table[int(course_info[4])][1].split(':'),
                                course_info[5])
                self.courses.append(course)
    def export_ics(self, path):
        cal = Calendar()
        for course in self.courses:
            for week in range(course.start_week, course.end_week+1):
                e = Event()
                e.add(
                    "description",
                    '课程名称：' + course.name +
                    ';上课地点：' + course.location +
                    ';教师：' + course.teacher
                )
                e.add(
                    "summary",
                    course.name+'@'+course.location
                )
                if week == 1:
                    date = start_day+timedelta(days = course.day-startday_index)
                elif week >=2:
                    date = start_day+timedelta(days = (7-startday_index) + (week-2)*7 + course.day)
                else:
                    raise(Exception)
                e.add(
                    "dtstart",
                    date.replace(
                        hour=int(course.start_time[0]),
                        minute=int(course.start_time[1])
                    )
                )
                e.add(
                    "dtend",
                    date.replace(
                        hour=int(course.end_time[0]),
                        minute=int(course.end_time[1])
                    )
                )
                cal.add_component(e)
        with open(path, 'wb') as fp:
            fp.write(cal.to_ical())
        print('complete!')

if __name__ == '__main__':
    cal = CourseCalendar()
    cal.read_csv('cal.csv')
    cal.export_ics('课程表.ics')

