$(function(){
	$('.submit-form').click(function(e){
		e.preventDefault();
		var pass = 0;
		var name = $('input[name=name]').val();
		var password = $('input[name=password]').val();
		var identify = $('input[name=identify]:checked').val()
		var check_name =checkname(name)
		var check_password = checkpassword(password)
		var check_identify = checkidentify(identify)
		check(name,password,identify,function(check_web){
			pass = check_name&&check_password&&check_identify&&check_web? true:false;
			if(!pass){
				$('.error-item').html("用户名或密码错误");
				return;
			}else{
				$('.error-item').html(" ");
			}	
			console.log('准备登陆')
			$('.login-form').submit();	
		})
	});
	function checkname(name){
		// 5~16位_a-zA-Z0-9
		_re = new RegExp('^[_a-zA-Z0-9]{5,16}$')
		console.log( '账号检测',_re.test(name))
		return _re.test(name)
	}
	function checkpassword(password){
		_re = new RegExp('^[_a-zA-Z0-9]{5,16}$')
		console.log( '密码检测',_re.test(password))
		return _re.test(password)
	}
	function checkidentify(identify){
		if( Number(identify) == 0 || Number(identify) == 1)
			return true
		console.log('身份检测',false)
		return false
	}
	function check(name,password,identify,cb){
		$.ajax({
			method:'POST',
			data:{
				name:name,
				password:password,
				identify:identify
			},
			url:'/api/checkuser',
			dataType:'json',
			success:function(response){
				if (response.code == '0') check_web =  true;
				cb(check_web);
				return;
				console.log('服务器检测',false)
				check_web=false;
				cb(check_web);
			},fail:function(error){
				if(error){
					console.log(error)
					check_web =false
				}
				cb(check_web);
			}
		})
	}
})