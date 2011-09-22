import web
from web import form


class MyInput(form.Input):

    def validate(self, value):
        self.set_value(value)
        for v in self.validators:
            if not v.valid(value):
                self.note = v.msg
                if self.note.find('${') != -1:
                    if self.note.find('${name}') != -1:
                        self.note = self.note.replace('${name}', self.name)
                    if self.note.find('${description}') != -1:
                        self.note = self.note.replace('${description}', self.description)
                return False
        return True

class MyTextbox(MyInput):
    def get_type(self):
        return 'text'


class MyPassword(MyInput):
    def get_type(self):
        return 'password'
