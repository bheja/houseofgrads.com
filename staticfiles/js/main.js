/*basic javascript*/
$(function(){
if($('#recipient_list').length != 0){
$('#recipient_list').magicSuggest({allowFreeEntries:false,data:'/search/autocomplete/recipients/',method:'get',name:'recipients',hideTrigger:true,placeholder:'Start typing nick of recipients...'});       
}
String.prototype.repeat = function(num){
  return new Array(num + 1).join(this);
}


 var filter = ["anal","anus","ass","asshole","ball kicking","ball licking","ball sucking","bbw","bdsm","big breasts","big tits","bimbos","bitch","black cock","bondage","boner","boob","butt","butthole","clit","clitoris","clusterfuck","cock","cumming","cunt","dick","dildo","eat my ass","ejaculation","erotic","eunuch","faggot","fingering","fisting","fuck","fucked","fucking","f*cking","g-spot","gang bang","genitals","hand job","handjob","hooker","how to kill","how to murder","incest","intercourse","jerk off","jizz","juggs","kinky","squirting","masturbate","milf","motherfucker","nigga","nigger","nipple","nipples","nude","nudity","nympho","orgasm","orgy","paedophile","panties","panty","pedophile","penis","piece of shit","pissing","playboy","porn","porno","pornography","pubes","pussy","rectum","semen","sex","shemale","shit","slut","strip club","taste my","threesome","tit","tits","titties","titty","topless","tranny","twat","vagina","vulva","wank","wet dream","xxx",
"madarchod","behenchod","maderchod","bahanchod","bahenchod","behanchod","bhnchod","chod","maadar","laude","choot"," chut ","chootiya","chutiya","chutiye","loda","lund"," gand ","gaand","gaandu","gandu","ke lode"," sala "," sale ","harami","kamine","kamina","haramkhor"];

$('textarea, input[type=text]').change(function(){
  for(var i=0; i<filter.length; i++){
    var pattern = new RegExp('\\b' + filter[i] + '\\b', 'g');
    var replacement = '*'.repeat(filter[i].length);
	var txt = $(this).val();
	txt = txt.replace(pattern, replacement);
	$(this).val(txt);
  }
});
window.scrollTo(0,0);

	$('#searchTextInput').hover(function(){$(this).siblings('.glyphicon-search').css('color','#000');}
	, function(){$(this).siblings('.glyphicon-search').css('color','#777');}
	);
	$('#searchTextInput').focus(function(){$(this).siblings('.glyphicon-search').css('color','#000');});
	$('.glyphicon-search').hover(function(){$(this).css('color','#000');},
	function(){$(this).css('color','#777');});

	if ($('.dropdown-menu#notificationMenu').css('display')== 'block'){

	}

	 $('#myCarousel').carousel({interval:300000});
	 $('#myCarousel2').carousel({interval:10000});
    
 $("#loginForm").validate({
        rules: {     
           username: { required: true, minlength: 4 },
		   password:{required: true, minlength:4}
        },
        tooltip_options: {
           username: { placement: 'top' },
		   password: { placement: 'top' }
		   },
		submitHandler:function(form){
						var url2 = document.URL;
						
						$("#loginButton").attr('disabled', true);
						$("#loginButton").text('Signing in....');
                        var remember = $('#rememberCheck').prop('checked');
					$.ajax({
								type:"POST",
								dataType:"json",
								url: $("#loginForm").attr('action'),
								data: $("#loginForm").serialize()+'&remember='+remember,
								success: function(data){
								$("#loginButton").attr('disabled', false);
								if (data['success']){
								
								if (url2.indexOf('threads')!=-1 || url2.indexOf('colleges')!=-1 || url2.indexOf('blogs')!=-1){
								window.location=url2;
								}else{
								window.location='/home/';}
								}
								else{
								$("#errMsg").text("Oops, wrong username/password combination, please try again");
								$("#errMsg").addClass("alert alert-danger");
								$("#loginButton").text('Sign in');
								}
								}
           
							});
						
	   
							}});
$("#loginPageForm").validate({
        rules: {     
           identification: { required: true, minlength: 4 },
		   password:{required: true, minlength:4}
        },
        tooltip_options: {
           identification: { placement: 'top' },
		   password: { placement: 'top' }
		   },
		submitHandler:function(form){
						form.submit();
							}});
$("#loginForm2").validate({
        rules: {     
           username: { required: true, minlength: 4 },
		   password:{required: true, minlength:4}
        },
        tooltip_options: {
           username: { placement: 'top' },
		   password: { placement: 'top' }
		   },
		submitHandler:function(form){
						var url2 = document.URL;
						
						$("#loginButton2").attr('disabled', true);
						$("#loginButton2").text('Signing in....');  
					$.ajax({
								type:"POST",
								dataType:"json",
								url: $("#loginForm2").attr('action'),
								data: $("#loginForm2").serialize(),
								success: function(data){
								$("#loginButton2").attr('disabled', false);
								if (data['success']){
								if (url2 == 'http://houseofgrads.com/' || url2 == 'http://www.houseofgrads.com/'){
								window.location='/home/';
								}else{
								window.location=url2;}
								}
								else{
								$("#errMsg2").text("Oops, wrong username/password combination, please try again");
								$("#errMsg2").addClass("alert alert-danger");
								$("#loginButton2").text('Sign in');
								}
								}
           
							});
						
	   
							}});

$("#registrationForm").validate({
        rules: {     
           email: { required: true, email: true },
		   password1:{required: true, minlength:4},
		   password2:{required:true, equalTo: '#password1'}
        },
        tooltip_options: {
           email: { placement: 'right' },
		   password1: { placement: 'right' },
		   password2: { placement: 'right' }
		   },
		submitHandler: function(form) {
							
							$("#signupButton").attr('disabled', true);
							$("#signupButton").text('Signing up....');
	    
							$.ajax({
									type:"POST",
									dataType:"json",
									url: '/register/',
									data: $("#registrationForm").serialize(),
									success: function(data){
											
											$("#signupButton").attr('disabled', false);
											if (data['success']){
											window.location='/registered/'+ data["signedun"]+'/signup_complete/'+data["email"]+'/';
											}
											else {
											$("#errMsg3").html(data["error"]);
											$("#errMsg3").addClass("alert alert-danger");
											$("#signupButton").text('Sign up');
												}
															}
									});
							
							
			}
			});
$('#registrationForm_download').validate({
        rules: {     
           email: { required: true, email: true },
		   password1:{required: true, minlength:4},
		   password2:{required:true, equalTo: '#password1'}
        },
        tooltip_options: {
           email: { placement: 'right' },
		   password1: { placement: 'right' },
		   password2: { placement: 'right' }
		   },
		submitHandler: function(form) {
							
							$("#signupButton").attr('disabled', true);
							$("#signupButton").text('Signing up....');
	    
							$.ajax({
									type:"POST",
									dataType:"json",
									url: '/register/',
									data: $("#registrationForm_download").serialize() + '&flag=true',
									success: function(data){
											
											$("#signupButton").attr('disabled', false);
											if (data['success']){
                                            if (data['flag'] == ''){
											window.location='/registered/'+ data["signedun"]+'/signup_complete/'+data["email"]+'/';
                                            }else{
                                            window.location='/registered/'+ data["signedun"]+'/signup_complete/'+data["email"]+'/'+data['flag']+'/';
                                            }}
											else{
											$("#errMsg3").html(data["error"]);
											$("#errMsg3").addClass("alert alert-danger");
											$("#signupButton").text('Sign up');
												}
															}
									});
							
							
			}
			});
$('#loginModal').on('hidden.bs.modal',function(e){
$('#errMsg').empty();
$('#errMsg').removeClass('alert alert-danger');
});
$("#registrationForm2").validate({
        rules: {     
           email: { required: true, email: true },
		   password1:{required: true, minlength:4},
		   password2:{required:true, equalTo: '#passwordpage1'}
        },
        tooltip_options: {
           email: { placement: 'top' },
		   password1: { placement: 'top' },
		   password2: { placement: 'top' }
		   },
		submitHandler: function(form) {
							
							$("#signupButton2").attr('disabled', true);
							$("#signupButton2").text('Signing up....');
	    
							$.ajax({
									type:"POST",
									dataType:"json",
									url: '/register/',
									data: $("#registrationForm2").serialize(),
									success: function(data){
											
											$("#signupButton2").attr('disabled', false);
											if (data['success']){
											window.location='/registered/'+ data["signedun"]+'/signup_complete/'+data["email"]+'/';
											}
											else {
											var err = data['error'];
											$("#errMsg4").html(data["error"]);
											$("#errMsg4").addClass("alert alert-danger");
											$("#signupButton2").text('Sign up');
												}
															}
									});
							
							
			}
			});
	
$(".postArea label").hide();
$('.postArea').on( 'keyup', '#msgText', function (e){
    $(this).css('height', 'auto' );
    $(this).height( this.scrollHeight );
});
$('.postArea').find( 'textarea' ).keyup();

$('#followThreadBtn').click(function(){
    var objname = $(this).attr('name');
	if ($('#followThreadBtn').text() == 'Follow'){

	$.post('/follow/followobj/',{'objname':objname,'thread':'True'},function(){$('#followThreadBtn').text('Unfollow');
	$('#followThreadBtn').removeClass('btn-success');
	$('#followThreadBtn').addClass('btn-default');
    $('#followThreadBtn').css('font-weight','bold');                                                                           
	});
	}else{

	$.post('/follow/unfollowobj/',{'objname':objname,'thread':'True'},function(){$('#followThreadBtn').text('Follow');
$('#followThreadBtn').removeClass('btn-default');
	$('#followThreadBtn').addClass('btn-success');
	 });
	}
	});

  $("#postForm").submit(function(event){
 var extra_context = new String();
if ($(this).find('.urlive-link').length > 0){
$('.postPanel .glyphicon-remove').hide();
var extra_context = new String($('<div>').append($(this).find('.liveContainer').clone()).remove().html()); 
$('.postArea .liveContainer').empty();
}
var postparam = new Array();
postparam = $('#postForm').find('input').map(function(){return $(this).val();}).get();
tinyMCE.triggerSave();

 for(var i=0; i<filter.length; i++){
    var pattern = new RegExp('\\b' + filter[i] + '\\b', 'g');
    var replacement = '*'.repeat(filter[i].length);
	var txt = $('#text').val();
	txt = txt.replace(pattern, replacement);
	$('#text').val(txt);}
if ($('#text').val() !=''){
    if ($('.qq-upload-success').length>0){$('.qq-upload-success').remove();}
$("#submitPost").text("Posting..");
$("#submitPost").attr("disabled",true);
var url = $('#postForm').attr('action');
    
$.post(url,{'csrfmiddlewaretoken':postparam[0],'content':$('#text').val(),'author':postparam[1],'date':postparam[2],'thread':postparam[3],'img_url':$('#img_url').val(),'preview':extra_context},function(data2){
   $('#img_url').val(''); 
$("#submitPost").attr("disabled",false);$("#submitPost").text("Post");
      var uploader = new qq.FileUploader( {
            action: "/upload/image/",
			allowedExtensions: ['png','jpeg','jpg','gif','ico','bmp'],
            element: $('#file-uploader')[0],
			listElement: $('.uploadedFilePanel')[0],
            multiple: true,
            onComplete: function( id, fileName, responseJSON ) {
              if( responseJSON.success )
              {
              file_name = fileName + "jPeFhhi"
              $('.uploadedFilePanel').append('<input type="hidden" value="'+responseJSON.path+'" id="'+file_name+'">')
			  }else{}},
            onAllComplete: function( uploads ) {
            $('#img_url').val('');
			  for(i=0;i<uploads.length;i++){
			  $('#img_url').val($('#img_url').val() + ' ' + uploads[i]['response']['path']);
			  }

			  },
            params: {
              'csrf_token': postparam[0],
              'csrf_name': 'csrfmiddlewaretoken',
              'csrf_xname': 'X-CSRFToken',
            },
          }) ;
$('.qq-upload-button').tooltip();
$('.uploadedFilePanel').hide();
tinyMCE.activeEditor.setContent('<p></p>');
$.get('/post/latest/', function(data){
			$('#newsFeed').prepend(data);
			var texta = $('.newsFeedWrapper textarea')[0];
			var latestid = texta.id;
			var latid = latestid.replace(/[^a-z\_]+/ig,"");
			if(latid == 'id_new_comment'){
			 latestid = latestid.replace(/[^0-9]+/ig,"");
			 latestid = parseInt(latestid) +1;
			$('#id_new_comment1').attr('id','id_new_comment'+latestid);
			}
			
			
    $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
    $('a').popover('hide');
			});
     
},"json");
}else{$('.postArea').attr('title','Please type something...');$('.postArea').tooltip('show');setTimeout('$(".postArea").tooltip("destroy")',3000);}
	event.preventDefault();

	});
	
 $("#shareForm").submit(function(event){
 event.preventDefault();
var cont = $('<div>').append($(this).find('.liveContainer2').clone()).remove();
cont.find('.feedText').removeClass('feedText');
cont = cont.html();

var extra_context = new String(cont); 
var postparam = new Array();
postparam = $('#shareForm').find('input').map(function(){return $(this).attr('value');}).get();
tinyMCE.triggerSave();
$("#submitShare").text("Posting..");
$("#submitShare").attr("disabled",true);

var url = $('#shareForm').attr('action');
$.post(url,{'csrfmiddlewaretoken':postparam[0],'content':$('#shareText').val(),'date':postparam[1],'initial-date':postparam[2],'preview':extra_context},function(data2){
$("#submitShare").attr("disabled",false);$("#submitShare").text("Post");$('#shareModal').modal('hide');
tinyMCE.activeEditor.setContent('<p></p>');
    $.get('/post/latest/', function(data){
			$('#newsFeed').prepend(data);
			var texta = $('.newsFeedWrapper textarea')[0];
			if (typeof texta == 'undefined'){var latestid = '1';}else{var latestid = texta.id}
			var latid = latestid.replace(/[^a-z\_]+/ig,"");
			if(latid == 'id_new_comment'){
			 latestid = latestid.replace(/[^0-9]+/ig,"");
			 latestid = parseInt(latestid) +1;
			$('#id_new_comment1').attr('id','id_new_comment'+latestid);
			}window.scrollTop();
    $('a.deleteLink').popover({html:true,placement:'bottom'});
    });
},"json");

	

	});

$("#postThreadForm").submit(function(event){
 var extra_context = new String();
if ($(this).find('.urlive-link').length > 0){
$('.postPanel .glyphicon-remove').hide();
var extra_context = new String($('<div>').append($(this).find('.liveContainer').clone()).remove().html()); 
$('.postArea .liveContainer').empty();
}
var postparam = new Array();
postparam = $('#postThreadForm').find('input').map(function(){return $(this).val();}).get();
tinyMCE.triggerSave();
if ($('.qq-upload-success').length>0){$('.qq-upload-success').remove();}
 for(var i=0; i<filter.length; i++){
    var pattern = new RegExp('\\b' + filter[i] + '\\b', 'g');
    var replacement = '*'.repeat(filter[i].length);
	var txt = $('#text').val();
	txt = txt.replace(pattern, replacement);
	$('#text').val(txt);}
if ($('#text').val() !=''){
$("#submitPost").text("Posting..");
$("#submitPost").attr("disabled",true);
var url = $('#postThreadForm').attr('action');
    
$.post(url,{'csrfmiddlewaretoken':postparam[0],'content':$('#text').val(),'author':postparam[1],'date':postparam[2],'thread':postparam[3],'img_url':$('#img_url').val(),'preview':extra_context},function(data2){
   $('#img_url').val(''); 
$("#submitPost").attr("disabled",false);$("#submitPost").text("Post");
     var uploader = new qq.FileUploader( {
            action: "/upload/image/",
			allowedExtensions: ['png','jpeg','jpg','gif','ico','bmp'],
            element: $('#file-uploader')[0],
			listElement: $('.uploadedFilePanel')[0],
            multiple: true,
            onComplete: function( id, fileName, responseJSON ) {
              if( responseJSON.success )
              {
              file_name = fileName + "jPeFhhi"
              $('.uploadedFilePanel').append('<input type="hidden" value="'+responseJSON.path+'" id="'+file_name+'">')
			  }else{}},
            onAllComplete: function( uploads ) {
            $('#img_url').val('');
			  for(i=0;i<uploads.length;i++){
			  $('#img_url').val($('#img_url').val() + ' ' + uploads[i]['response']['path']);
			  }

			  },
            params: {
              'csrf_token': postparam[0],
              'csrf_name': 'csrfmiddlewaretoken',
              'csrf_xname': 'X-CSRFToken',
            },
          }) ;
$('.qq-upload-button').tooltip();
$('.uploadedFilePanel').hide();
tinyMCE.activeEditor.setContent('<p></p>');
$.get('/post/thread/latest/',{'id':postparam[3]}, function(data){
            
			$('#postFeed').prepend(data);
			var texta = $('.newsFeedWrapper textarea')[0];
			var latestid = texta.id;
			var latid = latestid.replace(/[^a-z\_]+/ig,"");
			if(latid == 'id_new_comment'){
			 latestid = latestid.replace(/[^0-9]+/ig,"");
			 latestid = parseInt(latestid) +1;
			$('#id_new_comment1').attr('id','id_new_comment'+latestid);
			}
			
    $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
    $('a').popover('hide');
			});
     
},"json");
}else{$('.postArea').attr('title','Please type something...');$('.postArea').tooltip('show');setTimeout('$(".postArea").tooltip("destroy")',3000);}
	event.preventDefault();

	});
	
  $('#discussionBlock').endlessPaginate({divLatDiscuss: true,  paginateOnScroll: true, paginateOnScrollMargin: 1
});
    
$("#createThreadButton").click(function(){
 tinymce.init({
    selector: "#textThread",
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize"
    ],
	skin:'gradp',
    height: 200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link image emoticons ",
menubar: false, statusbar: false
});
});


$("#messageForm").validate({
        rules: {     
           to: { required: true, minlength: 4 },
		   body:{required: true}
        },
        tooltip_options: {
           to: { placement: 'top' },
		   body: { placement: 'top' }
		   },
		submitHandler: function(form){
						
							var data = $('#messageForm').find('input').map(function(){return $(this).val();}).get();
                            var data2 = data;
                            var recipients = data2.splice(2);
                            if (recipients.length>1){
                            recipients  = recipients.join(',');
                            $.trim(recipients);
                            recipients = recipients.substring(0,recipients.length-1);
                            }
                            else{
                            recipients  = recipients.join(',');
                            }
							
                            if (recipients != '' && $.trim($('#textAreaMsg').val()) != ''){
                                $("#submitMsg").text("Sending..");
							$("#submitMsg").attr("disabled",true);
							$.ajax({
									type:"POST",
									dataType:"json",
									url:'/messages/compose/',
									data: {'csrfmiddlewaretoken':data[0],'recipients':recipients,'text':$('#textAreaMsg').val()},
									success: function(data2){
											$("#textAreaMsg").val('');
											$("#submitMsg").attr("disabled",false);$("#submitMsg").text("Send");
											$('#messageCompose').modal('hide');
											}
									});}else{
                            if(recipients == ''){
                                var sel =  $('#recipient_list');
                           sel.attr('title','Please enter atleast one recipient...');
                            }else{
                                var sel = $('#textAreaMsg');
                            sel.attr('title','No message to send...');
                            }sel.tooltip('show');setTimeout("$('#textAreaMsg').tooltip('destroy')",3000);setTimeout("$('#recipient_list').tooltip('destroy')",3000);
                            }
									
										}
							});

    $('#mainSearchForm').submit(function(e){
        var query = $('#mainSearchBox').val(); 
        if (query != '' && query.length > 3){
        $(this).submit();}
        else{e.preventDefault();
            $('#mainSearchBox').attr('title', 'Please type in something (more than 3 chars long)');
             $('#mainSearchBox').tooltip('show');
             setTimeout(" $('#mainSearchBox').tooltip('destroy')", 3000);
            }
});
    

$("#ThreadForm").validate({
        rules: {     
           name: { required: true, minlength: 6 },
		   brief:{required: true, minlength: 10}
        },
        tooltip_options: {
           name: { placement: 'right' },
		   brief: { placement: 'right' }
		   },
		submitHandler: function(form) {
							var stream = $("#streamSelect").val();
							tinyMCE.triggerSave();
							$("#submitThread").attr('disabled', true);
							$("#submitThread").text('Creating thread....');
							var data = $("#ThreadForm").find('input').map(function(){return $(this).val();}).get();
                            console.log(data);
							$.ajax({
									type:"POST",
									dataType:"json",
									url: '/createthread/',
									data: {'csrfmiddlewaretoken':data[0],'name':data[1],'stream':stream,'brief':$('#textThread').val()},
									success: function(data){
											if (data['success']){
											$("#submitThread").attr('disabled', false);
											$("#submitThread").text('Create');
											window.location = '/threads/'+data['tid']+'/'
												}
												else{
												
												}
												}
									
									});
							
			}});


$('#likefollowBtn').click(function(){
	var username = $(this).siblings('[name="like_sender"]').val();
	
	if ($('#followBtn').text() == 'follow'){
	
	$.post('/followobj/',{'objname':username,'thread':'False'},function(){$('#followBtn').text('Unfollow');$('#followBtn').addClass('greenBg');});
	}else{
	
	$.post('/unfollowobj/',{'objname':username,'thread':'False'},function(){$('#followBtn').text('follow');$('#followBtn').removeClass('greenBg');});
	}
	});	


$('#newsFeed').endlessPaginate({paginateOnScroll: true,  paginateOnScrollChunkSize: 5, paginateOnScrollMargin: 1,
onCompleted: function(context, fragment){
               $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
				  var is_active = $('#actch123').val(); 
				 if(is_active == 'False'){$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;e.stopPropagation();$('#inActiveModal').modal('show');});
				 }
				  }
				  
					
});
$('#postFeed').endlessPaginate({paginateOnScroll: true,  paginateOnScrollChunkSize: 5, paginateOnScrollMargin: 1,
onCompleted: function(context, fragment){
   $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
			 var is_active = $('#actch123').val(); 
				 var is_logged = $('#logch123').val();
				 
				 if (is_logged == 'True'){
				 if(is_active == 'False'){$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;e.stopPropagation();$('#inActiveModal').modal('show');});
				 }
				 }else{$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;e.stopPropagation();$('#loginModal').modal('show');});
				 }
				 
				}	
});

