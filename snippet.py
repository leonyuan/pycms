        <%block name="content">
        ${next.body()}
        </%block>


        <%block name="nav-global"></%block>


                % if _verr and _verr.has_key('username'):
                <div id="catnameTip" class="onShow">${_verr['username']}</div>
                % endif

        '/relation/index', relation.index,
        '/relation/add', relation.add,
        '/relation/edit/(\d+)', relation.edit,
        '/relation/delete/(\d+)', relation.delete,

   <tr>
        <th>${form.type.description}</th>
        <td>
          <span id="normal_add">
            <select onchange="" id="type" name="type">
                <option value="">=请选择类型=</option>
                <option value="string" ${'selected="selected"' if str(form.d.type) == 'string' else ''}>字符串</option>
                <option value="integer" ${'selected="selected"' if str(form.d.type) == 'integer' else ''}>整数</option>
            </select>
            % if form.type.note:
            <div id="catnameTip" class="onShow">${form.type.note}</div>
            % endif
          </span>
		</td>
    </tr>

