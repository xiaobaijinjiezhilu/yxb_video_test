var inputNumber = $('#number')
var inputUrl = $('#url')
var videosubID = $('#videosub-input-id')

$('.update-btn').click(function(){
 alter(1)
    var videosubIDs= $(this).attr('data-id')
    var videosubNumber = parseInt($(this).attr('data-number'))
    var viedeoSubUrl = $(this).attr('data-url')
    inputNumber.val(videosubNumber)
    inputUrl.val(viedeoSubUrl)
    videosubID.val(videosubIDs)
})


