
      %#<td><input type="hidden" name="cid" value="${cid}">${catname}</td>%

<div class="selector">
              <div class="selector-available">
                <h2>可用 用户</h2>

                <p class="selector-filter">
                <label for="id_groups_input"style="width:16px;padding:2px;display:block;float:left;">
                    <img src="${static_url}/images/admin_img/selector-search.gif" alt="过滤">
                  </label><input type="text" id="id_groups_input">
                </p>
                <select id="id_groups_from" name="groups_old" class="filtered" multiple="multiple">
                    % for user in users:
                    <option value="${user.id}">${user.username}</option>
                    % endfor
                </select><a href="javascript: (function(){ SelectBox.move_all('id_groups_from', 'id_groups_to'); })()"
                 class="selector-chooseall">全选</a>
              </div>

              <ul class="selector-chooser">
                <li><a href="javascript: (function(){ SelectBox.move('id_groups_from','id_groups_to');})()" class="selector-add">增加</a></li>
                <li><a href="javascript: (function(){ SelectBox.move('id_groups_to','id_groups_from');})()" class="selector-remove">删除</a></li>
              </ul>

              <div class="selector-chosen">
                <h2>选中的 用户</h2>

                <p class="selector-filter">选择并点击 <img src="${static_url}/images/admin_img/selector-add.gif" alt="Add"></p>
                <select id="id_groups_to" multiple="multiple" size="0" name="groups" class="filtered">
                </select>
                  <a href="javascript: (function() { SelectBox.move_all('id_groups_to', 'id_groups_from');})()"
                 class="selector-clearall">清除全部</a>
              </div>
            </div>

