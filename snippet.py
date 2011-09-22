    <ul>
        % for e in _verr:
            <li>${e}</li>
        % endfor
    </ul>


                <td>${'├'+cate.level*'─' if cate.level > 0 else ''}${cate.name}</td>
                <td>${'&nbsp;&nbsp;'+(cate.level-1)*('&nbsp;' if cate.lasted else u'│')+'&nbsp;&nbsp;'+(u'└' if cate.lasted else u'├')+u'─' if cate.level else ''}${cate.name}</td>

        if level > 0:
            if level == 1:
                prefix = '&nbsp;&nbsp;'

            else:
                #if i == cnt-1:
                #    prefix = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                #else:
                prefix = u'│&nbsp;&nbsp;'

            #prefix += (level-1)*'&nbsp;&nbsp;'
            #prefix +=  '&nbsp;&nbsp;'

            base_prefix = super_prefix + prefix

            if i == cnt-1:
                prefix += u'└'
            else:
                prefix += u'├'

            prefix += u'─'
            prefix = super_prefix + prefix

<style type="text/css">
.ui_dialog_wrap {
    visibility: hidden
}

.ui_title_icon,.ui_content,.ui_dialog_icon,.ui_btns span {
    display: inline-block;
    *zoom: 1;
    *display: inline
}

.ui_dialog {
    text-align: left;
    position: absolute;
    top: 0
}

.ui_dialog table {
    border: 0;
    margin: 0;
    border-collapse: collapse
}

.ui_dialog td {
    padding: 0
}

.ui_title_icon,.ui_dialog_icon {
    vertical-align: middle;
    _font-size: 0
}

.ui_title_text {
    overflow: hidden;
    cursor: default
}

.ui_close {
    display: block;
    position: absolute;
    outline: none
}

.ui_content_wrap {
    text-align: center
}

.ui_content {
    margin: 10px;
    text-align: left
}

.ui_iframe .ui_content {
    margin: 0;
    *padding: 0;
    display: block;
    height: 100%;
    position: relative
}

.ui_iframe .ui_content iframe {
    border: none;
    overflow: auto
}

.ui_content_mask {
    visibility: hidden;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: #FFF;
    filter: alpha(opacity = 0);
    opacity: 0
}

.ui_bottom {
    position: relative
}

.ui_resize {
    position: absolute;
    right: 0;
    bottom: 0;
    z-index: 1;
    cursor: nw-resize;
    _font-size: 0
}

.ui_btns {
    text-align: right;
    white-space: nowrap
}

.ui_btns span {
    margin: 5px 10px
}

.ui_btns button {
    cursor: pointer
}

* .ui_ie6_select_mask {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
    filter: alpha(opacity = 0)
}

.ui_loading .ui_content_wrap {
    position: relative;
    min-width: 9em;
    min-height: 3.438em
}

.ui_loading .ui_btns {
    display: none
}

.ui_loading_tip {
    visibility: hidden;
    width: 5em;
    height: 1.2em;
    text-align: center;
    line-height: 1.2em;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -0.6em 0 0 -2.5em
}

.ui_loading .ui_loading_tip,.ui_loading .ui_content_mask {
    visibility: visible
}

.ui_loading .ui_content_mask {
    filter: alpha(opacity = 100);
    opacity: 1
}

.ui_move .ui_title_text {
    cursor: move
}

.ui_page_move .ui_content_mask {
    visibility: visible
}

.ui_move_temp {
    visibility: hidden;
    position: absolute;
    cursor: move
}

.ui_move_temp div {
    height: 100%
}

html > body .ui_fixed .ui_move_temp {
    position: fixed
}

html > body .ui_fixed .ui_dialog {
    position: fixed
}

* .ui_ie6_fixed {
    background: url(*) fixed
}

* .ui_ie6_fixed body {
    height: 100%
}

* html .ui_fixed {
    width: 100%;
    height: 100%;
    position: absolute;
    left: expression(documentElement.scrollLeft +
        documentElement.clientWidth-this.offsetWidth);
    top: expression(documentElement.scrollTop +
        documentElement.clientHeight-this.offsetHeight)
}

* .ui_page_lock select,* .ui_page_lock .ui_ie6_select_mask {
    visibility: hidden
}

* .ui_page_lock .ui_content select {
    visibility: visible;
}

.ui_overlay {
    visibility: hidden;
    _display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    filter: alpha(opacity = 0);
    opacity: 0;
    _overflow: hidden
}

.ui_lock .ui_overlay {
    visibility: visible;
    _display: block
}

.ui_overlay div {
    height: 100%
}

* html body {
    margin: 0
}
</style>



      <form method="post" action="" id="myform" name="myform">
        <div class="pad_10">
        <div class="table-list">
          <table width="100%">
            <thead>
              <tr>
                <th>排序</th>
                <th>ID</th>
                <th>标题</th>
                <th>点击量</th>
                <th>发布人</th>
                <th>更新时间</th>
                <th>管理操作</th>
              </tr>
          </thead>
        <tbody>
            % for article in articles:
            <tr>
                <td>${article.id}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
            % endfor
		</tbody>

          </table>

          <div class="btn">
              <label for="check_box">全选/取消</label>
              <input type="hidden" name="pc_hash" value="UaPUc2" />
              <input type="button" onclick="myform.action='?m=content&c=content';myform.submit();" value="排序" class="button" />
              <input type="button" onclick="myform.action='?m=content';return confirm_delete()" value="删除" class="button" />
              <input type="button" onclick="push();" value="推送" class="button" />
              <input type="button" onclick="myform.action='?m=content';myform.submit();" value="批量移动" class="button" />
          </div>

        </div>
        </div>
      </form>

