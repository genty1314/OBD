function developing(id){
    console.log(id);
    alert("开发中...");
}
function cahngetab(tabatc,tabdis){ //使用amazeui的tab元素 tabatc为要激活的tabid。tabdis为要取消激活的tabid
    if (tabatc=="tab2") {
        if ($("table input[name='code']").length>0) {
            $("#obd_code").html($("table input[name='code']").val());
        }
        if ($("table input[name='name']").length>0) {
            $("#obd_name").html($("table input[name='name']").val());
        }
        if ($("table input[name='address']").length>0) {
            $("#obd_address").html($("table input[name='address']").val());
        }
    }
    $("#"+tabatc).addClass("am-active");
    $("#"+tabdis).removeClass("am-active");
};
function ConfirmPic(picid,is_correct){
    //useconfirmpic
    code = $("table input[name='code']").val();
    name = $("table input[name='name']").val();
    address = $("table input[name='address']").val();
    if(code != ""){
    console.log("is_correct=="+is_correct);
    $.ajax({
          type:"put",
          url:"/useconfirmpic",
          data:{
            "picid":picid,
            "is_correct":is_correct,
            "code":code,
            "name":name,
            "address":address
          },
          datatype: "json",
          cache:false,
          success:function(data){
            if (data == "success") {
                alert("修改成功！")
                $("#pic_confirmed").modal("close");
            }else{
                alert("修改失败！")
            }
          },
          error:function(XMLHttpRequest, textStatus, errorThrown){
            alert(XMLHttpRequest+"\n"+textStatus+"\n"+errorThrown);
          },
        });
    }else{
        console.log("is_correct==0");
        $(".am-modal-confirm").remove();
        var confirminfo = $('<div class="am-modal am-modal-confirm" tabindex="-1" id="cancelconfirm">'+
                              '<div class="am-modal-dialog">'+
                                '<div class="am-modal-hd">缺少OBD编号信息</div>'+
                                '<div class="am-modal-bd">'+
                                  '缺少OBD编号信息，确定直接退出不保存吗？'+
                                '</div>'+
                                '<div class="am-modal-footer">'+
                                  '<span class="am-modal-btn" data-am-modal-confirm>确定</span>'+
                                  '<span class="am-modal-btn" data-am-modal-cancel>取消</span>'+
                                '</div>'+
                              '</div>'+
                            '</div>'
            ).appendTo("body");
        $('#cancelconfirm').modal({
        relatedTarget: this,
        onConfirm: function(options) {
          $.ajax({
          type:"put",
          url:"/useconfirmpic",
          data:{
            "picid":picid,
            "is_correct":0,
            "code":code,
            "name":name,
            "address":address
          },
          datatype: "json",
          cache:false,
          success:function(data){
            if (data == "success") {
                alert("退出成功！")
                $("#pic_confirmed").modal("close");
            }else{
                alert("修改失败！")
            }
          },
          error:function(XMLHttpRequest, textStatus, errorThrown){
            alert(XMLHttpRequest+"\n"+textStatus+"\n"+errorThrown);
          },
        });
          $("#pic_confirmed").modal("close");
        },
        // closeOnConfirm: false,
        onCancel: function() {
          cahngetab("tab1","tab2");
        }
      });
    }
    
};

function ShowText(text){
if (text!="") {
    alert(text);
}
};

