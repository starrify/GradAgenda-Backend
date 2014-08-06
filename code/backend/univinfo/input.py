from backend.univinfo.models import University, Major, Semester
from datetime import date

def inputUniversities():
	University.objects.create(id = 1, shortname = 'Unknown', fullname = 'Unknown')
	University.objects.create(id = 2, shortname = 'PU', fullname = 'Purdue University, West Lafayette')
	University.objects.create(id = 3, shortname = 'UCB', fullname = 'University of California, Berkeley')
	University.objects.create(id = 4, shortname = 'UNC Charlotte', fullname = 'University of North Carolina, Charlotte')
	University.objects.create(id = 5, shortname = 'UNC Chapel Hill', fullname = 'University of North Carolina, Chapel Hill')
	University.objects.create(id = 6, shortname = 'UMich Ann Arbor', fullname = 'University of Michigan, Ann Arbor')
	University.objects.create(id = 7, shortname = 'MSU', fullname = 'Michigan State University')
	University.objects.create(id = 8, shortname = 'CU', fullname = 'Columbia University In The City of New York')
	University.objects.create(id = 9, shortname = 'UIUC', fullname = 'University of Illinois, Urbana Champaign')
	University.objects.create(id = 10, shortname = 'UIC', fullname = 'University of Illinois, Chicago')
	University.objects.create(id = 11, shortname = 'UMN Twin Cities', fullname = 'University of Minnesota, Twin Cities')
	University.objects.create(id = 12, shortname = 'Duke', fullname = 'Duke University')
	University.objects.create(id = 13, shortname = 'Cornell', fullname = 'Cornell University')
	University.objects.create(id = 14, shortname = 'Emory', fullname = 'Emory University')

def inputMajors():
	Major.objects.create(id = 1, shortname = 'Unknown', fullname = 'Unknown')
	Major.objects.create(id = 2, shortname = 'CS', fullname = 'Computer Science')

def inputSemesters():
	Semester.objects.create(id = 1, name = 'summer-2014', university = University.objects.get(shortname='UCB'), start = date(2014,6,1), end = date(2014,8,31))