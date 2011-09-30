
                % if _verr and _verr.has_key('username'):
                <div id="catnameTip" class="onShow">${_verr['username']}</div>
                % endif

        '/relation/index', relation.index,
        '/relation/add', relation.add,
        '/relation/edit/(\d+)', relation.edit,
        '/relation/delete/(\d+)', relation.delete,


