Qualtrics.SurveyEngine.addOnload(function() {
	const TextLabel = jQuery("div#question_text_container1");
	const FirstAnswer = jQuery("#"+this.questionId+" input[choiceid=1]").closest("li").hide();
	const SecondAnswer = jQuery("#"+this.questionId+" input[choiceid=2]").closest("li").hide();
	const ThirdAnswer = jQuery("#"+this.questionId+" input[choiceid=3]").closest("li").hide();
	const FourthAnswer = jQuery("#"+this.questionId+" input[choiceid=4]").closest("li").hide();
	const FifthAnswer = jQuery("#"+this.questionId+" input[choiceid=5]").closest("li").hide();
	var that = this;
	that.disableNextButton();

	FirstAnswer.hide();
	SecondAnswer.hide()
	ThirdAnswer.hide();
	FourthAnswer.hide();
	FifthAnswer.hide();
	TextLabel.hide();
	
	const Video = jQuery("#video")
	const PlayButton = jQuery("#play_button");


	Video.css("pointerEvents","none");
	PlayButton.click(() => {
		if (Video[0].ended) return;
		Video[0].play();
	});

	let onVideoEnded = () => {
		TextLabel.show();
		FirstAnswer.show();
		SecondAnswer.show()
		ThirdAnswer.show();
		FourthAnswer.show();
		FifthAnswer.show();

		PlayButton.html("Video file ended");
	    PlayButton[0].disabled = true;
    };
		
	Video[0].on("ended", onVideoEnded);
	jQuery('ul li:eq(0), ul li:eq(1), ul li:eq(2), ul li:eq(3), ul li:eq(4)').find('input[type="radio"]').change(function(){
	that.enableNextButton();});

});

Qualtrics.SurveyEngine.addOnReady(function() {});


Qualtrics.SurveyEngine.addOnUnload(function() {});