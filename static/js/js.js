
$(document).ready(function() {
  $('.field_file').change(function() {
    if (this.files[0])
      $('.field_file-fake').text(this.files[0].name);
  });
});

if ($('.wrapper_link').length){
	 $('.info_from_user').css('display', 'none')
}

else{
	$('.info_from_user').css('display', 'block')
}



