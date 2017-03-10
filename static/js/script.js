$(function(){
	
	$("#getpatients").click(function(){
		     $.ajax({url: "/getpatients", success: function(result){
				$("#div1").html(result);
				 $(document).find('#example').DataTable();
			}});
	});
	  var current = 1,current_step,next_step,steps;
	  steps = $("fieldset").length;
	 /* $(".next").click(function(){
		current_step = $(this).parent();
		next_step = $(this).parent().next();
		next_step.show();
		current_step.hide();
		setProgressBar(++current);
	  });*/
	  $(".previous").click(function(){
		current_step = $(this).parent();
		next_step = $(this).parent().prev();
		next_step.show();
		current_step.hide();
		setProgressBar(--current);
	  });
	  setProgressBar(current);
	  // Change progress bar action
	  function setProgressBar(curStep){
		var percent = parseFloat(100 / steps) * curStep;
		percent = percent.toFixed();
		$(".progress-bar")
		  .css("width",percent+"%")
		  .html(percent+"%");   
	  }
	var patientid = '';
	$("#step1_next").on('click',function(){
		current_step = $(this).parent();
		next_step = $(this).parent().next();
		var fname = $("#fname").val();
		var lname = $("#lname").val();
		var dob = $("#dob").val();
		if(fname == '' || lname == '' || dob == '')
		{
			alert("Please Enter all fields!");
		}
		else{
			$.ajax({url:'/getpatient',
					method:'get',
					data:{'fname':fname,'lname':lname,'dob':dob},
					success:function(resp){
						var resp = resp['results'][0];
                         patientid = resp['id'];
                         var address = resp['address']
                         var cellphone = resp['cell_phone']
                         var email = resp['email']
                         var ssn = resp['social_security_number']
                         var zipcode = resp['zipcode']

						
						next_step.show();
						current_step.hide();
						setProgressBar(++current);
						
						setpatientData(patientid);
						
					}
				   });
		}
	});
	function setpatientData(pid){
		$.ajax({url:'/getappointment',
					method:'get',
					data:{'pid':pid},
					success:function(resp){
					}
			   });
		
	}
});