$('#followedthreads').endlessPaginate({paginateOnScroll: true,  paginateOnScrollChunkSize: 5, paginateOnScrollMargin: 1,
onCompleted: function(context, fragment){}
});

$('#checkUserText').blur(function(event){
event.preventDefault();
event.stopPropagation();
var username = $(this).val();
var regexp = /^[\.\w]+$/;
if (!regexp.test(username)){$('#checkUserText').attr('title','Your nick should contain only alphabets, numbers, dots and underscores.. ');
							$(this).addClass('validationErr');
							$(this).tooltip();
							$(this).tooltip('show');}else{
$.post('/check/user/',{'username':username}, function(data){
if (data["exist"]=='true')
{$('#checkUserText').attr('title',"That one's taken, sorry...");
$('#checkUserText').addClass('validationErr');
$('#checkUserText').tooltip();
$('#checkUserText').tooltip('show');
$('#checkUserText').focus();
}else{$('#checkUserText').attr('title','');
$('#checkUserText').removeClass('validationErr');
if($('#checkUserText').attr('data-original-title')){
$('#checkUserText').tooltip('destroy');}
return true;
}
});}

});
$('.avatarSelect').click(function(){
$('.avatarSelect').each(function(){$(this).removeClass('selectedAvatar')});
$(this).addClass('selectedAvatar');
$('#profileImg').val('');
// var url = $(this).find('img').attr('src');
// var email = $('#email').val();
// $.post('/mugshot/select/',{'url':url,'email':email},function(data){});
return false;
});

