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
	var address = '';
	 var cellphone = '';
	 var email = '';
	 var ssn = '';
	 var zipcode = '';
	
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
                         address = resp['address']
                         cellphone = resp['cell_phone']
                         email = resp['email']
                         ssn = resp['social_security_number']
                         zipcode = resp['zip_code']
						 $("textarea[name=address]").val(address);
						$("input[name=email]").val(email);
						$("input[name=cellphone]").val(cellphone);
						$("input[name=ssn]").val(ssn);
						$("input[name=zipcode]").val(zipcode);

						
						
						
						setpatientData(patientid);
						
					}
				   });
		}
	});

	$("#step2_next").on('click',function(){
		current_step = $(this).parent();
		next_step = $(this).parent().next();
		var fname = $("#fname").val();
		var lname = $("#lname").val();
		var appointment_id = $("#appointment_id").val();
		var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
		$.ajax({url:'/getappointment',
					method:'post',
					data:{'fname':fname,'lname':lname,'csrfmiddlewaretoken':csrfmiddlewaretoken,'appointment_id': appointment_id,'status': 'Arrived'},
					success:function(resp){
						alert("Check In Successful !!");
						
						next_step.show();
						current_step.hide();
						setProgressBar(++current);


						
					}
				   });
		
		
	});
	$("#update_next").on('click',function(){
		var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
		
		var params = {
			'csrfmiddlewaretoken':csrfmiddlewaretoken,
                'patient_id': patientid,
                'email': email,
                'address': address,
                'social_security_number': ssn,
                'zipcode': zipcode,
                'cellphone': cellphone
            };

		
		$.ajax({url:'/getpatient',
					method:'post',
					data:params,
					success:function(resp){
						alert("Update Successful !!");
						
											
					}
				   });

		
	});
	
	$.ajax({url:'/getdoctordetails',
					method:'get',
					success:function(resp){
						var doc_details = resp['data'];
                        var wait_time = doc_details['total_wait_time'];
                        var total_patients = doc_details['total_patients'];
                        var temp = wait_time / total_patients;
                        var mins = Math.floor(temp);
                        var temp2 = temp - mins;
                        if (temp2 == 0) {
                            var secs = 0;
                        } else {
                            var secs = Math.floor(temp2 * 60);
                        }
						$("#mins").html(mins);
						$("#secs").html(secs);
					}
				   });

	
	
	getappointments('Confirmed');
	getduration();
	

	
		
	function setpatientData(pid){
		$.ajax({url:'/getappointment',
					method:'get',
					data:{'p_id':pid},
					success:function(resp){
						$("#step2_resp").empty().append(resp);
						next_step.show();
						current_step.hide();
						setProgressBar(++current);
					}

			   });
		
	}
});

function getduration(){
	
}

function getappointments(status){
	$.ajax({url:'/doctorappointments',
					method:'get',
					data:{'status':status},
					success:function(resp){
						$("#resp_data").html(resp);
				 $(document).find('#doctors_table').DataTable();	
					}
				   });
	}