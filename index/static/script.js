$(document).ready(function(){
	// Handles navigating to the forget password form in the login page
	$('.forgetpass').click(function(){
		var ref = $(this).data('access')
		// Setting display:none to the active class
		$('body').find('.innernavactive').removeClass('innernavactive').addClass('hide')

		// Setting display:block to the clicked tag
		$(ref).addClass('innernavactive')
		$(ref).removeClass('hide')
	})

	// Handle toggle of the nav button
	$('.dropimg').on('click', function(){
		$('#data').toggleClass('hide');
	})

	// Handles toggling of the more button
	$('.infodrop .more').click(function(){
		var drop = $(this).data('drop')
		$('#'+drop).toggle(10, function(){
			
		})
	})
	$('.jump .hider').click(function(){
		$('.jump .newacc').toggleClass('hide');
		$('.jump .btnwhite.hider').toggleClass('hide');
	})

	// Handles creation of new log
	$('#newlogForm').on('submit', function(event){
		event.preventDefault();
		var title = $('.jump #newlogForm .newlogtitle').val()
		$.ajax({
			url: '/newlog/',
			method: 'POST',
			data: {
				'title': title,
				'csrfmiddlewaretoken': $('.jump #newlogForm #newlogToken').text()
			},
			success: function(data){
				if(!data){
					alert('Sorry, an error occured')
					return;
				}
				id = $('.jump .account .currentlog').attr('id')
				$('.jump .recents').append("<a href='#' class='recentA' id='account"+id+"'>"+ $('.jump .account .currentlog').text() +"</a>")
				$('.jump .account .currentlog').text( title )
				$('.jump .account .currentlog').attr('id', data.id.toString() )
				$('.jump #newlogForm .newlogtitle').val('')
				$('.jump .spending .acc').html('')

				// Hiding the form and showing the new-log button
				$('.jump .newacc').toggleClass('hide');
				$('.jump .btnwhite.hider').toggleClass('hide');

				$('.jump .norecent').remove();
				$('.jump .account .spending #totinput').text(0)
				$('.jump .account .spending #totoutput').text(0)
			},
			error: function(err){
				console.log(err)
			}
		})
	})

	// Handles creation of new account to a log
	$('#newaccountForm').on('submit', function(event){
		event.preventDefault();
		if(!$('.jump .account .currentlog').attr('id')){
			alert('Please create a log before creating accounts')
			return;
		}
		var accType = $('.jump #newaccountForm input[name="type"]:checked').val()
		var amount = parseInt( $('.jump #newaccountForm input[name="amount"]').val() )
		$.ajax({
			url: '/newaccount/',
			method: 'POST',
			data: {
				'author': parseInt( $('.jump #newaccountForm input[name="author"]').val()),
				'log': parseInt( $('.jump .account .currentlog').attr('id').replace('log', '') ),
				'accType': accType,
				'amount': amount,
				'description': $('.jump #newaccountForm input[name="description"]').val(),
				'csrfmiddlewaretoken': $('.jump #newlogForm #newlogToken').text()
			},
			success: function(data){
				if(!data){
					alert('Sorry, an error occured')
					return;
				}
				$('.jump #newaccountForm input[name="amount"]').val('')
				$('.jump #newaccountForm input[name="description"]').val('')
				$('.jump .account .spending .noacc').remove()

				var newAccTemplate = $('#newaccountTemplate').html();
				$('.jump .spending .acc').append(Mustache.render(newAccTemplate, data))
				if(accType=='input'){
					$('.jump .account .spending #totinput').text( parseInt($('.jump .account .spending #totinput').text())+amount)
				}else{
					$('.jump .account .spending #totoutput').text( parseInt($('.jump .account .spending #totoutput').text())+amount) 
				}
			},
			error: function(err){
				alert('Error')
				console.log(err)
			}
		})
	})

	// Handles fetching of the accounts under the clicked logs
	$('.jump').delegate('.recentA','click', function(event){
		event.preventDefault();
		var id = $(this).attr('id').replace('account', '')
		var self = $(this)
		$.ajax({
			url: '/getacclogs/'+id,
			method: 'GET',
			success: function(data){
				if(!data){
					alert('Sorry, an error occured')
					return;
				}

				var currentIdforOldCurrent = $('.jump .account .currentlog').attr('id').replace('account', '')
				$('.jump .recents').append("<a href='#' class='recentA' id='account"+currentIdforOldCurrent+"'>"+ $('.jump .account .currentlog').text() +"</a>")
				
				$('.jump .account .currentlog').attr('id', id)
				$('.jump .account .currentlog').text( self.text() )
				
				var currentIdforOldCurrent = self.attr('id')

				self.remove();


				$('.jump .account .spending #totinput').text(data[1][0])
				$('.jump .account .spending #totoutput').text(data[1][1])
				if(data[0].length>0){
					$('.jump .account .spending .noacc').remove()
					$('.jump .account .spending .acc').html('')
					var newAccTemplate = $('#newaccountTemplate').html();
					for(var i=0;i<data[0].length;i++){
						$('.jump .account .spending .acc').append(Mustache.render(newAccTemplate, data[0][i]))
					}
				}else{
					$('.jump .account .spending .acc').html('')
					$('.jump .account .spending').append("<h5 class='noacc'>No account yet</h5>")
				}
			},
			error: function(err){
				alert('Error')
				console.log(err)
			}
		})
	})
})