$('#profileForm').validate({
        rules: {     
           username: { required: true, minlength: 4 },
		   mugshot:{required: true},
		   stream:{required: true}
        },
        tooltip_options: {
           username: { placement: 'top' },
		   mugshot:{ placement: 'top' },
		   stream:{placement : 'top'}
		   },
		messages:{username:"Please specify your nick..",stream:"Specifying your GATE paper helps us show you contents relevant to your subject..."},
		submitHandler: function(form){
							
							var postArray = $('#profileForm').find('input:not(input[type=file])').map(function(){return $(this).val();}).get();
							
							if(postArray.length == 7){postArray.splice(2,1);}
							
							var regexp = /^[\.\w]+$/;
							if (!regexp.test(postArray[1])){$('#checkUserText').attr('title','Your nick should contain only alphabets, numbers, dots and underscores.. ');
							$('#checkUserText').addClass('validationErr');
							$('#checkUserText').tooltip('show');}else{
							
							
							$("#submitProfile").attr("disabled",true);
							var url = $('.selectedAvatar').find('img').attr('src');
							 $.ajax({
							 type: 'POST',
							 url:'/profile/signup/complete/',
							 data:{'csrfmiddlewaretoken':postArray[0],'username':postArray[1],'firstname':postArray[2],'lastname':postArray[3],'email':postArray[4],'gate_stream':$('#profileStreamSelect').val(),'mugshot':$('#profileImg').val()},
							 success:function(data){
                                 var stream_gate = $('#profileStreamSelect').val();
                                 
							var slug = data['slug'];
							 if (data['success']=='true'){
                                 if ($('#flagVal').val() != ''){download_init(stream_gate);}
                             var slug = data['slug'];
                                 download_register(url,slug);
                             }
                             }
							 });
							 
							 }}});
