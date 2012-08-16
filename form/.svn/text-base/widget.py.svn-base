import web
from web import form


class MyForm(form.Form):
    def validates(self, source=None, _validate=True,  prefix='', **kw):
        source = source or kw or web.input()
        out = True
        attrname_start = len(prefix)+1
        for i in self.inputs:
            v = form.attrget(source,  i.name[attrname_start:] if prefix else i.name)
            if _validate:
                out = i.validate(v) and out
            else:
                i.set_value(v)
        if _validate:
            out = out and self._validate(source)
            self.valid = out
        return out

    def fill(self, source=None, prefix='', **kw):
        return self.validates(source, _validate=False, prefix=prefix, **kw)



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
                    if self.note.find('${value}') != -1:
                        self.note = self.note.replace('${value}', value)
                    if self.note.find('${description}') != -1:
                        self.note = self.note.replace('${description}', self.description)
                return False
        return True

    def render(self):
        #if web.config.debug:
        #    import pdb
        #    pdb.set_trace()

        html = super(MyInput, self).render()
        if self.note:
            html += '<div class="input-notification error png_bg">%s</div>' % (self.note,)
        return html


class MyButton(MyInput, form.Button):
    def get_type(self):
        return 'button'

class MyTextbox(MyInput, form.Textbox):
    def __init__(self, name, *validators, **attrs):
        attrs['class_'] = 'text-input'
        super(MyTextbox, self).__init__(name, *validators, **attrs)

class MyTextarea(MyInput, form.Textarea):
    def get_type(self):
        return 'textarea'

class MyLongText(MyInput, form.Textarea):
    def __init__(self, name, *validators, **attrs):
        attrs['class_'] = 'richtext-field'
        super(MyLongText, self).__init__(name, *validators, **attrs)

    def render_html(self):
        return super(MyLongText, self).render()

    def render_js(self):
        return '''
        <script type="text/javascript">
            CKEDITOR.replace('%s',
            {
                language:'zh-cn',height:250,textareaid:'content',module:'content',cid:'13',
                alowuploadexts:'',allowbrowser:'1',allowuploadnum:'10',authkey:'1b8426a752d07b7232968152c952ccb8',
                filebrowserUploadUrl: '%s',
                filebrowserBrowseUrl: '%s',
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
        ''' % (self.name, web.config.upload_url, web.config.browse_url)

    def render(self):
        html = self.render_html()
        html += self.render_js()
        return html

    def get_type(self):
        return 'richtext'

class MyPassword(MyInput, form.Password):
    pass

class MyDropdown(MyInput, form.Dropdown):
    def get_type(self):
        return 'dropdown'


class MyRadio(MyInput, form.Radio):
    def get_type(self):
        return 'radio'

class MyCheckbox(MyInput, form.Checkbox):
    def get_type(self):
        return 'checkbox'

class MyFile(MyInput, form.File):
    def render(self):
        html = super(MyFile, self).render()
        if self.value is not None:
            html = '<a href="%s">%s</a></br>' % (self.value, self.value) + html
        return html

    def get_type(self):
        return 'file'

class MyCheckboxGroup(MyInput):
    def __init__(self, name, args, *validators, **attrs):
        self.args = args
        super(MyCheckboxGroup, self).__init__(name, *validators, **attrs)

    def render(self):
        x = '<span>'
        for arg in self.args:
            if isinstance(arg, (tuple, list)):
                value, desc= arg
            else:
                value, desc = arg, arg
            attrs = self.attrs.copy()
            attrs['id'] = self.name + '_' + web.utils.safeunicode(value or "").replace(' ', '_')
            attrs['name'] = self.name
            attrs['type'] = 'checkbox'
            attrs['value'] = value
            if self.value and value in self.value:
                attrs['checked'] = 'checked'
            x += '<input %s/> %s' % (attrs, web.net.websafe(desc))
        x += '</span>'
        return x

    def get_type(self):
        return 'checkboxgroup'

class Selector(MyInput):
    def render(self):
        pass

    def get_type(self):
        return 'selector'
