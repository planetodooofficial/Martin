// JavaScript Document

	
  var slidePosition = 0,
  count = $("#contain .slide"),
  numOfSlide = $(".slide").length,
  currentSlide = Math.floor(numOfSlide / 2),
  slideWidth = $(".slide").outerWidth(true);


  var parent = $("#contain");
  var nodesSameClass = document.querySelectorAll('#contain .slide').length;
  console.log(nodesSameClass.length);
console.log(currentSlide + 1);
moveSlide(currentSlide);
$(".slide-" + currentSlide).addClass("active");

$(".slide-container").css("width", numOfSlide * slideWidth);

$(".previous").click(function () {
  $(".slide-" + currentSlide).removeClass("active");
  if (currentSlide - 1 >= 0) {
    currentSlide--;
  } else {
    currentSlide = numOfSlide - 1;
  }
  console.log(currentSlide)
  $(".slide-" + currentSlide).addClass("active");

  var active_slide = $('.slide.active').data('id');

  $('#active-slider').val(active_slide);

  console.log('1234.....')

  moveSlide(currentSlide);
});

$(".next").click(function () {
  $(".slide-" + currentSlide).removeClass("active");
     if (currentSlide + 1 < numOfSlide) {
    currentSlide++;
  } else {
    currentSlide = 0;
  }
  console.log(currentSlide)
  $(".slide-" + currentSlide).addClass("active");

  var active_slide = $('.slide.active').data('id');

  $('#active-slider').val(active_slide);

  console.log('5678.....')

  moveSlide(currentSlide);
});

function moveSlide(slideNumber) {
  var slidePosition = -1 * (slideNumber * slideWidth);
  $(".slide-container").css({
    transform: "translateX(" + slidePosition + "px)"
  });
}

$(document).ready(function(){
  $(".slide-" + currentSlide).addClass("active");
  var active_slide = $(".slide-" + currentSlide).data('id');
  $('#active-slider').val(active_slide);
});



