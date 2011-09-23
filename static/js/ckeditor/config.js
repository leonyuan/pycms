/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	config.uiColor = '#f7f5f4';
	config.width = '';
	config.removePlugins = 'elementspath,scayt';
	config.disableNativeSpellChecker = false;
	config.resize_dir = 'vertical';
	config.keystrokes =[[ CKEDITOR.CTRL + 13 /*Enter*/, 'maximize' ]];	
	config.extraPlugins = 'capture';
};
//CKEDITOR.plugins.load('pgrfilemanager');
function insert_page(editorid)
{
	var editor = CKEDITOR.instances[editorid];
	editor.insertHtml('[page]');
	if($('#paginationtype').val()) {
		$('#paginationtype').val(2);
		$('#paginationtype').css("color","red");
	}
}

function insert_page_title(editorid,insertdata)
{
	if(insertdata)
	{
		var editor = CKEDITOR.instances[editorid];
		var data = editor.getData();
		var page_title_value = $("#page_title_value").val();
		if(page_title_value=='')
		{
			$("#msg_page_title_value").html("<font color='red'>请输入子标题</font>");
			return false;
		}
		page_title_value = '[page]'+page_title_value+'[/page]';
		editor.insertHtml(page_title_value);
		$("#page_title_value").val('');
		$("#msg_page_title_value").html('');
		if($('#paginationtype').val()) {
			$('#paginationtype').val(2);
			$('#paginationtype').css("color","red");
		}
	}
	else
	{
		$("#page_title_div").slideDown("fast");
	}
}
var objid = MM_objid = key = 0;
function file_list(fn,url,obj) {
	$('#MM_file_list_editor1').append('<div id="MM_file_list_'+fn+'">'+url+' <a href=\'#\' onMouseOver=\'javascript:FilePreview("'+url+'", 1);\' onMouseout=\'javascript:FilePreview("", 0);\'>查看</a> | <a href="javascript:insertHTMLToEditor(\'<img src='+url+'>\',\''+fn+'\')">插入</A> | <a href="javascript:del_file(\''+fn+'\',\''+url+'\','+fn+')">删除</a><br>');
}

