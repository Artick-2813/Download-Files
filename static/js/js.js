//$('body').on('change', '.field', function (e) {
//  var file = e.target.files[0].name;
//  $(this).next('.field_file-wrapper').html(file);
//});

$(document).ready(function() {
  $('.field_file').change(function() {
    if (this.files[0])
      $('.field_file-fake').text(this.files[0].name);
  });
});



