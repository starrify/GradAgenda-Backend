#!/usr/bin/env python
"""Processor of curriculum for UC Berkeley"""

# TODO: complete the license and version info
__author__ = 'Ji YANG'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Ji YANG']
__license__ = ''
__version__ = ''
__maintainer__ = 'Ji YANG'
__email__ = 'yangji9181@163.com'
__status__ = 'development'

_wdaylist = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']

def process(data, semester, user):
    try:
        university = University.objects.get(shortname='UCB')
    except University.DoesNotExist:
        ret = produceRetCode('fail', 'run inputunivinfo first')
        return ret
    try:
        semester = Semester.objects.get(name=semester, university=university)
    except Semester.DoesNotExist:
        ret = produceRetCode('fail', 'semester data error')
        return ret
    classes = data['classes']
    for classdata in classes:
        try:
            course = Course.objects.get(fullname=classdata['title'], shortname=classdata['course_code'], university=University.objects.get(shortname=university), department = classdata['dept'])
        except Course.DoesNotExist:
            course = Course(fullname=classdata['title'], shortname=classdata['course_code'], university=university, department = classdata['dept'])
            course.save()
        sections = classdata['sections']
        for sectiondata in sections:
            try:
                section = Section.objects.get(name=sectiondata['section_label'], unit=sectiondata['unit'], semester=semester, course=course)
            except Section.DoesNotExist:              
                section = Section(name=sectiondata['section_label'], unit=sectiondata['unit'], semester=semester, course=course, start=semester.start, end=semester.end)
                professors = sectiondata['instructors']
                for professordata in professors:
                    name = professordata['name'].partition(' ')
                    try:
                        professor = Professor.objects.get(first_name=name[0], last_name=name[2])
                    except Professor.DoesNotExist:
                        professor = Professor(first_name=name[0], last_name=name[2], university=university)
                        professor.save()
                    section.professor.add(professor)
                section.save()
                lectures = sectiondata['schedules']
                for lecturedata in lectures:
                    schedule = lecturedata['schedule']
                    tups = schedule.split(' ')
                    for i in range(0, tups.count, 2):
                        timetup = tups[i+1].partition('-')
                        start = time.strptime(timetup[0]+'M', '%I:%M%p')
                        end = time.strptime(timetup[2]+'M', '%I:%M%p')
                        daytup = tups[i]
                        weekday = 0
                        for wday in _wdaylist:
                            weekday = weekday + 1
                            if daytup.find(wday) != -1:
                                Lecture.objects.create(section=section, weekday=weekday, starttime=start, endtime=end, location=lecturedata['buildingName']+' '+lecturedata['roomNumber'])
            try:
                courseitem = CourseItem.objects.get(user=user, section=section)
            except CourseItem.DoesNotExist:
                courseitem = CourseItem(user=user, section=section)
                courseitem.save()
    ret = produceRetCode("success")


