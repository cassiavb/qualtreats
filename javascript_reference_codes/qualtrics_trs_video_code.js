Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
	const Video = jQuery("#video")
	const PlayButton = jQuery("#play_button");
	var textBox = jQuery('input[type="text"]');
	var that = this;
	that.disableNextButton();
	
	Video.css("pointerEvents","none");
	
	PlayButton.click(() => {
		if (Video[0].ended) return;
		Video[0].play();
	});
	
	
	let onVideoEnded = () => {

  			PlayButton.html("Video ended");
		    PlayButton[0].disabled = true;
	};
	Video[0].on("ended", onVideoEnded);
	
	let onTextChanged = () => {
		if (textBox.eq(0).val().match(/\S/)){	
			that.enableNextButton();
			}
	};

	textBox.on('input',onTextChanged);

});

Qualtrics.SurveyEngine.addOnReady(function()
{
/*Place your JavaScript here to run when the page is fully displayed*/

});

Qualtrics.SurveyEngine.addOnUnload(function()
{
  /*Place your JavaScript here to run when the page is unloaded*/

});