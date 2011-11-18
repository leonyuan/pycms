jQuery.fn.hookMenu = function(settings) {
	settings = jQuery.extend({
		'growUp':false,
		'fixed':false		
	},settings);
	var hook_menu = new Array();
	var hook_menu_x = new Array();
	var hook_menu_xy = new Array();
	this.each(function(i) {
		hook_menu[i] = jQuery(this).next('ul.hook_menu');
		if(hook_menu[i].length) {
			jQuery(this).append('<span class="hook_menu_x">Expand</span>');
			hook_menu_x[i] = jQuery(this).children('span.hook_menu_x').eq(0);
			hook_menu_xy[i] = {
				'width': Math.max((hook_menu_x[i].offset().left + hook_menu_x[i].outerWidth() - jQuery(this).offset().left) - (hook_menu[i].outerWidth() - hook_menu[i].width()),'125'),
				'top': jQuery(this).offset().top + jQuery(this).height(),
				'left': jQuery(this).offset().left
			};
			hook_menu[i].css({
				'position': 'absolute',
				'display': 'none',
				'left': hook_menu_xy[i].left,
				'width': hook_menu_xy[i].width,
				'top': hook_menu_xy[i].top
			});
			jQuery(this).wrapInner('<span class="hook_menu_xc"/>')
			hook_menu_x[i].bind({
				mouseenter: function(e) {
					jQuery(this).parent().toggleClass('hook_highlight');
				},
				mouseout: function(e) {
					jQuery(this).parent().toggleClass('hook_highlight');
				},
				click: function(e) {
					hook_menu[i].fadeIn('slow');
				}
			});
			hook_menu[i].bind({
				mouseout: function(e) {
					var isChild = $(e.currentTarget).has($(e.relatedTarget)).length;
					if(!(isChild)) {
						hook_menu[i].fadeOut('fast');
					}
				},
				click: function(e) {
					hook_menu[i].fadeOut('fast');
				}
			});
		}
	});
	return this;
};