$('#editProfileForm').validate({
        rules: {     
           age: { minlength: 2,digits: true },
		   location:{minlength:3, digits:false}
		   
        },
        tooltip_options: {
           age: { placement: 'top' },
		   location:{ placement: 'top' }
		   },
		submitHandler: function(form){
							var username = $('#identificationString').val();
							var postArray = $('#editProfileForm').find('input:not(input[type=file])').map(function(){return $(this).val();}).get();	     
                            var checkArr2 = [];
                            for (j=0;j<postArray.length;j++){checkArr2.push(postArray[j]);}
							var checkArr = $('#initial_values').find('input:not(input[type=file])').map(function(){return $(this).val();}).get();
                            checkArr2.push($('#id_about_me').val());
							checkArr2.splice(0,1);
							var check = checkArr.join('');
                            var initial = checkArr2.join('');
                            if ($('.selectedAvatar').length >0 ){var is_mugshot = true;}else{var is_mugshot =false;}
							if (check!=initial || is_mugshot){
							$('#updateProfile').attr('title','update');
							$('#updateProfile').tooltip('destroy');
							if (postArray.length == 7){postArray.splice(3,1);}
							
							$("#submitProfile").text("Starting up..");
							$("#submitProfile").attr("disabled",true);
							var url = $('.selectedAvatar').find('img').attr('src');
							
							if (postArray[4]==''){postArray[4]='0';}
							
							 $.ajax({
							 type: 'POST',
							 url:'',
							 data:{'csrfmiddlewaretoken':postArray[0],'first_name':postArray[1],'last_name':postArray[2],'about_me':$('#id_about_me').val(),'location':postArray[3],'age':postArray[4],'mugshot':$('#profileImg').val()},
							 success:function(data){
                            if (typeof url == 'undefined' || url == ''){}else{ 
							 $.post('/mugshot/select/',{'url':url},function(data){});}
							 if (data['success']=='true'){ 
							 $('#editProfileForm .success-message').html('<div class="alert largeFont alert-success">Your profile was updated successfully.</div>');
                                 if (typeof url == 'undefined' || url == ''){$('#mugshotImage').attr('src',$('#profileImg').val());}else{ $('#mugshotImage').attr('src',url);}
							 if ($('#mugshotImage').attr('src') == ''){$('#mugshotImage').attr('src',$('.navThumb').attr('src'));}
                             window.location = '/'+username+'/';
                             }
                           
							 }
							 });
							 }else{$('#updateProfile').attr('title','Please fill out atleast one field..');
							 $('#updateProfile').tooltip('show');
							 setTimeout('$("#updateProfile").tooltip("destroy")',3000);
							 }
							}
							 });
							 
$('#password_change_form').validate({
			rules: {     
           old_password: { minlength: 4,required: true },
		   new_password1:{required: true, minlength:4},
		   new_password2:{required:true, equalTo: '#id_new_password1'}
        },
		 tooltip_options: {
           old_password: { placement: 'top' },
		   new_password1:{ placement: 'top' },
		   new_password2:{placement : 'top'}
		   },
		  submitHandler: function(form){
		  if ($('#id_old_password').val() == $('#id_new_password1').val()){
		  $('#updatePassword').attr('title',"New password can't be same as current password");
		  $('#updatePassword').tooltip('show');
		  setTimeout(' $("#updatePassword").tooltip("destroy")',2000);
		  }else{
		  form.submit();
		  }}
});
$('#email_change_form').validate({
			rules: {     
           email: {required: true, email:true }
        },
		 tooltip_options: {
           email:{ placement: 'top' }
		   },
		  submitHandler: function(form){
		  
		  form.submit();
		  }
});
$('#blogForm').validate({
			rules: {     
           title: { minlength: 6,required: true },
		   blog_content:{required: true, minlength:400},
		   tag:{required:true}
            
        },
		 tooltip_options: {
           title: { placement: 'top' },
		   blog_content:{ placement: 'top' },
		   tag:{placement : 'right'}
		   },
		  submitHandler: function(form){
                        tinyMCE.triggerSave();
		              var a = $('#blogForm').serializeArray();
              var key;
           var regexp = /^[ A-Za-z0-9_.:,\[\]\(\)]*$/;
              if (a[5]['value'] =="draft"){var published="false";key ='draft'}else{var published = "true";key="publish";}
              if (regexp.test(a[2]['value'])){
        $.post('/create/blog/'+key+'/',{'author':a[1]['value'],'csrfmiddlewaretoken':a[0]['value'],'title':a[2]['value'],'blog_content':a[3]['value'],'tag':a[4]['value'],'img_url':$('#img_url').val()},function(data){
            if(data['success']=="true"&&published=="true"){
            window.location = '/blogs/'+data['id']+'/'+data['slug']+'/';
            }else if(data['success']=="true"&&published=="false"){
            window.location = '/blogs/all/drafts/';
            }else{}
        });
         
}else{ $('#blogTitleText').attr('title','Only alphanumerics, underscores, square brackets, parentheses, colons, comma and dots allowed..');
      $('#blogTitleText').tooltip('show');
      window.scrollTop();
      setTimeout(" $('#blogTitleText').tooltip('destroy')", 5000);}
          }});
$('#editBlogForm').validate({
			rules: {     
           title: { minlength: 6,required: true },
		   blog_content:{required: true, minlength:400},
		   tag:{required:true}
            
        },
		 tooltip_options: {
           title: { placement: 'top' },
		   blog_content:{ placement: 'top' },
		   tag:{placement : 'right'}
		   },
		  submitHandler: function(form){
                        tinyMCE.triggerSave();
		              var a = $('#editBlogForm').serializeArray();
              var key;var pk = $('#kpOOGh').val()
              
              if (a[5]['value'] =="draft"){var published="false";key ='draft'}else{var published = "true";key="publish";}
             
        $.post('/blogs/edit/'+pk+'/'+key+'/',{'author':a[1]['value'],'csrfmiddlewaretoken':a[0]['value'],'title':a[2]['value'],'blog_content':a[3]['value'],'tag':a[4]['value'],'img_url':$('#img_url').val()},function(data){
            if(data['success']=="true"&&published=="true"){
            window.location = '/blogs/'+data['id']+'/'+data['slug']+'/';
            }else if(data['success']=="true"&&published=="false"){
            window.location = '/blogs/all/drafts/';
            }else{}
        });
         
}});
							 
	$('.feedFollow').click(function(){
$curr = $(this);
var objname = $(this).attr('id');
$.post('/follow/followobj/',{'objname':objname,'thread':'False'},function(data){$curr.attr('disabled',true);$curr.text('Following');
$curr.parents('.followPanel').addClass('disabledFollow');
});
});
$('.feedThreadFollow').click(function(){
$curr = $(this);
var objname = $(this).attr('id');
$.post('/follow/followobj/',{'objname':objname,'thread':'True'},function(data){$curr.attr('disabled',true);$curr.text('Following');
});
});
$('.followingThread').click(function(){
$curr = $(this);
var objname = $(this).attr('id');
if ($.trim($curr.text())=='Unfollow'){
$.post('/follow/unfollowobj/',{'objname':objname,'thread':'True'},function(data){$curr.text('Follow');$curr.removeClass('btn-default');
                                                                                 $curr.addClass('btn-success');
});
}else{
$.post('/follow/followobj/',{'objname':objname,'thread':'True'},function(data){$curr.text('Unfollow');$curr.removeClass('btn-success');
                                                                                 $curr.addClass('btn-default');
});
}
});

$('#configFeed').click(function(e){
var len = $('.disabledFollow').length;

if(len<3){$('.usertip').attr('title','Please follow at least 3 users to build your feed');
$('.usertip').tooltip('show');
$('body').scrollTop(0);
return false;}
window.location = '/home/';
}); 
    
$('#messageBtn').click(function(){
var un = $(this).attr('data-username');
var is_new = $(this).attr('data-new');
if (typeof is_new == 'undefined' || is_new == 'true'){
    var ms = $('#recipient_list').magicSuggest({});
    ms.setValue([un]);
$(this).attr('data-new','false');
}
});

});

function highlightpanel(url,username){

if (url == 'http://houseofgrads.com/home/' || url == 'http://www.houseofgrads.com/home/' || url == 'http://houseofgrads.com/home#' || url == 'http://www.houseofgrads.com/home#' || url == 'http://houseofgrads.com/home/#_=_'){$('#sideMenu').find('#sp1').addClass('active greenBg');}
else if(url == 'http://houseofgrads.com/'+username+'/' || url == 'http://www.houseofgrads.com/'+username+'/' ||url=='http://houseofgrads.com/myprofile/edit/' || url == 'http://www.houseofgrads.com/myprofile/edit/'){$('#sideMenu').find('#sp4').addClass('active greenBg');}
else if(url=='http://houseofgrads.com/following/threads/'||url=='http://www.houseofgrads.com/following/threads/'){$('#sideMenu').find('#sp3').addClass('active greenBg');}
}
function convForm(){
	$.get('/messages/create/',function(data){$('#convFormDiv').html(data);});
}
$('#messagePostForm').submit(function(event){
$.post('/messages/create/', function(data){});
event.preventDefault;
});
function getFeedMain(){
				
				var is_active = $('#isactive').val(); 
				 if(is_active == 'False'){$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;$('#inActiveModal').modal('show');});
                    $('#newsFeed').data('count',1);                      }
    $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
				}
