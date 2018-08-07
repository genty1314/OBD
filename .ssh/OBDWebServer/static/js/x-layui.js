/*弹出层*/
/*
	参数解释：
	title	标题
	url		请求的url
	id		需要操作的数据id
	w		弹出层宽度（缺省调默认值）
	h		弹出层高度（缺省调默认值）
*/
function x_admin_show(title,url,w,h,act){
	if (title == null || title == '') {
		title=false;
	};
	if (url == null || url == '') {
		url="404.html";
	};
	if (w == null || w == '') {
		w=800;
	};
	if (h == null || h == '') {
		h=($(window).height() - 50);
	};
	perContent = layer.open({
		type: 2,
		offset: 'auto',
		area: [w*1.5 + 'px', h*1.5 +'px'],
		fix: false, //不固定
		maxmin: true,
		shadeClose: true,
		shade:0.4,
		title: title,
		content: url,
		end: act
	});
	// layer.full(perContent);
}

/*关闭弹出框口*/
function x_admin_close(){
	var index = parent.layer.getFrameIndex(window.name);
	parent.layer.close(index);
}