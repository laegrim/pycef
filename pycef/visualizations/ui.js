$(function () {

	var timer = null,
	level = 0,
	max = 110,
	duration = 1000,	
	
	function plotLevel() {
		if (level <= max) {
			$('#level').slider({value:level});
			$('#level-val').text(level);	
			level++;
		}	
	}

	$('#level').slider({
		value: level, min:1, max:max, slide: function(e, ui) {
		level = ui.value;
		plotLevel();
		}
	});
	
	$('#play').click(function () {
		if (level > max) level = 1;
		plotLevel();
		if (timer) clearInterval(timer);
		timer = setInterval(function () {
			if (level <= max) plotLevel();
			else $('#stop').click();
			}, duration);
		$(this).hide();
		$('#stop').show();
	}).click();
	
	$('#stop').click(function() {
		if (timer) clearInterval(timer);
		$(this).hide();
		$('#play').show();
	});
});