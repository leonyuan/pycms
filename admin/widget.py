import web
from web import form


class MyInput(form.Input):

    def __init__(self, name, *validators, **attrs):
        self.required = attrs.pop('required', False)
        super(MyInput, self).__init__(name, *validators, **attrs)

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

    def render(self):
        html = super(MyInput, self).render()
        if self.note:
            html += '<div id="catnameTip" class="onShow">%s</div>' % (self.note,)
        return html


class MyButton(MyInput, form.Button):
    pass

class MyTextbox(MyInput, form.Textbox):
    pass

class MyLongText(MyInput, form.Textarea):
    def render(self):
        html = super(MyLongText, self).render()
        html +='''
        <script type="text/javascript" src="%s/js/ckeditor/ckeditor.js"></script><script type="text/javascript">
                      CKEDITOR.replace( '%s',{language:'zh-cn',height:200,pages:true,subtitle:true,textareaid:'content',module:'content',cid:'13',
        flashupload:true,alowuploadexts:'',allowbrowser:'1',allowuploadnum:'10',authkey:'1b8426a752d07b7232968152c952ccb8',
        filebrowserUploadUrl : 'http://localhost/phpcms/index.php?m=attachment&c=attachments&a=upload&module=content&cid=13&dosubmit=1',
        toolbar :
        [
        ['Source','-','Templates'],
                    ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print'],
                    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],['ShowBlocks'],['Image','Capture','Flash'],['Maximize'],
                    '/',
                    ['Bold','Italic','Underline','Strike','-'],
                    ['Subscript','Superscript','-'],
                    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
                    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
                    ['Link','Unlink','Anchor'],
                    ['Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
                    '/',
                    ['Styles','Format','Font','FontSize'],
                    ['TextColor','BGColor'],
                    ['attachment'],
        ]
        });
        </script>
        ''' % (web.ctx.req['static_url'], self.name)
        return html

class MyPassword(MyInput, form.Password):
    pass

class MyDropdown(MyInput, form.Dropdown):
    pass

class MyRadio(MyInput, form.Radio):
    pass