function showImg(baseUrl) {
$("#ShowImg").remove();
var infoImg =$( '<div id="ShowImg" class="am-popup">' +
                      '<div class="am-popup-inner">'+
                          '<div class="am-popup-hd">'+
                            '<h4 class="am-popup-title">放大图</h4>'+
                            '<span data-am-modal-close class="am-close">&times;</span>'+
                          '</div>'+
                          '<div class="am-popup-bd">'+
                 '<img class="am-img-responsive" src="' + baseUrl + '" />' +
                          '</div>'+
                      '</div>'+
        '</div>').appendTo("body");
  infoImg.modal("open");
};
(function( $ ){
    // 当domReady的时候开始初始化
    var GPS="";
    if (navigator.geolocation){ 
      navigator.geolocation.getCurrentPosition(function(position){ 
      var lat = position.coords.latitude; //纬度 
      var lag = position.coords.longitude; //经度 
      GPS = lag+":"+lat;
      } ,function (error){ 
        switch(error.code) { 
        case error.PERMISSION_DENIED: 
        alert("定位失败,用户拒绝请求地理定位"); 
        break; 
        case error.POSITION_UNAVAILABLE: 
        alert("定位失败,位置信息是不可用"); 
        break; 
        case error.TIMEOUT: 
        alert("定位失败,请求获取用户位置超时"); 
        break; 
        case error.UNKNOWN_ERROR: 
        alert("定位失败,定位系统失效"); 
        break; 
        } 
      });
      
    }else{ 
      alert("浏览器不支持地理定位"); 
    }

    $(function() {

        //图片信息选择
        $('#picinfo').mobiscroll().treelist({
            lang: 'zh',
            theme: 'ios',
            display: 'bottom',
            width: [156, 136, 146],
            showScrollArrows:false,
            headerText:'图片端口信息',
            showLabel:['端口朝向', '0口位置', '端口排序'],
            inputClass:'picinfo',
            placeholder: '点击选择图片端口信息',
            labels: ['端口朝向', '0口位置', '端口排序'],
        });


        var $wrap = $('#uploader'),
            $picinfo_dummy = $("#picinfo_dummy"),
            // $port_direction = $("#port_direction"),
            // $zero_port_pos = $("#zero_port_pos"),
            // $port_sort = $("#port_sort"),
            $addAddress = $("#addAddress"),
            $OBDCode = $("#OBDCode"),

            $dndArea = $("#dndArea"),
            
            // 图片容器
            $queue = $( '<ul class="filelist"></ul>' )
                .appendTo( $wrap.find( '#dndArea' ) ),
            // 状态栏，包括进度和控制按钮
            $statusBar = $wrap.find( '.statusBar' ),

            // 文件总体选择信息。 
            $info = $statusBar.find( '.info' ),

            // 上传按钮
            $upload = $( '#upload' ),

            // 没选择文件之前的内容。
            $placeHolder = $wrap.find( '.placeholder' ),

            $progress = $statusBar.find( '.progress' ).hide(),
            
            //控制缩放比例 
            imgScale = 1,

            // 添加的文件数量
            fileCount = 0,

            // 添加的文件总大小
            fileSize = 0,

            // 优化retina, 在retina下这个值是2
            ratio = window.devicePixelRatio || 1,

            // 缩略图大小
            thumbnailWidth = 1,
            thumbnailHeight = 1,

            // 可能有pedding, ready, uploading, confirm, done.
            state = 'pedding',

            // 所有文件的进度信息，key为file id
            percentages = {},
            
            // 判断浏览器是否支持图片的base64
            isSupportBase64 = ( function() {
                var data = new Image();
                var support = true;
                data.onload = data.onerror = function() {
                    if( this.width != 1 || this.height != 1 ) {
                        support = false;
                    }
                }
                data.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
                return support;
            } )(),

            // 检测是否已经安装flash，检测flash的版本
            flashVersion = ( function() {
                var version;

                try {
                    version = navigator.plugins[ 'Shockwave Flash' ];
                    version = version.description;
                } catch ( ex ) {
                    try {
                        version = new ActiveXObject('ShockwaveFlash.ShockwaveFlash')
                                .GetVariable('$version');
                    } catch ( ex2 ) {
                        version = '0.0';
                    }
                }
                version = version.match( /\d+/g );
                return parseFloat( version[ 0 ] + '.' + version[ 1 ], 10 );
            } )(),

            supportTransition = (function(){
                var s = document.createElement('p').style,
                    r = 'transition' in s ||
                            'WebkitTransition' in s ||
                            'MozTransition' in s ||
                            'msTransition' in s ||
                            'OTransition' in s;
                s = null;
                return r;
            })(),

            // WebUploader实例
            uploader;

        if ( !WebUploader.Uploader.support('flash') && WebUploader.browser.ie ) {

            // flash 安装了但是版本过低。
            if (flashVersion) {
                (function(container) {
                    window['expressinstallcallback'] = function( state ) {
                        switch(state) {
                            case 'Download.Cancelled':
                                alert('您取消了更新！')
                                break;

                            case 'Download.Failed':
                                alert('安装失败')
                                break;

                            default:
                                alert('安装已成功，请刷新！');
                                break;
                        }
                        delete window['expressinstallcallback'];
                    };

                    var swf = './expressInstall.swf';
                    // insert flash object
                    var html = '<object type="application/' +
                            'x-shockwave-flash" data="' +  swf + '" ';

                    if (WebUploader.browser.ie) {
                        html += 'classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" ';
                    }

                    html += 'width="100%" height="100%" style="outline:0">'  +
                        '<param name="movie" value="' + swf + '" />' +
                        '<param name="wmode" value="transparent" />' +
                        '<param name="allowscriptaccess" value="always" />' +
                    '</object>';

                    container.html(html);

                })($wrap);

            // 压根就没有安转。
            } else {
                $wrap.html('<a href="http://www.adobe.com/go/getflashplayer" target="_blank" border="0"><img alt="get flash player" src="http://www.adobe.com/macromedia/style_guide/images/160x41_Get_Flash_Player.jpg" /></a>');
            }

            return;
        } else if (!WebUploader.Uploader.support()) {
            alert( 'Web Uploader 不支持您的浏览器！');
            return;
        }

        // 实例化
        uploader = WebUploader.create({
            pick: {
                id: '#filePicker',
                label: '添加照片'
            },// 选择文件的按钮
            // formData: {
            //     "folder": "folder"
            // },
            // dnd: '#dndArea',
            paste: '#uploader',
            swf: '../../dist/Uploader.swf',// swf文件路径
            chunked: false,
            chunkSize: 512 * 1024,
            server: '/useconfirmpic',// 文件接收服务端
            // runtimeOrder: 'flash',
            // 只允许选择图片文件。
            accept: {
                title: 'Images',
                extensions: 'gif,jpg,jpeg,bmp,png',
                mimeTypes: 'image/*'
            },
            thumb:{
                // 图片质量，只有type为`image/jpeg`的时候才有效。
                quality: 50,

                // 是否允许放大，如果想要生成小图的时候不失真，此选项应该设置为false.
                allowMagnify: true,

                // 是否允许裁剪。
                crop: false,

                // 为空的话则保留原有图片格式。
                // 否则强制转换成指定的类型。
                type: ''
            },
            // compress:false,//不压缩
            compress: {
                width:1600,
                height:1600,
                // 图片质量，只有type为`image/jpeg`的时候才有效。
                quality: 90,

                // 是否允许放大，如果想要生成小图的时候不失真，此选项应该设置为false.
                allowMagnify: false,

                // 是否允许裁剪。
                crop: false,

                // 是否保留头部meta信息。
                preserveHeaders: true,

                // 如果发现压缩后文件大小比原来还大，则使用原来图片
                // 此属性可能会影响图片自动纠正功能
                noCompressIfLarger: false,

                // 单位字节，如果图片大小小于此值，不会采用压缩。
                compressSize: 2*1024*1024
            },
            resize: false,//尺寸不改变
            disableGlobalDnd: true,
            fileNumLimit: 1,//限制上传个数
            fileSizeLimit: 50*1024 * 1024,    // 5 M  
            fileSingleSizeLimit: 50*1024 * 1024    // 5 M 限制单个上传图片的大小
        });

        uploader.on();

        // 拖拽时不接受 js, txt 文件。
        uploader.on( 'dndAccept', function( items ) {
            var denied = false,
                len = items.length,
                i = 0,
                // 修改js类型
                unAllowed = 'application/javascript ';
//              unAllowed = 'text/plain;application/javascript ';

            for ( ; i < len; i++ ) {
                // 如果在列表里面
                if ( ~unAllowed.indexOf( items[ i ].type ) ) {
                    denied = true;
                    break;
                }
            }

            return !denied;
        });

        uploader.on('dialogOpen', function() {
            console.log('here');
        });

        // uploader.on('filesQueued', function() {
        //     uploader.sort(function( a, b ) {
        //         if ( a.name < b.name )
        //           return -1;
        //         if ( a.name > b.name )
        //           return 1;
        //         return 0;
        //     });
        // });

        // 添加“添加文件”的按钮，
        // uploader.addButton({
        //     id: '#filePicker2',
        //     label: '继续添加'
        // });

        uploader.on('ready', function() {
            window.uploader = uploader;
        });

        // 当有文件添加进来时执行，负责view的创建
        function addFile( file ) {
            var $li = $( '<li id="' + file.id + '">' +
                    '<p class="title">' + file.name + '</p>' +
                    '<p class="imgWrap"></p>'+
                    '<p class="progress"><span></span></p>' +
                    '</li>' ),

                $btns = $('<div class="file-panel">' +
                    '<span class="cancel">删除</span>'
                    ).appendTo( $li ),
                $prgress = $li.find('p.progress span'),
                $wrap = $li.find( 'p.imgWrap' ),
                $info = $('<p class="error"></p>'),
                baseUrl = '',

                showError = function( code ) {
                    $(".am-modal-loading").modal("close");
                    switch( code ) {
                        case 'exceed_size':
                            text = '文件大小超出';
                            break;

                        case 'interrupt':
                            text = '上传暂停';
                            break;

                        default:
                            //text = '上传失败，请重试';
                            text = '检测失败，请拍摄正确的照片后重试'
                            break;
                    }
                    $info.text( text ).appendTo( $li );
                };

            if ( file.getStatus() === 'invalid' ) {
                showError( file.statusText );
            } else {
                // @todo lazyload
                $wrap.text( '预览中' );
                uploader.makeThumb( file, function( error, src ) {
                    var img;
                    baseUrl = src;
                    if ( error ) {
                        $wrap.text( '不能预览' );
                        return;
                    }
                    if( isSupportBase64 ) {
						if(file._info.height>file._info.width){
							img = $('<div style="background:url('+src+') center no-repeat;width: '+$dndArea.width()+'px;height: '+$dndArea.height()+'px;background-size: 300px 300px;"></div>');
						}else{
							img = $('<div style="background:url('+src+') center no-repeat;width: '+$dndArea.width()+'px;height: '+$dndArea.height()+'px;background-size: 300px 300px;"></div>');
						}
                        $wrap.empty().append( img );
                    } else {
                        $.ajax('/', {
                            method: 'POST',
                            data: src,
                            dataType:'json'
                        }).done(function( response ) {
                            if (response.result) {
                                img = $('<div style="background:url('+response.result+') center no-repeat;width: '+$dndArea.width()+'px;height: '+$dndArea.height()+'px;background-size: 300px 300px;"></div>');
                                $wrap.empty().append( img );
                            } else {
                                $wrap.text("预览出错");
                            }
                        });
                    }
                }, thumbnailWidth, thumbnailHeight );

                percentages[ file.id ] = [ file.size, 0 ];
                file.rotation = 0;
            }

            file.on('statuschange', function( cur, prev ) {
                if ( prev === 'progress' ) {
                    $prgress.hide().width(0);
                } else if ( prev === 'queued' ) {
                    $li.off( 'mouseenter mouseleave' );
                    // $btns.remove();
                }

                // 成功
                if ( cur === 'error' || cur === 'invalid' ) {
                    console.log( file.statusText );
                    showError( file.statusText );
                    percentages[ file.id ][ 1 ] = 1;
                } else if ( cur === 'interrupt' ) {
                    showError( 'interrupt' );
                } else if ( cur === 'queued' ) {
                    $info.remove();
                    $prgress.css('display', 'block');
                    percentages[ file.id ][ 1 ] = 0;
                } else if ( cur === 'progress' ) {
                    $info.remove();
                    $prgress.css('display', 'block');
                } else if ( cur === 'complete' ) {
                    $prgress.hide().width(0);
                    $li.append( '<span class="success"></span>' );
                }

                $li.removeClass( 'state-' + prev ).addClass( 'state-' + cur );
            });

            // $li.on( 'mouseenter', function() {
            //     $btns.stop().animate({height: 30});
            // });

            // $li.on( 'mouseleave', function() {
            //     $btns.stop().animate({height: 0});
            // });
            
            $wrap.on( 'mouseup', function() {
                showImg(baseUrl);
            });

            //鼠标滚动事件
            var scrollFunc=function(e){
				var direct = 0;
				e = e || window.event;
				
				if(e.wheelDelta) { //IE/Opera/Chrome
					direction(e.wheelDelta);
				} else if(e.detail) { //Firefox
					direction(-e.detail);
				}
			}
            
            //滚动方向
            function direction(roll){
            	if(roll>0){
					//向上滚动
					imgScale+=0.2;
					var imgTransform = "translate(-50%,-50%) scale(" + imgScale + "," + imgScale + ")";
					$("#img_info img").css({
						"transform":imgTransform,
						"-moz-transform":imgTransform,
						"opacity":"1"
					});
				}else{
					//向下滚动
					if(imgScale>0.5){
						imgScale-=0.2;
						var imgTransform = "translate(-50%,-50%) scale(" + imgScale + "," + imgScale + ")";
						$("#img_info img").css({
							"transform":imgTransform,
							"-moz-transform":imgTransform,
							"opacity":"1"
						});
					}else{
						//alert("已经到最小了");
					}
				}
            }

            $btns.on( 'click', 'span', function() {
                var index = $(this).index(),
                    deg;

                switch ( index ) {
                    case 0:
                        uploader.removeFile( file );
                        return;

                    case 1:
                        file.rotation += 90;
                        break;

                    case 2:
                        file.rotation -= 90;
                        break;
                }

                if ( supportTransition ) {
                    deg = 'rotate(' + file.rotation + 'deg)';
                    $wrap.css({
                        '-webkit-transform': deg,
                        '-mos-transform': deg,
                        '-o-transform': deg,
                        'transform': deg
                    });
                } else {
                    $wrap.css( 'filter', 'progid:DXImageTransform.Microsoft.BasicImage(rotation='+ (~~((file.rotation/90)%4 + 4)%4) +')');
                    // use jquery animate to rotation
                    // $({
                    //     rotation: rotation
                    // }).animate({
                    //     rotation: file.rotation
                    // }, {
                    //     easing: 'linear',
                    //     step: function( now ) {
                    //         now = now * Math.PI / 180;

                    //         var cos = Math.cos( now ),
                    //             sin = Math.sin( now );

                    //         $wrap.css( 'filter', "progid:DXImageTransform.Microsoft.Matrix(M11=" + cos + ",M12=" + (-sin) + ",M21=" + sin + ",M22=" + cos + ",SizingMethod='auto expand')");
                    //     }
                    // });
                }

            });

            $li.appendTo( $queue );
        }

        // 负责view的销毁
        function removeFile( file ) {
            var $li = $('#'+file.id);

            delete percentages[ file.id ];
            updateTotalProgress();
            $li.off().find('.file-panel').off().end().remove();
        }

        function updateTotalProgress() {
            var loaded = 0,
                total = 0,
                spans = $progress.children(),
                percent;

            $.each( percentages, function( k, v ) {
                total += v[ 0 ];
                loaded += v[ 0 ] * v[ 1 ];
            } );

            percent = total ? loaded / total : 0;


            spans.eq( 0 ).text( Math.round( percent * 100 ) + '%' );
            spans.eq( 1 ).css( 'width', Math.round( percent * 100 ) + '%' );
            updateStatus();
        }

        function updateStatus() {
            var text = '', stats;

            if ( state === 'ready' ) {
                text = '选中' + fileCount + '张图片，共' +
                        WebUploader.formatSize( fileSize ) + '。';
            } else if ( state === 'confirm' ) {
                stats = uploader.getStats();
                if ( stats.uploadFailNum ) {
                    text = '已成功上传' + stats.successNum+ '张照片至XX相册，'+
                        stats.uploadFailNum + '张照片上传失败，<a class="retry" href="#">重新上传</a>失败图片或<a class="ignore" href="#">忽略</a>'
                }

            } else {
                stats = uploader.getStats();
                text = '共' + fileCount + '张（' +
                        WebUploader.formatSize( fileSize )  +
                        '），已上传' + stats.successNum + '张';

                if ( stats.uploadFailNum ) {
                    text += '，失败' + stats.uploadFailNum + '张';
                }
            }

            $info.html( text );
        }

        function setState( val ) {
            var file, stats;

            if ( val === state ) {
                return;
            }

            $upload.removeClass( 'state-' + state );
            $upload.addClass( 'state-' + val );
            state = val;

            switch ( state ) {
            	//未上传状态
                case 'pedding':
//                  $placeHolder.removeClass( 'element-invisible' );
                    $queue.hide();//隐藏存放图片容器
                    $statusBar.addClass( 'element-invisible' );
                    $(".filePrompt").show();
                    uploader.refresh();
                    break;

                case 'ready':
//                  $placeHolder.addClass( 'element-invisible' );
                    $( '#filePicker2' ).removeClass( 'element-invisible');
                    $queue.show();//显示存放图片容器
                    $statusBar.show();
                    $statusBar.removeClass('element-invisible');
                    $(".filePrompt").hide();
                    uploader.refresh();
                    break;

                case 'uploading':
                    $( '#filePicker2' ).addClass( 'element-invisible' );
                    $progress.show();
                    $upload.text( '暂停上传' );
                    break;

                case 'paused':
                    $progress.show();
                    $upload.text( '继续上传' );
                    break;

                case 'confirm':
                    $progress.hide();
                    $( '#filePicker2' ).removeClass( 'element-invisible' );
                    $upload.text( '验证' );

                    stats = uploader.getStats();
                    if ( stats.successNum && !stats.uploadFailNum ) {
                        setState( 'finish' );
                        return;
                    }
                    break;
                case 'finish':
                    stats = uploader.getStats();
                    if ( stats.successNum ) {
                        //图片上传成功后的验证
                        
                    } else {
                        // 没有成功的图片，重设
                        state = 'done';
                        location.reload();
                    }
                    break;
            }

            updateStatus();
        }

        uploader.onStartUpload = function(){
            //上传前的loding
            $(".am-modal-loading").modal("open");
        };

        uploader.onUploadProgress = function( file, percentage ) {

            var $li = $('#'+file.id),
                $percent = $li.find('.progress span');

            $percent.css( 'width', percentage * 100 + '%' );
            percentages[ file.id ][ 1 ] = percentage;
            updateTotalProgress();
        };

        uploader.onFileQueued = function( file ) {
            fileCount++;
            fileSize += file.size;

//          if ( fileCount === 2 ) {
//              $placeHolder.addClass( 'element-invisible' );
//              $statusBar.show();
//          }
            addFile( file );
            setState( 'ready' );
            updateTotalProgress();
        };

        uploader.onFileDequeued = function( file ) {
            fileCount--;
            fileSize -= file.size;

            if ( !fileCount ) {
                setState( 'pedding' );
            }

            removeFile( file );
            updateTotalProgress();

        };

        uploader.on( 'all', function( type ) {
            var stats;
            switch( type ) {
                case 'uploadFinished':
                    setState( 'confirm' );
                    break;

                case 'startUpload':
                    setState( 'uploading' );
                    break;

                case 'stopUpload':
                    setState( 'paused' );
                    break;

            }
        });

        //每张图片上传成功后返回
        uploader.on( 'uploadSuccess', function( file, response ) {
        	$(".am-modal-loading").modal("close");
            $(".am-popup").remove();
            switch(response.msg){
            	case "success":
	                if (response.oldOBDInfo.msg == "nodata") {
	                	var infoImg =$( 
	                    '<div class="am-popup" id="pic_confirmed">'+
	                      '<div class="am-popup-inner">'+
	                        '<div class="am-popup-hd">'+
	                          '<h4 class="am-popup-title">返回结果</h4>'+
	                          '<span data-am-modal-close class="am-close">&times;</span>'+
	                        '</div>'+
	                        '<div class="am-popup-bd">'+
	                          '<div class="am-tabs" data-am-tabs>'+
	                            '<div id="showresult" class="am-tabs-bd">'+
	                              '<div class="am-tab-panel am-fade am-in am-active" id="tab1">'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                    '<li style="text-align:center;list-style-type:none;">'+
	                                      '<strong>本次结果</strong>'+
	                                      '<img name="confirmed" src="/static/'+response.confirmed_picture_path+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
	                                    '</li>'+
	                                  '</ul>'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                   '<table class="am-table" style="table-layout: fixed;">'+
	                                      '<thead>'+
	                                          '<tr>'+
	                                              '<th width="30%">名称</th>'+
	                                              '<th width="70%">本次结果</th>'+
	                                          '</tr>'+
	                                      '</thead>'+
	                                      '<tbody>'+
	                                          '<tr>'+
	                                              '<td>编码 : </td>'+
	                                              '<td name="code" onclick="ShowText(this.innerHTML)">'+response.code+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>端口占用 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>名称 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.name+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>地址 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.address+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>GPS : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
	                                          '</tr>'+
	                                      '</tbody>'+
	                                  '</table>'+
	                                  '</ul>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
                                      '<button class="am-btn am-btn-success" onclick="developing('+response.id+')">结果下载</button>'+
                                      '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab2\',\'tab1\')">备注</button>'+
                                      '</ul>'+
                                      '<br>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                  '<button  class="am-btn am-btn-secondary" data-am-modal-close>保存</button>'+
                                      '<button class="am-btn am-btn-danger am-fr" data-am-modal-close onclick="ConfirmPic('+response.id+',\'0\')">返回</button>'+
                                      '</ul>'+
	                                 '</div>'+
	                             '</div>'+
	                           '</div>'+
	                         '</div>'+
	                       '</div>'+
	                     '</div>'+
	                    '<br/>'
	                    ).appendTo("body");
					}else{
						var infoImg =$( 
	                    '<div class="am-popup" id="pic_confirmed">'+
	                      '<div class="am-popup-inner">'+
	                        '<div class="am-popup-hd">'+
	                          '<h4 class="am-popup-title">返回结果</h4>'+
	                          '<span data-am-modal-close class="am-close">&times;</span>'+
	                        '</div>'+
	                        '<div class="am-popup-bd">'+
	                          '<div class="am-tabs" data-am-tabs>'+
	                            '<div id="showresult" class="am-tabs-bd">'+
	                              '<div class="am-tab-panel am-fade am-in am-active" id="tab1">'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                    '<li style="text-align:center;list-style-type:none;">'+
	                                      '<strong>上次结果</strong>'+
	                                      '<img name="confirmed" src="/static/'+response.oldOBDInfo.confirmed_picture_path+'" onclick="showImg(this.src)" class="am-thumbnail"/>'+
	                                    '</li>'+
                                      '</ul>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                    '<li style="text-align:center;list-style-type:none;">'+
	                                      '<strong>本次结果</strong>'+
	                                      '<img name="confirmed" src="/static/'+response.confirmed_picture_path+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
	                                    '</li>'+
	                                  '</ul>'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                   '<table class="am-table" style="table-layout: fixed;">'+
	                                      '<thead>'+
	                                          '<tr>'+
	                                              '<th width="20%">名称</th>'+
	                                              '<th width="40%">上次结果</th>'+
	                                              '<th width="40%">本次结果</th>'+
	                                          '</tr>'+
	                                      '</thead>'+
	                                      '<tbody>'+
	                                          '<tr>'+
	                                              '<td>编码 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.code+'</td>'+
	                                              '<td name="code" onclick="ShowText(this.innerHTML)">'+response.code+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>端口占用 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.ports_occupy+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>名称 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.name+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.name+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>地址 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.address+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.address+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>GPS : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.GPS+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
	                                          '</tr>'+
	                                      '</tbody>'+
	                                  '</table>'+
	                                  '</ul>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
                                      '<button class="am-btn am-btn-success" onclick="developing('+response.id+')">结果下载</button>'+
                                      '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab2\',\'tab1\')">备注</button>'+
                                      '</ul>'+
                                      '<br>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                  '<button class="am-btn am-btn-secondary" data-am-modal-close>保存</button>'+
                                      '<button class="am-btn am-btn-danger am-fr" data-am-modal-close onclick="ConfirmPic('+response.id+',\'0\')">返回</button>'+
                                      '</ul>'+
	                                 '</div>'+
	                             '</div>'+
	                           '</div>'+
	                         '</div>'+
	                       '</div>'+
	                     '</div>'+
	                    '<br/>'
	                    ).appendTo("body");
					}
					break;
                case "AllFail":
            		alert(response.msg+': 无法识别端口和设备编号，请手动输入设备信息');
                    var infoImg =$( 
                    '<div class="am-popup" id="pic_confirmed">'+
                      '<div class="am-popup-inner">'+
                        '<div class="am-popup-hd">'+
                          '<h4 class="am-popup-title">返回结果</h4>'+
                          '<span  onclick = "ConfirmPic('+response.id+',\'0\')" class="am-close">&times;</span>'+
                        '</div>'+
                        '<div class="am-popup-bd">'+
                          '<div class="am-tabs" data-am-tabs>'+
                            '<div id="showresult" class="am-tabs-bd">'+
                              '<div class="am-tab-panel am-fade am-in am-active" id="tab1">'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                    '<li style="text-align:center;list-style-type:none;">'+
                                      '<strong>本次结果</strong>'+
                                      '<img name="confirmed" src="/static/'+response.picture_path+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
                                    '</li>'+
                                  '</ul>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                   '<table class="am-table" style="table-layout: fixed;">'+
                                      '<thead>'+
                                          '<tr>'+
                                              '<th width="30%">名称</th>'+
                                              '<th width="70%">本次结果</th>'+
                                          '</tr>'+
                                      '</thead>'+
                                      '<tbody>'+
                                          '<tr>'+
                                              '<td>端口占用 : </td>'+
                                              '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>编码 : </td>'+
                                              '<td><input type="text" name="code" value="'+response.code+'" ></td>'+
                                          '</tr>'+

                                          '<tr>'+
                                              '<td>名称 : </td>'+
                                              '<td><input type="text" name="name" value="'+response.name+'" ></td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>地址 : </td>'+
                                              '<td><input type="text" name="address" value="'+response.address+'" ></td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>GPS : </td>'+
                                              '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
                                          '</tr>'+
                                      '</tbody>'+
                                  '</table>'+
                                  '</ul>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                  '<button class="am-btn am-btn-success" onclick="developing('+response.id+')">结果下载</button>'+
                                  '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab2\',\'tab1\')">备注</button>'+
                                  '</ul>'+
                                  '<br>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                  '<button  class="am-btn am-btn-secondary" onclick = "ConfirmPic('+response.id+',\'0\')">保存</button>'+
                                  '<button class="am-btn am-btn-danger am-fr" data-am-modal-close onclick="ConfirmPic('+response.id+',\'0\')">返回</button>'+
                                  '</ul>'+
                                 '</div>'+
                             '</div>'+
                           '</div>'+
                         '</div>'+
                       '</div>'+
                     '</div>'+
                    '<br/>'
                    ).appendTo("body");
                    break;
                case "QrcodeFail":
            		alert(response.msg+': 无法识别设备编号等信息，请手动输入设备信息');
                	var infoImg =$( 
                    '<div class="am-popup" id="pic_confirmed">'+
                      '<div class="am-popup-inner">'+
                        '<div class="am-popup-hd">'+
                          '<h4 class="am-popup-title">返回结果</h4>'+
                          '<span  onclick = "ConfirmPic('+response.id+',\'0\')" class="am-close">&times;</span>'+
                        '</div>'+
                        '<div class="am-popup-bd">'+
                          '<div class="am-tabs" data-am-tabs>'+
                            '<div id="showresult" class="am-tabs-bd">'+
                              '<div class="am-tab-panel am-fade am-in am-active" id="tab1">'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                    '<li style="text-align:center;list-style-type:none;">'+
                                      '<strong>本次结果</strong>'+
                                      '<img name="confirmed" src="/static/'+response.confirmed_picture_path+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
                                    '</li>'+
                                  '</ul>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                   '<table class="am-table" style="table-layout: fixed;">'+
                                      '<thead>'+
                                          '<tr>'+
                                              '<th width="30%">名称</th>'+
                                              '<th width="70%">本次结果</th>'+
                                          '</tr>'+
                                      '</thead>'+
                                      '<tbody>'+
                                          '<tr>'+
                                              '<td>端口占用 : </td>'+
                                              '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>编码 : </td>'+
                                              '<td><input type="text" name="code" value="'+response.code+'" ></td>'+
                                          '</tr>'+

                                          '<tr>'+
                                              '<td>名称 : </td>'+
                                              '<td><input type="text" name="name" value="'+response.name+'" ></td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>地址 : </td>'+
                                               '<td><input type="text" name="address" value="'+response.address+'" ></td>'+
                                          '</tr>'+
                                          '<tr>'+
                                              '<td>GPS : </td>'+
                                              '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
                                          '</tr>'+
                                      '</tbody>'+
                                  '</table>'+
                                  '</ul>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                  '<button class="am-btn am-btn-success" onclick="developing('+response.id+')">结果下载</button>'+
                                  '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab2\',\'tab1\')">备注</button>'+
                                  '</ul>'+
                                  '<br>'+
                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
                                  '<button  class="am-btn am-btn-secondary" onclick = "ConfirmPic('+response.id+',\'1\')">保存</button>'+
                                  '<button class="am-btn am-btn-danger am-fr" data-am-modal-close onclick="ConfirmPic('+response.id+',\'0\')">返回</button>'+
                                  '</ul>'+
                                 '</div>'+
                             '</div>'+
                           '</div>'+
                         '</div>'+
                       '</div>'+
                     '</div>'+
                    '<br/>'
                    ).appendTo("body");
                    break;
                case "detectbusy":
                case "DetectFail":
                    if (response.msg == "detectbusy") {
                        text = ':端口识别正忙，请重新上传照片识别';
                    }else{
                        text = ':端口识别失败，请选择合适的照片';
                    }
            		alert(response.msg + text);
            		var infoImg =$( 
	                    '<div class="am-popup" id="pic_confirmed">'+
	                      '<div class="am-popup-inner">'+
	                        '<div class="am-popup-hd">'+
	                          '<h4 class="am-popup-title">返回结果</h4>'+
	                          '<span data-am-modal-close class="am-close">&times;</span>'+
	                        '</div>'+
	                        '<div class="am-popup-bd">'+
	                          '<div class="am-tabs" data-am-tabs>'+
	                            '<div id="showresult" class="am-tabs-bd">'+
	                              '<div class="am-tab-panel am-fade am-in am-active" id="tab1">'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                    '<li style="text-align:center;list-style-type:none;">'+
	                                      '<strong>上次结果</strong>'+
	                                      '<img name="confirmed" src="/static/'+response.oldOBDInfo.confirmed_picture_path+'" onclick="showImg(this.src)" class="am-thumbnail"/>'+
	                                    '</li>'+
                                      '</ul>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                    '<li style="text-align:center;list-style-type:none;">'+
	                                      '<strong>本次原图</strong>'+
	                                      '<img name="confirmed" src="/static/'+response._picture_path+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
	                                    '</li>'+
	                                  '</ul>'+
	                                  '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                   '<table class="am-table" style="table-layout: fixed;">'+
	                                      '<thead>'+
	                                          '<tr>'+
	                                              '<th width="20%">名称</th>'+
	                                              '<th width="40%">上次结果</th>'+
	                                              '<th width="40%">本次结果</th>'+
	                                          '</tr>'+
	                                      '</thead>'+
	                                      '<tbody>'+
	                                          '<tr>'+
	                                              '<td>编码 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.code+'</td>'+
	                                              '<td name="code" onclick="ShowText(this.innerHTML)">'+response.code+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>端口占用 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.ports_occupy+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>名称 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.name+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.name+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>地址 : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.address+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.address+'</td>'+
	                                          '</tr>'+
	                                          '<tr>'+
	                                              '<td>GPS : </td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.oldOBDInfo.GPS+'</td>'+
	                                              '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
	                                          '</tr>'+

	                                      '</tbody>'+
	                                  '</table>'+
	                                  '</ul>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
                                      '<button class="am-btn am-btn-success" onclick="developing('+response.id+')">结果下载</button>'+
                                      '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab2\',\'tab1\')">备注</button>'+
                                      '</ul>'+
                                      '<br>'+
                                      '<ul class="am-avg-sm-1 am-thumbnails">'+
	                                  '<button class="am-btn am-btn-secondary"  data-am-modal-close>保存</button>'+
                                      '<button class="am-btn am-btn-danger am-fr" data-am-modal-close onclick="ConfirmPic('+response.id+',\'0\')">返回</button>'+
                                      '</ul>'+
	                                 '</div>'+
	                             '</div>'+
	                           '</div>'+
	                         '</div>'+
	                       '</div>'+
	                     '</div>'+
	                    '<br/>'
	                    ).appendTo("body");
                    break;
            }
            if (response.msg == "success" || response.msg == "QrcodeFail") {
                picpath = response.confirmed_picture_path;
            }else{
                picpath = response.picture_path;
            }
            var notepage = $(//备注提交页
                             '<div class="am-tab-panel am-fade am-in am-active" id="tab2">'+
                                  '<ul class="am-avg-sm-2 am-thumbnails">'+
                                        '<li style="text-align:center;list-style-type:none;">'+
                                            '<table class="am-table" style="table-layout: fixed;">'+
                                                '<thead>'+
                                                    '<tr>'+
                                                        '<th width="30%">名称</th>'+
                                                        '<th width="70%">本次结果</th>'+
                                                    '</tr>'+
                                                '</thead>'+
                                                '<tbody align="left">'+
                                                  '<tr>'+
                                                      '<td>编码 : </td>'+
                                                      '<td id="obd_code" onclick="ShowText(this.innerHTML)">'+response.code+'</td>'+
                                                  '</tr>'+
                                                  '<tr>'+
                                                      '<td>端口 : </td>'+
                                                      '<td onclick="ShowText(this.innerHTML)">'+response.ports_occupy+'</td>'+
                                                  '</tr>'+
                                                  '<tr>'+
                                                      '<td>名称 : </td>'+
                                                      '<td id="obd_name" onclick="ShowText(this.innerHTML)">'+response.name+'</td>'+
                                                  '</tr>'+
                                                  '<tr>'+
                                                      '<td>地址 : </td>'+
                                                      '<td id="obd_address" onclick="ShowText(this.innerHTML)">'+response.address+'</td>'+
                                                  '</tr>'+
                                                  '<tr>'+
                                                      '<td>GPS : </td>'+
                                                      '<td onclick="ShowText(this.innerHTML)">'+response.GPS+'</td>'+
                                                  '</tr>'+
                                                '</tbody>'+
                                            '</table>'+
                                        '</li>'+
                                        '<li style="text-align:center;list-style-type:none;">'+
                                          '<img name="confirmed" src="/static/'+picpath+'"  onclick="showImg(this.src)" class="am-thumbnail"/>'+
                                        '</li>'+
                                  '</ul>'+
                                  '<div class="am-form-group">'+
                                      '<label for="note_category">备注类型：</label>'+
                                      '<select data-am-selected id="note_category">'+
                                          '<option value="0" selected>端口错误</option>'+
                                          '<option value="1">其他备注</option>'+
                                      '</select>'+
                                  '</div>'+
                                  '<div class="am-form-group">'+
                                    '<label for="note">内容：</label>'+
                                    '<br>'+
                                    '<textarea rows="5" id="note" style="width:100%"  placeholder="请输入形如[0,1,0,0,1,1,0]的正确的端口占用情况，0为未占用，1为已占用。"></textarea>'+
                                  '</div>'+
                                  '<div class="essentialInformationBox" hidden>'+
                                      '<div class="productDrawingBox">'+
                                           '<div class="productDescription">备注配图<span class="remark">（5M以内，jpg，png格式，最多三张）</span></div>'+
                                              '<div class="productImg">'+
                                                  '<div id="uploadBox">'+
                                                  '</div>'+
                                                  '<div class="uploadDIv">'+
                                                  '<span>+</span><input type="file" name="file" multiple id="inputs" accept="image/*" class="fileTest" multiple="multiple" />'+
                                                  '</div>'+
                                          '</div>'+
                                      '</div>'+
                                  '</div>'+
                                  '<button id="notesubmit" class="am-btn am-btn-secondary">提交</button>'+
                                  '<button class="am-btn am-btn-warning am-fr"  onclick="cahngetab(\'tab1\',\'tab2\')">返回</button>'+
                                 '</div>'+
                             '</div>').appendTo("#showresult");
            $("#pic_confirmed").modal({closeViaDimmer: 0});
            ///////////////////备注提交js//////////////////////////////////////////////////
            //------------上传图片-------
            $(function() {
            var img = []; //创建一个空对象用来保存传入的图片
            var AllowImgFileSize = 1024*5; //1兆
            $("#note_category").change(function(){
                cat = $("#note_category").val();
                console.log(cat)
                if(cat=="0"){//端口错误
                    $(".essentialInformationBox").hide();
                    $("#note").attr('placeholder',"请输入形如[0,1,0,0,1,1,0]的正确的端口占用情况，0为未占用，1为已占用。");
                }else{
                    $(".essentialInformationBox").show();
                    $("#note").attr('placeholder',"请输入内容！");
                }
            });
            $("#inputs").change(function() {
            var fil = this.files;
            for(var i = 0; i < fil.length; i++) {
            var curr = $('#inputs')[i].files[0].size;
            if(curr > AllowImgFileSize * 1024) { //当图片大于1兆提示
            layer.msg("图片文件大小超过限制 请上传小于1M的文件");
            } else {
            reads(fil[i]);
            img.push($('#inputs')[i].files[0]); //将传入的图片push到空对象中
            }
            }
            if(img.length >= 3) { //判断图片的数量，数量不能超过3张
            $('.uploadDIv').hide();
            } else {
            $('.uploadDIv').show();
            }
            });
            function reads(fil) {
            var reader = new FileReader();
            reader.readAsDataURL(fil);


            reader.onload = function() {
            document.getElementById("uploadBox").innerHTML += "<div class='divImg' id='uploadImg'><img onclick='showImg(this.src)'  src='" + reader.result + "' class='imgBiMG'></div>";
            }
            }
            $('#notesubmit').click(function() {
            //获取input框输入的值
            self = $(this);
            self.attr({"disabled":"disabled"});
            self.removeClass("am-btn-secondary");
            self.addClass("am-btn-danger");
            self.html("提交中...");
            var formData = new FormData(); //创建一个空的formData对象用来保存变量参数
            var arrhh= $('#inputs')[0].files[0]; //
            if ($("#obd_code").html()!="") {
                obd_code = $("#obd_code").html();
                note_category = $("#note_category").val();
                note = $("#note").val();
                formData.append("obd_code",obd_code);
                formData.append("note_category",note_category);
                formData.append("note",note);
            }else{
                alert("OBD编号为空！")
                cahngetab("tab1","tab2");
                self.html("提交");
                self.removeAttr("disabled");
                self.removeClass("am-btn-danger");
                self.addClass("am-btn-secondary");
                return;
            }
            formData.append("img_1", img[0]); //以键值对的形式将这些值保存到formData对象中
            formData.append("img_2", img[1]);
            formData.append("img_3", img[2]);
            $(".am-modal-loading").modal("open");
            $.ajax({ //申请加盟
            type: "post", //请求方式
            dataType: 'json',
            url: '/obdnote', //请求接口
            data: formData, //请求参数（这里将参数都保存在formData对象中）
            processData: false, //因为data值是FormData对象，不需要对数据做处理。
            contentType: false, //默认为true,不设置Content-type请求头
            success: function(data) {
                self.html("提交成功");
                $("#note_category").attr({"disabled":"disabled"})
                $("#note").attr({"disabled":"disabled"})
                self.removeClass("am-btn-danger");
                self.addClass("am-btn-success");
                $(".am-modal-loading").modal("close");
                alert(data);
            }, 
            error:function(XMLHttpRequest, textStatus, errorThrown){
            alert(XMLHttpRequest+"\n"+textStatus+"\n"+errorThrown);
            $(this).removeAttr("disabled");
            self.html("提交");
            self.removeClass("am-btn-danger");
            self.addClass("am-btn-secondary");
            $(".am-modal-loading").modal("close");
            }
            });
            })
            })
            ////////////////备注提交结束/////////////////////////////////////////////////////
        });

        uploader.onError = function( code ) {
        	if(code==="Q_TYPE_DENIED"){
        		alert( "上传类型不对，请重新选择" );
        	}else if(code==="Q_EXCEED_NUM_LIMIT"){
                alert( "上传数量不对，请重新选择" );
        	}else if(code==="F_EXCEED_SIZE"){
        		alert( "文件过大，请重新选择" );
        	}else if(code==="F_DUPLICATE"){
        		alert("重复上传，请重新选择");
        	}
            
        };

        $upload.on('click', function() {
            if ( $(this).hasClass( 'disabled' ) ) {
                return false;
            }
            var picinfo_dummy_array = $picinfo_dummy.val();
            if (picinfo_dummy_array == "") {
                alert("请点击选择图片参数");
                return false;
            }
            console.log(picinfo_dummy_array);
            picinfo_dummy_array = picinfo_dummy_array.split(" ");
            var port_direction = {"端口朝上":"0",
                                  "端口朝上":"1",
                                  "端口朝左":"2",
                                  "端口朝右":"3"},
                zero_port_pos = {"端口朝左":"0",
                                 "端口朝右":"1",
                                 "端口朝上":"2",
                                 "端口朝下":"3"},
                port_sort = {"顺时针":"0",
                             "逆时针":"1"};
            uploader.options.formData.port_direction = port_direction[picinfo_dummy_array[0]]; //$port_direction.val();
            uploader.options.formData.zero_port_pos = zero_port_pos[picinfo_dummy_array[1]]; //$zero_port_pos.val();
            uploader.options.formData.port_sort = port_sort[picinfo_dummy_array[2]]; //$port_sort.val();
            uploader.options.formData.address = $addAddress.val();
            uploader.options.formData.OBDCode = $OBDCode.val();
            uploader.options.formData.GPS = GPS;
            if ( state === 'ready' ) {
                uploader.upload();
            } else if ( state === 'paused' ) {
                uploader.upload();
            } else if ( state === 'uploading' ) {
                uploader.stop();
            }
        });

        $info.on( 'click', '.retry', function() {
            uploader.retry();
        } );

        $info.on( 'click', '.ignore', function() {
        	var arrFile = uploader.getFiles();
        	for(var i = 0,len = arrFile.length;i<len;i++){
        		if(arrFile[i].getStatus()==="error"){
        			uploader.removeFile(arrFile[i]);
        		}
        	}
        } );

        $upload.addClass( 'state-' + state );
        updateTotalProgress();
    });

})( jQuery );