function likeList(x){
		var objid = $(x).parents('.postStatBox').siblings('[name="object_pk"]').attr("value");
		
		$.get('/like/likelist/'+objid+'/',function(data){$('#likeList .modal-body').html(data)});
		}
function getCommentList(x, post_id){
var post_id = post_id;
$.get('/comments/list/'+ post_id +'/', function(data){
		$(x).siblings('.parentCommentList').html(data);
		$(x).siblings('.parentCommentList').find('.commentTxt').filter(function(i){
		
		var a = $(this).text();
		$(this).html(a);
		
		});
		$(x).hide();
       
                   $('a.deleteCommentLink').popover({html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
		});
}
function toggleBg(x){
$(x).toggleClass('bgGreen');
}
function showoptionfeed(x){
$(x).find('a.hiding').show();
$(x).find('a.hiding').show();

}
function hideoptionfeed(x){
$(x).find('a.hiding').hide();
$(x).find('a.hiding').hide();
};
function showtooltipfeed(x){
$(x).tooltip('show');
}
function hidetooltipfeed(x){
$(x).tooltip('hide');
}
function postComm(x){
var blog =false;
if($('#id_blog_comment').length >0){blog = true;}
var textid = $(x).parents('.commentForm').children('textarea').attr('id');
var edinst = tinymce.EditorManager.get(textid);
edinst.editorManager.triggerSave();
 String.prototype.repeat = function(num){
  return new Array(num + 1).join(this);
}
 var filter = ["anal","anus","ass","asshole","ball kicking","ball licking","ball sucking","bbw","bdsm","big breasts","big tits","bimbos","bitch","black cock","bondage","boner","boob","butt","butthole","clit","clitoris","clusterfuck","cock","cumming","cunt","dick","dildo","eat my ass","ejaculation","erotic","eunuch","faggot","fingering","fisting","fuck","fucked","fucking","f*cking","g-spot","gang bang","genitals","hand job","handjob","hooker","how to kill","how to murder","incest","intercourse","jerk off","jizz","juggs","kinky","squirting","masturbate","milf","motherfucker","nigga","nigger","nipple","nipples","nude","nudity","nympho","orgasm","orgy","paedophile","panties","panty","pedophile","penis","piece of shit","pissing","playboy","porn","porno","pornography","pubes","pussy","rectum","semen","sex","shemale","shit","slut","strip club","taste my","threesome","tit","tits","titties","titty","topless","tranny","twat","vagina","vulva","wank","wet dream","xxx",
"madarchod","behenchod","maderchod","bahanchod","bahenchod","behanchod","bhnchod","chod","maadar","laude","choot"," chut ","chootiya","chutiya","chutiye","loda","lund"," gand ","gaand","gaandu","gandu","lode "," sala "," sale ","harami","kamine","kamina","haramkhor"];
  for(var i=0; i<filter.length; i++){
    var pattern = new RegExp('\\b' + filter[i] + '\\b', 'g');
    var replacement = '*'.repeat(filter[i].length);
	var txt = $('#'+textid).val();
	txt = txt.replace(pattern, replacement);
	$('#'+textid).val(txt);
  }
$('#'+textid).parents('.commentBox').find('.parentCommentList').append('<img class="imgLoading" src="/static/img/loading.gif"/>');
var a = $(x).parents('.commentForm').siblings("input").map(function(){return $(this).attr("value");}).get();
a[4]= $('#'+textid).val();
edinst.setContent('<p></p>');
var url_comm;
if (blog){url_comm = '/comments/blogs/'}else{url_comm='/comments/'}
$.ajax({
        type:"POST",
		dataType:"json",
        url:url_comm,
        data:{'content_type':a[0],'object_pk':a[1],'timestamp':a[2],'security_hash':a[3],'comment':a[4],'csrfmiddlewaretoken': a[5]},
        success: function(data1){
		
		 $.get('/ajaxpostrefresh/'+data1['commentid']+'/',function(data){
             $('#'+textid).parents('.commentBox').find('.parentCommentList').find(".imgLoading").remove();
		 $('#'+textid).parents('.commentBox').find('.parentCommentList').append(data);
		
              $('a.deleteCommentLink').popover({
    html:true,placement:'bottom'});
     $('a.reportCommentLink').popover({html:true,placement:'bottom'});
             edinst.remove();
		 });
		 
		}
          });
		  

$('#'+textid).siblings('.hiding').hide();

}
function notification_list(){
	$('.glyphicon-globe + .badge').css('visibility','hidden');
	$.get('/notification/',function(data){
	
	$('#notificationContentInner').html(data);
	  $('#notificationContent').perfectScrollbar();
	
	 
  $('#notificationContent').endlessPaginate({divScroll: true,  paginateOnScrollChunkSize: 5, paginateOnScrollMargin: 1
});

        
	 $.post('/notification/notification/read/',function(data){});
	$('#notificationContentInner li').hover(function(){
$(this).css('background-color','#F8E4C1');
},function(){$(this).css('background-color','#fff');});
	});
	
	}
	function message_list(){
	
	$.get('/messages/list/',function(data){
	$('#messageContentInner').html(data);
	  $('#messageContent').perfectScrollbar();
	  $('.msgTxtNotify').each(function(i){
				 var b = $(this).text();
				 $(this).html(b);}
				);
		 $('#messageContent').endlessPaginate({divMsgScroll: true,  paginateOnScrollChunkSize: 5, paginateOnScrollMargin: 1
});
	});
	}
	function search_result(){
	var query= $('#searchTextInput').val();
	if ($('#searchTextInput').val()!=''){
	$.get('/search/autocomplete/',{'q':query},function(data){
	if (data != ''){
	$('.ajaxSearchResult').html(data);
	$('.ajaxSearchResult').fadeIn();
	}
	});   
	}
	else{
	$('.ajaxSearchResult').fadeOut();
	}
	}
function search_result_main(){
	var query= $('#mainSearchBox').val();
	if ($('#mainSearchBox').val()!=''){
	$.get('/search/autocomplete/',{'q':query},function(data){
	if (data != ''){
	$('.ajaxMainSearchResult').html(data);
	$('.ajaxMainSearchResult').fadeIn();
	}
	});   
	}
	else{
	$('.ajaxMainSearchResult').fadeOut();
	}
	}
	function submitForm(){
	
	$('#searchNavigationForm').submit();
	}
function block(x,y){
$.post('/block/' + y +'/',function(data){
$(x).hide();
$('#unblockBtn').show();
$('#followBtn').fadeOut();
$('#followBtn').removeClass('greenBg').text('follow');

$('#newsFeed').fadeOut();
$('#messageBtn').fadeOut();
});
}
function unblock(x,y){
$.post('/unblock/' + y + '/',function(data){
$(x).hide();
$('#blockBtn').show();
$('#followBtn').fadeIn();
$('#messageBtn').fadeIn();
$.get('/myactivity/',{'username':username}, function(data){
				$('#newsFeed').fadeIn();
				$('#newsFeed').html(data);
				$('.contentNewsFeed span').each(function(i){
					
				 $('#newsFeed').data('count',1);
				});
				if (username != requestuser)
				{
				$('.glyphicon-remove').remove();
				}
			});
});
}

 
function selectTag(x,el){
var str = tinymce.activeEditor.getContent();
var modifiedstr = str.substring(0,str.lastIndexOf(" "));
if (str.lastIndexOf('</ol>') == str.length-5 || str.lastIndexOf('</ul>') == str.length-5)
{
if(str.lastIndexOf('</ul>') == str.length-5){
tinymce.activeEditor.setContent(modifiedstr +' '+ '<a href="../'+x+'/" class="tinymceTag">'+x+'</a>'+'</li></ul>');}
else{tinymce.activeEditor.setContent(modifiedstr +' '+ '<a href="../'+x+'/" class="tinymceTag">'+x+'</a>'+'</li></ul>');}
if ($(el).parents('.tagUser').length>0){$(el).parents('.tagUser').remove();}else{$('#tagUser').remove();}
$('#tagHidden').val($('#tagHidden').val() + ' '+x);
}
else{
tinymce.activeEditor.setContent(modifiedstr + ' '+ '<a href="../'+x+'/" class="tinymceTag">'+x+'</a>'+'</p>');
if ($(el).parents('.tagUser').length>0){$(el).parents('.tagUser').remove();}else{$('#tagUser').remove();}
$('#tagHidden').val($('#tagHidden').val() + ' '+x);
}
}
$.fn.selectRange = function(end) {
    return this.each(function() {
        if (this.setSelectionRange) {
            this.focus();
            this.setSelectionRange(end,end);
        } else if (this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
             range.moveStart('character', end);
            range.moveEnd('character', end);
		range.focus();
        }
    });
};

function tinyMCEcomm(x){
var sel = $(x).attr('id');
tinymce.init({
	selector:'#'+sel,
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize table"
    ],
	skin:'gradp',
	height:200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link emoticons table",
menubar: false, statusbar: false

});
$(x).siblings('.hiding').show();
setTimeout(function(){
tinymce.activeEditor.on('blur',function(){
	var val2 = tinymce.activeEditor.getContent();
if (val2==''){
tinymce.activeEditor.remove();
$(x).siblings('.hiding').hide();
}
});

tinymce.activeEditor.on('keyup', function(e){
var prev = 0;
var $tagelem = $(x).siblings('.tagElement');
var $combox = $(x).parents('.commentBox');
prev =  $(tinymce.activeEditor.getBody()).data('code');
 $(tinymce.activeEditor.getBody()).data('code',e.keyCode);
if( typeof $(tinymce.activeEditor.getBody()).data('flag') == 'undefined' || $(tinymce.activeEditor.getBody()).data('flag') == false){
if (e.keyCode == 50){
if(prev == 32 || typeof prev == 'undefined' || prev == 16){
	var val = tinymce.activeEditor.getContent();
	var tags = getTags(val);
	if (tags != []){$tagelem.val(tags.join(' ' ));}else{$tagelem.val('');}
	$(tinymce.activeEditor.getBody()).data('flag',true);
	 }}
}
else{
	var str = $(tinymce.activeEditor.getBody()).text();
	if(str.indexOf('@') != -1){
	$(tinymce.activeEditor.getBody()).bind('keyup',function(){
	 var searchval = new String(str.match(/\w*$/));
	 $.trim(searchval);
	 if(searchval != ''){
	 var tagexist = $tagelem.val();
	 $.get('/search/autocomplete/tag/',{'content': searchval,'tagexist':tagexist},function(data){
	 if ($combox.find('.tagUser').length==0){$combox.find('.btn-group').before('<div class="tagUser"></div>');}
	
	 $combox.find('.tagUser').html(data);
	 });
	 }
	 });
	 }else{
	 $(tinymce.activeEditor.getBody()).unbind('keyup');
	 $(tinymce.activeEditor.getBody()).data('flag',false);
	 if ($combox.find('.tagUser').length>0){$combox.find('.tagUser').remove();}
	 }
	 }
});
},1000);
return false;
}
function tinyMCEinit(t){
tinymce.init({
    selector: ".postArea textarea",
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize"
    ],
	skin:'gradp',
    height:200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link emoticons",
menubar: false, statusbar: false

});
setTimeout(function(){
tinymce.activeEditor.on('keyup paste', function(){
if($('#postForm .liveContainer').find('.urlive-link').length > 0){
			 
			 }else{
			
$(tinymce.activeEditor.getBody()).urlive({container: '.liveContainer', imageSize: 'small', callbacks: {
            onStart: function () {
				
                $('.loading').show();
                $('.liveContainer').empty();
				},
            onSuccess: function (data) {
				
                $('.loading').hide();
				$('.postPanel .glyphicon-remove').show();
				},
			onFail: function(){$('.loading').hide(); },
            noData: function () {
                $('.loading').hide();
				}
        }});}

});
tinymce.activeEditor.on('keyup', function(e){
var prev = 0;
prev =  $(tinymce.activeEditor.getBody()).data('code');
 $(tinymce.activeEditor.getBody()).data('code',e.keyCode);
if( typeof $(tinymce.activeEditor.getBody()).data('flag') == 'undefined' || $(tinymce.activeEditor.getBody()).data('flag') == false){
if (e.keyCode == 50){
    console.log("@pressed", prev);
if(prev == 32 || typeof prev == 'undefined' || prev == 16){
	var val = tinymce.activeEditor.getContent();
    
	var tags = getTags(val);
	if (tags != []){$('#tagHidden').val(tags.join(' ' ));}else{$('#tagHidden').val('');}
	$(tinymce.activeEditor.getBody()).data('flag',true);
	 }}
}
else{
	var str = $(tinymce.activeEditor.getBody()).text();
	if(str.indexOf('@') != -1){
	$(tinymce.activeEditor.getBody()).bind('keyup',function(){
	 var searchval = new String(str.match(/\w*$/));
	 $.trim(searchval);
	 if(searchval != ''){
	 var tagexist = $('#tagHidden').val();
	 $.get('/search/autocomplete/tag/',{'content': searchval,'tagexist':tagexist},function(data){
         if (!t){
	 if ($('#postForm .postPanel').find('#tagUser').length == 0){ $('#postForm .postPanel').append('<div id="tagUser"></div>');}
     $('#tagUser').html(data);}else{
      if ($('#postThreadForm .postPanel').find('#tagUser').length == 0){ $('#postThreadForm .postPanel').append('<div id="tagUser"></div>'); }
         $('#tagUser').html(data);
     }
	 });
	 }
	 });
	 }else{
	 $(tinymce.activeEditor.getBody()).unbind('keyup');
	 $(tinymce.activeEditor.getBody()).data('flag',false);
	 if ($('#tagUser').length>0){ $('#tagUser').remove();}
	 }
	 }
});
},900);

}
function getTags(val){
$('body').append('<div id="tagList"></div>');
$('#tagList').html(val);
var tags =[];
$('#tagList').find('a').each(function(i){
tags.push($(this).text());
});
$('#tagList').remove();
return tags;
}
function share(x){

tinymce.init({
    selector: "#shareText",
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize"
    ],
	skin:'gradp',
    height:200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link image emoticons ",
menubar: false, statusbar: false

});
setTimeout(function(){

tinymce.activeEditor.on('keyup', function(e){
var prev = 0;
prev =  $(tinymce.activeEditor.getBody()).data('code');
 $(tinymce.activeEditor.getBody()).data('code',e.keyCode);
if( typeof $(tinymce.activeEditor.getBody()).data('flag') == 'undefined' || $(tinymce.activeEditor.getBody()).data('flag') == false){
if (e.keyCode == 50){
if(prev == 32 || typeof prev == 'undefined' || prev == 16){
	var val = tinymce.activeEditor.getContent();
	var tags = getTags(val);
	if (tags != []){$('#tagHidden').val(tags.join(' ' ));}else{$('#tagHidden').val('');}
	$(tinymce.activeEditor.getBody()).data('flag',true);
	 }}
}
else{
	var str = $(tinymce.activeEditor.getBody()).text();
	if(str.indexOf('@') != -1){
	$(tinymce.activeEditor.getBody()).bind('keyup',function(){
	 var searchval = new String(str.match(/\w*$/));
	 $.trim(searchval);
	 if(searchval != ''){
	 var tagexist = $('#tagHidden').val();
	 $.get('/search/autocomplete/tag/',{'content': searchval,'tagexist':tagexist},function(data){
	 $('#postForm .postPanel').append('<div id="tagUser"></div>');
	 $('#tagUser').html(data);
	 });
	 }
	 });
	 }else{
	 $(tinymce.activeEditor.getBody()).unbind('keyup');
	 $(tinymce.activeEditor.getBody()).data('flag',false);
	 if ($('#tagUser').length>0){ $('#tagUser').remove();}
	
	 }
	 }
});
},1000);
var user = $(x).parents('.commentBox').siblings('.newsFeedItem').children('.actorUser').text();
if ($(x).parents('.commentBox').siblings('.newsFeedItem').find('.newsFeedItemText').text() == 'created a thread'){
var context = 'thread'}else{var context = 'post';}
$('#shareModal').find('h4').text("Share "+user+ "'s " +context);
 var postContent = $(x).parents('.commentBox').siblings('.newsFeedItem').clone();
 var checkShare = $(x).parents('.commentBox').siblings('.newsFeedItem').find('.liveContainer2').length;
 postContent.find('.timestampText').remove();
 postContent.find('a.hiding').remove();
 if (context == 'thread'){var threaddesc = $(x).parents('.commentBox').find('.feedText').clone();
 postContent = postContent.append(threaddesc);
 }
 var postContent2 = postContent.find('.liveContainer2').clone();
 if (checkShare>0){

 $('#shareModal').find('.liveContainer2').html(postContent2.html());}else{
 $('#shareModal').find('.liveContainer2').html(postContent.html());}
 
}
function remove_uploaded(x,y,z){
if(y){ 
var filename = $(x).siblings('.qq-upload-file').text();
    var id_file = filename.toString() + 'jPeFhhi';
var hashed_file = document.getElementById(id_file).value;
    $('#'+id_file).remove();
$.post('/upload/delete/original/',{'filename':hashed_file},function(data){
var str = $('#img_url').val();
var path = hashed_file;
$.trim(str);
var arr = str.split(' ');
var index = arr.indexOf(path);
if (index != -1){
arr.splice(index,1);
$('#img_url').val(arr.join(' '));
    if($('.uploadedFilePanel').children('div').length==1)
{   var token = $('#tokenMiddle').val();
    $('.uploadedFilePanel').hide();
    var uploader = new qq.FileUploader({
            action: "/upload/image/",
			allowedExtensions: ['png','jpeg','jpg','gif','ico','bmp'],
            element: $('#file-uploader')[0],
			listElement: $('.uploadedFilePanel')[0],
            multiple: true,
            onComplete: function( id, fileName, responseJSON ) {
              if( responseJSON.success )
              {
			  }else{}},
            onAllComplete: function( uploads ) {
            $('#img_url').val('');
			  for(i=0;i<uploads.length;i++){
			  $('#img_url').val($('#img_url').val() + ' ' + uploads[i]['response']['path']);
			  }

			  },
            params: {
              'csrf_token': token,
              'csrf_name': 'csrfmiddlewaretoken',
              'csrf_xname': 'X-CSRFToken',
            },
          }) ;                                             
                                                 
}
}else{}
$(x).parents('.qq-upload-success').fadeOut().remove();

return false;
});
}else{
   if(z=="false"){
var filename = $(x).siblings('.uploadedFileUrl').val();
$.post('/upload/delete/original/mugshot/',{'filename':filename},function(data){
$(x).parents('.qq-upload-success').fadeOut().remove();
if($('.uploadedFilePanel2').find('div').length==0){$('.uploadedFilePanel2').hide();}
$('.qq-upload-button img').attr('src','/static/img/upload.png');
return false;
});
   }else{
       var filename = $(x).siblings('.uploadedFileUrl').val();
   $.post('/upload/delete/blog/',{'filename':filename},function(data){
$(x).parents('.uploadedFilePanel2').fadeOut().empty();
if($('.uploadedFilePanel2').find('div').length==0){$('.uploadedFilePanel2').hide();}
$('.blogCover').css('height','100px');
return false;
});
   
   }
}
}
function get_image(x){
var url = $(x).find('img').attr('src');
var actor = $(x).parents('.newsFeedItem').find('.actorUser').first().text();

$('#imageModal').find('img').attr('src',url);
$('#imageModal').find('h4').text(actor+"'s post");
}
function editProfile(){
window.location = '/myprofile/edit/'; 
}
function changePass(x){window.location='/accounts/'+x+'/password/'}
function changeMail(x){window.location='/accounts/'+x+'/email/'}
function actch(e){e.preventDefault();e.stopPropagation();$('#inActiveModal').modal('show');}
function logch(e){e.preventDefault();e.stopPropagation();$('#loginModal').modal('show');
                 if ($('.followingThread').length > 0){
                 $('.followingThread').each(function(){ 
                     $(this).off('click');
                 });
                 }
                 }
