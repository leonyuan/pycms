import web


article_form = web.form.Form(
    web.form.Textbox('title', web.form.notnull,
        size=30,
        description="Post title:"),
    web.form.Textarea('content', web.form.notnull,
        rows=20, cols=60,
        description="Post content:"),
    web.form.Button('Post entry'),
)


