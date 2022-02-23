
$(document).ready(function() {
  $('.field_file').change(function() {
    if (this.files[0])
      $('.field_file-fake').text(this.files[0].name);
  });
});



