/*
Copyright (c) 2005-2011, PHPCMS V9- Rocing Chan. All rights reserved.
For licensing, see http://www.phpcms.cn.com/license
*/
(function()
{
	var loadcapture =
	{
		exec : function( editor )
		{
			var pluginNameExt = 'capture';
			ext_editor = editor.name;
				if(CKEDITOR.env.ie) {
					try{
						 //var t = new ActiveXObject("WEBCAPTURECTRL.WebCaptureCtrlCtrl.1");
						 return document.getElementById("PC_Capture").ShowCaptureWindow();
					} catch(e){
						CKEDITOR.dialog.add(pluginNameExt,  function( api )
						{
							var dialogDefinition =
							{
								title : editor.lang.capture.notice,
								minWidth : 350,
								minHeight : 80,
								contents : [
									{
										id : 'tab1',
										label : 'Label',
										title : 'Title',
										padding : 0,
										elements :
										[
											{
												type : 'html',
												html : editor.lang.capture.notice_tips
											}
										]
									}
								],
								buttons : [ CKEDITOR.dialog.cancelButton ]
							};

							return dialogDefinition;
						});
						editor.addCommand(pluginNameExt, new CKEDITOR.dialogCommand(pluginNameExt));						
						editor.execCommand(pluginNameExt);				
					}
				} else {
					alert(editor.lang.capture.unsport_tips);
					return false;
				}
		}
		
	};

	var pluginName = 'capture';
	CKEDITOR.plugins.add('capture',
	{
		lang: ['zh-cn'],
		init: function(editor)
		{
			if ( CKEDITOR.env.ie ) {
				editor.addCommand(pluginName, loadcapture);
				editor.ui.addButton('Capture',
					{
						label: editor.lang.capture.title,
						command: pluginName,
						icon: CKEDITOR.plugins.getPath('capture') + 'capture.png'
					});
			} 
		}
	});
})();

function pc_screen(param){
	var oEditor = CKEDITOR.instances[ext_editor];
	var data = oEditor.getData();
	var imgtag = "<img src="+param+"><BR>";
	oEditor.insertHtml(imgtag);
}