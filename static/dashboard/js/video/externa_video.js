

var videoEreaStatic = false;
var videoEditArea = $('#video-edit-area');

$('#open-add-video-btn').click(function(){
  if (!videoEreaStatic) {
    videoEditArea.show();
    videoEreaStatic = true;
  } else {
    videoEditArea.hide();
    videoEreaStatic = false;
  }
});


$('#close_form').click(function(){
  if (!videoEreaStatic) {
    videoEditArea.show();
    videoEreaStatic = true;
  } else {
  $('#open-add-video-btn').text('创建')
    videoEditArea.hide();
    videoEreaStatic = false;
  }
});




var InputName = $('#name')
var InputImage = $('#image')
var SeceltType = $('.video_type')
var NationalityType = $('.nationality')
var Video_info = $('#info')
$('.update-video-btn').click(function(){
    if (!videoEreaStatic) {
    videoEditArea.show();
    videoEreaStatic = true;
    $('#open-add-video-btn').text('编辑')
  }


    var video_name= $(this).attr('name')
    var video_img= $(this).attr('video_img')
    var video_type = $(this).attr('video_type')
    var nationality_type = $(this).attr('nationality')
    var video_info = $(this).attr('info')
    InputName.val(video_name)
    InputImage.val(video_img)
    SeceltType.val(video_type)
    NationalityType.val(nationality_type)
    Video_info.val(video_info)
})