function getThreadFeed(){
				
				 var is_active = $('#actch123').val(); 
				 var is_logged = $('#logch123').val();
				 
				 if (is_logged == 'True'){
				 if(is_active == 'False'){$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;$('#inActiveModal').modal('show');});
				 }
				 }else{$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;e.stopPropagation();$('#loginModal').modal('show');});
				 }
				
                 $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({
    html:true,placement:'bottom'}); }
function anonReg(){$('.registrationWrapper').fadeIn();return false;}

function profileFeed(){	
var username = $('#profile_username').val();	
var requestuser = $('#user_username').val();	
if(username == requestuser){
				
                     $('a.deleteLink').popover({html:true,placement:'bottom'});
                   $('a.deleteCommentLink').popover({
    html:true,placement:'bottom'});
				}
		
		
		else{
		if ($('#followBtn').is(":visible")){
				
				$('.glyphicon-remove').remove();
		
		}
		}}
function followingthreadlist(){
$('#followThreadList .panel-body').find('img').each(function(i){
var url = $(this).attr('src');
url = url.substring(2);
$(this).attr('src',url);
});
}
function fetch_user_list(){
	$.get('/messages/user_list/{{object.pk}}/',function(data){$('#userListConv .modal-body').html(data);});
	}
function formSubmitConv(){
var data = $('messageForm2').find('input').map(function(){return $(this).val()}).get();
    var url = $('messageForm2').attr('action');
$.post(url,{'csrfmiddlewaretoken':data[0],'text':$('#msgText').val()},function(data){
$.post('/messages/latest/new/',{'pk':data['id']},function(data){$('#messageBox>div').append(data);
                                                                var diff = $('#messageBox>div').height()-$('#messageBox').height();
                                                               
                                                               $('#msgText').val('');$('#messageBox').scrollTop(diff);
                                                               });
});
}
function tinyMCEblog(){
 tinymce.init({
    selector: "#blogText",
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize"
    ],
	skin:'gradp',
     height:200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link image emoticons",
menubar: false, statusbar: false
});
}
function isblog(x){
if (x){
$('.blogCover').find('img').remove();
$('.blogCover').append('<span class="largeFont">Upload a cover pic</span>');
}
}

