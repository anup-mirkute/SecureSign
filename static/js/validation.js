function usernameChecker(username, flag=true){
	if (username.length < 1){
		flag = false;
		$('#username').after('<div class="error">This field is required</div>');
	}
	else if (username.length > 25){
		flag = false;
		$('#username').after('<div class="error">Length should be less than 25</div>');
	}
	else {
		var regEx = /^[a-zA-Z0-9._]+$/;
		var valid = regEx.test(username);
		if (!valid){
			flag = false;
			$('#username').after('<div class="error">Username can contain only . and _</div>');
		}
	}

	if(!flag){
		$('#username').css("border-color", "red");
	}
	else{
		$('#username').css("border-color", "black");
	}
	return flag;
}

function passwordChecker(password, flag=true){
	if(password.length < 8){
		flag = false;
		$('#password').after('<div class="error">Length should be greater than 8</div>');
	}
	else if (password.length > 15){
		flag = false;
		$('#password').after('<div class="error">Length should be smaller than 15</div>');
	}
	else{
		var regEx  = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{7,15}$/;
		var valid = regEx.test(password);
		if(!valid){
			flag = false;
			$('#password').after('<div class="error">Password should combination of symbol, letters, numbers</div>');
		}
	}
	if(!flag){
		$('#password').css("border-color", "red");
	}
	else{
		$('#password').css("border-color", "black");
	}
	return flag;
}

function passwordMatch(password, repassword, flag=true){
	if (password.length < 1){
		flag = false;
      	$('#repassword').after('<div class="error">This field is required</div>');
	}
	else if (password != repassword){
		flag = false;	
		$('#repassword').after('<div class="error">Password does not match.</div>');
	}
	else{

	}

	if(!flag){
		$('#repassword').css("border-color", "red");
	}
	else{
		$('#repassword').css("border-color", "black");
	}
	return flag;
}

function emailChecker(email, flag=true){
	if(email.length < 1){ 
		flag = false;
      	$('#email').after('<div class="error">This field is required</div>');
	}
	else {
		var regEx = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;  
    	var valid = regEx.test(email);
		if(!valid){
    		flag = false;  
        	$('#email').after('<div class="error">Enter a valid email</div>');
    	}
	}

	if(!flag){
		$('#email').css("border-color", "red");
	}
	else{
		$('#email').css("border-color", "black");
	}
	return flag;
}
// ##############################################################################################################################
function loginFormValidation() {
	$(".error").remove();
	let username = $.trim($('#username').val());
	let password = $.trim($('#password').val());
	var flag = true;

	var usernameobj = usernameChecker(username);
	var passobj = passwordChecker(password);

	if(usernameobj == true && passobj == true){
		flag = true;
	}
	else{
		flag = false;
	}
	return flag;
}

function signupFormValidation(){
	$(".error").remove();
	let username = $.trim($('#username').val());
	let email = $.trim($('#email').val());
	let password = $.trim($('#password').val());

	var usernameobj = usernameChecker(username);
	var emailobj = emailChecker(email);
	var passobj = passwordChecker(password);

	if(usernameobj == true && emailobj == true && passobj == true){
		flag = true;
	}
	else{
		flag = false;
	}
	return flag;
}

function forgetPassword(){
	$(".error").remove();
	let email = $.trim($('#email').val());
	var flag = true;

	var emailobj = emailChecker(email);

	if(emailobj == true){
		flag = true
	}
	else{
		flag = false;
	}
	return flag;
}

function resetPasswordValidation(){
	$(".error").remove();
	let password = $.trim($('#password').val());
	let repassword = $.trim($('#repassword').val());

	var passobj = passwordChecker(password);
	var repassobj = passwordMatch(password, repassword);

	if(passobj == true && repassobj == true){
		flag = true;
	}
	else{
		flag = false;
	}
	return flag;
}

