function usernameChecker(username){
	if (username.length < 1) {
        $('#username').after('<div class="error">This field is required</div>');
        return false;
    }
	if (username.length > 25) {
        $('#username').after('<div class="error">Length should be less than 25</div>');
        return false;
    }

	var regEx = /^[a-zA-Z0-9._]+$/;
    var valid = regEx.test(username);
    if (!valid) {
        $('#username').after('<div class="error">Username can contain only _ and .</div>');
        return false;
    }
	
    return true;
}

function passwordChecker(password){
	if(password.length < 8){
		$('#password').after('<div class="error">Length should be greater than 8</div>');
		return false;
	}
	if (password.length > 15){
		$('#password').after('<div class="error">Length should be smaller than 15</div>');
		return false;
	}

	var regEx  = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{7,15}$/;
	var valid = regEx.test(password);
	if(!valid){
		$('#password').after('<div class="error">Password should combination of symbol, letters, numbers</div>');
		return false;
	}

	return true;
}

function passwordMatch(password, repassword){
	if (password.length < 1){
      	$('#repassword').after('<div class="error">This field is required</div>');
		return false;
	}
	if (password != repassword){
		$('#repassword').after('<div class="error">Password does not match.</div>');
		return false;
	}

	return true;
}

function emailChecker(email){
	if(email.length < 1){ 
      	$('#email').after('<div class="error">This field is required</div>');
		return false;
	}

	var regEx = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;  
    var valid = regEx.test(email);
	if(!valid){
        $('#email').after('<div class="error">Enter a valid email</div>');
		return false;
    }

	return true;
}
// ##############################################################################################################################
function loginFormValidation() {
	$(".error").remove();
	let username = $.trim($('#username').val());
	let password = $.trim($('#password').val());

	var usernameobj = usernameChecker(username);
	var passobj = passwordChecker(password);

	$('#username').css("border-color", !usernameobj ? "red" : "black");
    $('#password').css("border-color", !passobj ? "red" : "black");

	return usernameobj && passobj;
}

function signupFormValidation(){
	$(".error").remove();
	let username = $.trim($('#username').val());
	let email = $.trim($('#email').val());
	let password = $.trim($('#password').val());

	var usernameobj = usernameChecker(username);
	var emailobj = emailChecker(email);
	var passobj = passwordChecker(password);

	$('#username').css("border-color", !usernameobj ? "red" : "black");
    $('#email').css("border-color", !emailobj ? "red" : "black");
	$('#password').css("border-color", !passobj ? "red" : "black");

	return usernameobj && emailobj && passobj;
}

function forgetPassword(){
	$(".error").remove();
	let email = $.trim($('#email').val());

	var emailobj = emailChecker(email);
	$('#email').css("border-color", !emailobj ? "red" : "black");

	return emailobj;
}

function resetPasswordValidation(){
	$(".error").remove();
	let password = $.trim($('#password').val());
	let repassword = $.trim($('#repassword').val());

	var passobj = passwordChecker(password);
	var repassobj = passwordMatch(password, repassword);

	$('#password').css("border-color", !passobj ? "red" : "black");
	$('#repassword').css("border-color", !repassobj ? "red" : "black");

	return passobj && repassobj;
}