function tinyMCEblogcomm(){
    var x = '#id_blog_comment';
tinymce.init({
	selector:'#id_blog_comment',
    plugins: [
        "autolink lists link charmap emoticons",
		"autoresize table"
    ],
	skin:'gradp',
	height:200,
    toolbar: "bold italic underline | superscript subscript charmap | bullist numlist alignjustify alignright alignleft | link emoticons table",
menubar: false, statusbar: false

});
$(x).siblings('.hiding').show();
setTimeout(function(){
tinymce.activeEditor.on('blur',function(){
	var val2 = tinymce.activeEditor.getContent();
if (val2==''){
tinymce.activeEditor.remove();
$(x).siblings('.hiding').hide();
}
});

tinymce.activeEditor.on('keyup', function(e){
var prev = 0;
var $tagelem = $(x).siblings('.tagElement');
var $combox = $(x).parents('.commentBox');
prev =  $(tinymce.activeEditor.getBody()).data('code');
 $(tinymce.activeEditor.getBody()).data('code',e.keyCode);
if( typeof $(tinymce.activeEditor.getBody()).data('flag') == 'undefined' || $(tinymce.activeEditor.getBody()).data('flag') == false){
if (e.keyCode == 50){
if(prev == 32 || typeof prev == 'undefined' || prev == 16){
	var val = tinymce.activeEditor.getContent();
	var tags = getTags(val);
	if (tags != []){$tagelem.val(tags.join(' ' ));}else{$tagelem.val('');}
	$(tinymce.activeEditor.getBody()).data('flag',true);
	 }}
}
else{
	var str = $(tinymce.activeEditor.getBody()).text();
	if(str.indexOf('@') != -1){
	$(tinymce.activeEditor.getBody()).bind('keyup',function(){
	 var searchval = new String(str.match(/\w*$/));
	 $.trim(searchval);
	 if(searchval != ''){
	 var tagexist = $tagelem.val();
	 $.get('/search/autocomplete/tag/',{'content': searchval,'tagexist':tagexist},function(data){
	 if ($combox.find('.tagBlogUser').length==0){$combox.find('.btn-group').before('<div class="tagBlogUser"></div>');}
	 
	 $combox.find('.tagBlogUser').html(data);
	 });
	 }
	 });
	 }else{
	 $(tinymce.activeEditor.getBody()).unbind('keyup');
	 $(tinymce.activeEditor.getBody()).data('flag',false);
	 if ($combox.find('.tagUser').length>0){$combox.find('.tagUser').remove();}
	 }
	 }
});
},1000);
return false;
}
function setEditBlog(y){
var content = $('.clone').text();

    if($('.uploadedFileUrl').val() == ''){ $('.blogCover').css('height','100px');}else{
    $('.blogCover').css('height','auto');}
setTimeout(function(){
    var ed = tinymce.EditorManager.get('blogText');
    ed.setContent(content);},1000);
    $('select').val(y);$('.clone').remove();
}

