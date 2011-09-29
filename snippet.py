
                % if _verr and _verr.has_key('username'):
                <div id="catnameTip" class="onShow">${_verr['username']}</div>
                % endif

        '/field/index', field.index,
        '/field/add', field.add,
        '/field/edit/(\d+)', field.edit,
        '/field/delete/(\d+)', field.delete,
