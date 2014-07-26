import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2= 'default_guestbook2'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MemberOnePage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
           'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('member1.htm')
        self.response.write(template.render(template_values))



class MemberTwoPage(webapp2.RequestHandler):
    
    def get(self):
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {

            'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('member2.html')
        self.response.write(template.render(template_values))



class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(20)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        template_values = {

            'user_name': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('guestbookhome.html')
        self.response.write(template.render(template_values))



class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


class Guestbook1(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/1?'  + urllib.urlencode(query_params))

class Guestbook2(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/module-1/2?' + urllib.urlencode(query_params))









#THESIS

class Thesis(ndb.Model):
    thesis_title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    school_year = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)



class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        template_values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_add.html')
        self.response.write(template.render(template_values))

    def post(self):
        thesis = Thesis()
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.description = self.request.get('description')
        thesis.school_year = self.request.get('school_year')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/success')



class ThesisListHandler(webapp2.RequestHandler):

    def get(self):
    

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        thesis = Thesis.query().fetch()
        
        template_values = {
            'user_name': users.get_current_user(),
            "all_thesis": thesis,
            'url_linktext': url_linktext,
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_records.html')
        self.response.write(template.render(template_values))


class ThesisView(webapp2.RequestHandler):
    def get(self,thesis_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        all_thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        template_values = {
            'all_thesis': all_thesis,
            'id': thesis_id,
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_view.html')
        self.response.write(template.render(template_values))


class ThesisEdit(webapp2.RequestHandler):
    def get(self, thesis_id):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        all_thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        template_values = {
            'all_thesis': all_thesis,
            'id': thesis_id,
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('thesis_edit.html')
        self.response.write(template.render(template_values))


    def post(self,thesis_id):
        thesis_id = int(thesis_id)
        thesis = Thesis.get_by_id(thesis_id)
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.description = self.request.get('description')
        thesis.school_year = self.request.get('school_year')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/success')


class ThesisSuccessPageHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('success.html')
        self.response.write(template.render())


# THESIS END








#ADVISER

class Adviser(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    firstname = ndb.StringProperty(indexed=False)
    middlename = ndb.StringProperty(indexed=False)
    lastname = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    num = ndb.StringProperty(indexed=False)
    dept = ndb.StringProperty(indexed=False)



class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'
        
        template_values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_new.html')
        self.response.write(template.render(template_values))

    def post(self):
        adviser = Adviser()
        adviser.title = self.request.get('title')
        adviser.firstname = self.request.get('firstname')
        adviser.middlename = self.request.get('middlename')
        adviser.lastname = self.request.get('lastname')
        adviser.email = self.request.get('email')
        adviser.num = self.request.get('num')
        adviser.dept = self.request.get('dept')
        adviser.put()
        self.redirect('/adviser/success')


class AdviserListHandler(webapp2.RequestHandler):

    def get(self):
        adviser = Adviser.query().fetch()
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        template_values = {
            "all_adviser": adviser,
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,        
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_list.html')
        self.response.write(template.render(template_values))


class AdviserView(webapp2.RequestHandler):
    def get(self,adviser_id):

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'
        
        all_adviser = Adviser.query().fetch()
        adviser_id = int(adviser_id)

        template_values = {
            'all_adviser': all_adviser,
            'id': adviser_id,
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,  
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_view.html')
        self.response.write(template.render(template_values))


class AdviserEdit(webapp2.RequestHandler):
    def get(self,adviser_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'


        all_adviser = Adviser.query().fetch()
        adviser_id = int(adviser_id)

        values = {
            'all_adviser': all_adviser,
            'id': adviser_id,
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url, 
        }

        template = JINJA_ENVIRONMENT.get_template('adviser_edit.html')
        self.response.write(template.render(values))

    def post(self, adviser_id):
        adviser_id = int(adviser_id)
        adviser = Adviser.get_by_id(adviser_id)
        adviser.title = self.request.get('title')
        adviser.firstname = self.request.get('firstname')
        adviser.middlename = self.request.get('middlename')
        adviser.lastname = self.request.get('lastname')
        adviser.email = self.request.get('email')
        adviser.num = self.request.get('num')
        adviser.dept = self.request.get('dept')
        adviser.put()
        self.redirect('/adviser/success')



class AdviserSuccessPageHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successadviser.html')
        self.response.write(template.render())



#ADVISER END








#Student


class Student(ndb.Model):
    first_name = ndb.StringProperty(indexed=False)
    middle_name = ndb.StringProperty(indexed=False)    
    last_name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    stud_num = ndb.StringProperty(indexed=False)
    numb = ndb.StringProperty(indexed=False)
    college = ndb.StringProperty(indexed=False)



class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
        }
        template = JINJA_ENVIRONMENT.get_template('student_new.html')
        self.response.write(template.render(values))

    def post(self):
        student = Student()
        student.first_name = self.request.get('first_name')
        student.middle_name = self.request.get('middle_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.stud_num = self.request.get('stud_num')
        student.numb = self.request.get('numb')
        student.college = self.request.get('college')
        student.put()
        self.redirect('/student/success')


class StudentListHandler(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        students = Student.query().fetch()

        template_values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
            "all_students": students
        }

        template = JINJA_ENVIRONMENT.get_template('student_records.html')
        self.response.write(template.render(template_values))


class StudentView(webapp2.RequestHandler):
    def get(self,students_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        all_students = Student.query().fetch()
        students_id = int(students_id)

        values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
            'all_students': all_students,
            'id': students_id
        }

        template = JINJA_ENVIRONMENT.get_template('student_view.html')
        self.response.write(template.render(values))

class StudentEdit(webapp2.RequestHandler):
    def get(self,students_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Log out'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Log In'

        all_students = Student.query().fetch()
        students_id = int(students_id)

        values = {
            'user_name': users.get_current_user(),
            'url_linktext': url_linktext,
            'url': url,
            'all_students': all_students,
            'id': students_id
        }

        template = JINJA_ENVIRONMENT.get_template('student_edit.html')
        self.response.write(template.render(values))

    def post(self, students_id):
        students_id = int(students_id)
        student = Student.get_by_id(students_id)
        student.first_name = self.request.get('first_name')
        student.middle_name = self.request.get('middle_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.stud_num = self.request.get('stud_num')
        student.numb = self.request.get('numb')
        student.college = self.request.get('college')
        student.put()
        self.redirect('/student/success')


class StudentSuccessPageHandler(webapp2.RequestHandler):
    
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successstud.html')
        self.response.write(template.render())


#Student End





application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),

    ('/thesis/new', ThesisNewHandler),
    ('/success', ThesisSuccessPageHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/view/(\d+)', ThesisView),
    ('/thesis/edit/(\d+)', ThesisEdit),

    ('/adviser/new', AdviserNewHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserView),
    ('/adviser/edit/(\d+)', AdviserEdit),
    ('/adviser/success', AdviserSuccessPageHandler),

    ('/student/new', StudentNewHandler),
    ('/student/success', StudentSuccessPageHandler),
    ('/student/list', StudentListHandler),
    ('/student/view/(\d+)', StudentView),
    ('/student/edit/(\d+)', StudentEdit)

], debug=True)