function delete_post(x,y){
 $.post('/delete/post/',{'id':x},function(){
                $(y).parents('.newsFeedWrapper').fadeOut();
      setTimeout("$(y).parents('.newsFeedWrapper').remove()",500);
                });
    return false;
}
function delete_comment(x,y){
 $.post('/delete/comment/',{'id':x},function(){
                $(y).parents('.commentList').fadeOut();
      setTimeout("$(y).parents('.commentList').remove()",500);
                });
    return false;
}
function delete_blog(x,y){
 $.post('/delete/blog/',{'id':x},function(){
                $(y).parents('.blogItemWrapper').fadeOut();
      setTimeout("$(y).parents('.blogItemWrapper').remove()",500);
        window.location = '/blogs/all/published/';               
 });
    return false;
}
function delete_conv(x,y){
 $.post('/messages/'+x+'/archive/',function(){
                $(y).parents('.panel-body').fadeOut();
      setTimeout("$(y).parents('.panel-body').remove()",500);            
 });
    return false;
}
function resend_activate_mail(x){
$.post('/resend/activate/mail/'+x+'/',function(d){
if (d['success'] == 'true'){
$('#inActiveModal').find('.alert').text('An activation mail has been sent to your mail. Please follow steps in the mail to activate your account.');
$('#inActiveModal').find('.alert').removeClass('alert-danger').addClass('alert-success');
}else{
$('#inActiveModal').find('.alert').text('Mail could not be sent. Please try again after some time.');
}}
);
}
function report_comment(x,y){
$('#reportModal').modal('show');
$('#reportModal').find('.btn-primary').attr('id',x);
    $('a.deleteCommentLink').popover('hide');
    $('a.reportCommentLink').popover('hide');
}
function report_post(x,y){
$('#reportPostModal').modal('show');
$('#reportPostModal').find('.btn-primary').attr('id',x);
    $('a.deleteLink').popover('hide');
}
function reportComment(x){
var id = $(x).attr('id');
var typeArr = $(x).parents('.input-group').find('input[type=checkbox]');
var categoryArr = new Array();
for (i=0;i<typeArr.length;i++){
if ($(typeArr[i]).prop('checked')){
categoryArr.push($(typeArr[i]).val());}
}
var category = categoryArr.join(' ');
$.post('/moderate/report/comment/',{'id':id,'category':category}, function(d){
if (d['success']=='true'){
$('#reportModal').modal('hide');
$('#reportModalSuccess').modal('show');
}else if (d['success']=='duplicate')
{
$('#reportModal').modal('hide');
$('#reportModalSuccess').modal('show');
$('#reportModalSuccess').find('.alert').removeClass('alert-success').addClass('alert-danger').text('You have already reported this content. Moderators are reviewing this content.');
}
});
}
function reportPost(x){
var id = $(x).attr('id');
var typeArr = $(x).parents('.input-group').find('input[type=checkbox]');
var categoryArr = new Array();
for (i=0;i<typeArr.length;i++){
if ($(typeArr[i]).prop('checked')){
categoryArr.push($(typeArr[i]).val());}
}
var category = categoryArr.join(' ');
$(x).attr('disabled',true);
$(x).text('Reporting...');
$.post('/moderate/report/post/',{'id':id,'category':category}, function(d){
$(x).text('Report it');
$('#reportPostModal').modal('hide');
$('#reportPostModalSuccess').modal('show');

});
}
function new_thread(){
  $('#checkThreadModal').modal('hide');
                                $('#createThreadModal').modal('show');
                                 var title = $('#threadTitleSearch').val();
                                 $('#threadTitle').val(title);
}
function backonthread(){
$('#checkThreadModal .modal-body').html('<p><b>Title of the Thread:</b></p>'+
				'<div class="clearfix"></div>'+
				'<textarea type="text" class="form-control marginT noResize" placeholder="Give a title to your thread..." name="q" id="searchThread"></textarea>'+
				'<div class="postPanel row clearfix"><div class="btn-group btn-group-sm floatR">'+
				'<button id="checkThreadSubmit" onclick="seach_existing_t();" class="btn btn-primary"><b>Next</b></button></div></div>');
$('#checkThreadModal h4').text('Create a discussion thread');  
}
function seach_existing_t(){
var query = $('#searchThread').val();
var regexp = /^[ A-Za-z0-9_.:,\[\]\(\)]*$/;
if (query != '' && query.length > 9 && regexp.test(query)){

$.get('/threads/search/',{'q':query},function(d){
    $('#checkThreadModal h4').text('Existing similar discussion threads');
    $('#checkThreadModal .modal-body').html(d);
    if ($('#resultCountThread').val() == '0'){new_thread();}
$('.threadSearchResult').highlight(query);});
}else if(!regexp.test(query)){$('#searchThread').attr('title','Only alphanumerics, underscores, square brackets, parentheses, colons, comma and dots allowed..');
                        $('#searchThread').tooltip('show');
                        setTimeout('$("#searchThread").tooltip("destroy")',5000);
}
else{
      $('#searchThread').attr('title','Please enter the thread title (more than 10 chars long)');
      $('#searchThread').tooltip('show');
        setTimeout('$("#searchThread").tooltip("destroy")',3000);}}
function fresh_create_thread(){
$('#createThreadModal').modal('hide');
$('#checkThreadModal').modal('show');
backonthread();
}
function registerModalShow(){
$('#loginModal').modal('hide');
$('#registerModal').modal('show');
}
function blog_details_init(){
 var is_active = $('#actch123').val(); 
				 if(is_active == 'False'){$('.phileo a.btn-default').each(function(){$(this).attr('href','#');});
				 $('.phileo a.btn-default').click(function(e){e.preventDefault;e.stopPropagation();$('#inActiveModal').modal('show');});
				 }
$('.phileo .glyphicon-share-alt').each(function(){$(this).parent().remove();});
}

function registerSection(){
$('.loginSection').hide();
$('.registrationSection').fadeIn();
}

function loginSection(){
$('.registrationSection').hide();
$('.loginSection').fadeIn();
}
/************************************cookie functions to view recent activity *****************************************/

function checkHistory(targetId) {
    var username = $('#id_unique_identity').val();
    var history = $.cookie('historyhog'+username);
    var htmlContent = '';
    
    if (history != "" && typeof history != 'undefined' ) {
        var insert = true;
        var sp = history.toString().split(",");
        for ( var i = sp.length - 1; i >= 0; i=i-2) {
            htmlContent += '<a class="list-group-item colorBlue"  href="'
                    + sp[i-1]
                    + '">'
                    + sp[i] + '</a>';
            if (sp[i-1] == document.URL) {
                insert = false;
            }
            document.getElementById(targetId).innerHTML = htmlContent;
        }
        if (insert && document.URL.indexOf('threads')!=-1 && document.URL.indexOf('following')==-1) {
            sp.push(document.URL, document.title);
        }
        $.cookie("historyhog"+username, sp.toString(), {expires:365, path:'/'});
    } else {
        var stack = new Array();
        if (document.URL.indexOf('threads')!=-1 && document.URL.indexOf('following')==-1){
        stack.push(document.URL, document.title);}
        $.cookie("historyhog"+username, stack.toString(), {expires:365, path:'/'});
    }
    var lencheck = $.cookie('historyhog'+username).toString().split(",");
    if (lencheck.length >12 ){lencheck.splice(0,2);
                              $.cookie("historyhog"+username, lencheck.toString(), {expires:365, path:'/'});
                             }
}
function clearHistory(targetId) {
    $.removeCookie("historyhog"+username,{expires:365,path:'/'});
    document.getElementById(targetId).innerHTML = "";
}
function update_stream_social()
{
var stream = $('#profileStreamSelectSocial').val();
if (stream !=''){
    var flag = $('#flagVal').val();
$.post('',{'stream':stream},function(data){
if (data['success'] == 'true'){
if (flag!=''){download_init(stream);}
}
});
$.get('/fb/registration/feed/',{'stream':stream}, function(data){
$('#feedBuildSocial').html(data);
    $('.feedFollow').click(function(){
$curr = $(this);
var objname = $(this).attr('id');
$.post('/follow/followobj/',{'objname':objname,'thread':'False'},function(data){$curr.attr('disabled',true);$curr.text('Following');
$curr.parents('.followPanel').addClass('disabledFollow');
});
});
    $('.feedThreadFollow').click(function(){
$curr = $(this);
var objname = $(this).attr('id');
$.post('/follow/followobj/',{'objname':objname,'thread':'True'},function(data){$curr.attr('disabled',true);$curr.text('Following');
});
});
    $('#configFeed').click(function(e){
var len = $('.disabledFollow').length;

if(len<3){$('.usertip').attr('title','Please follow at least 3 users to build your feed');
$('.usertip').tooltip('show');
$('body').scrollTop(0);
return false;}
window.location = '/home/';
}); 
});}else{$('#profileStreamSelectSocial').attr('title','Please select your GATE stream');$('#profileStreamSelectSocial').tooltip();
        setTimeout(function(){$('#profileStreamSelectSocial').tooltip('destroy');},3000);
        }
}
function follow_people(userid,x){
if ($.trim($(x).text()) == 'Follow'){
$.post('/follow/followobj/',{'objname':userid,'thread':'False'},function(data){$(x).text('Unfollow');$(x).removeClass('btn-success'); $(x).addClass('btn-default');
});
}else if ($.trim($(x).text()) == 'Unfollow'){
 $.post('/follow/unfollowobj/',{'objname':userid,'thread':'False'},function(data){$(x).text('Follow');$(x).removeClass('btn-default'); $(x).addClass('btn-success');   
});
}
}
function download_init(stream){
if (stream == 'EC'){
    $("#submitProfile").text("Downloading...");
window.location='/register/download?stream='+stream;
}else{ 
alert("We are still making guide for"+stream+". We will soon mail you the link to download.");
}
}
function download_register(url,slug){
$("#submitProfile").text("Finishing registration...");
if (typeof url == 'undefined' || url == ''){
                                     window.location='/feed/build/'+slug+'/'+$('#profileStreamSelect').val()+'/';}else{
                                  $.post('/mugshot/select/',{'url':url},function(data){
                                      
                              window.location='/feed/build/'+slug+'/'+$('#profileStreamSelect').val()+'/';});
							}
}