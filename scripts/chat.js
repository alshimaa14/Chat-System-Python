var webSocket;
var name;
var names;
$(function(){

	webSocket= new WebSocket("ws://localhost:8888/ws");
	webSocket.onmessage = function(e){
		// console.log(e.data);
		names=JSON.parse(e.data)
		console.log(names)
		if(names['name']=="userNames"){
				$("#clientNames").html("")
				names=names['names']
				$("#clientNames").append("<option value='all'>all</option>")
			names.forEach(function(elm,idx){
				$("#clientNames").append("<option value="+elm+">"+elm+"</option>")
			})
		}
		else
		{
				detmessage=names['message'].split(":")
				msg=detmessage[0]+":"+detmessage[2]
				console.log(detmessage)
				if((name==detmessage[1] || detmessage[1]=="all")||(name==detmessage[0]))
					$("#mytext").append("<P>"+msg+"</p>")
		}
	}
	$('#change').click(function(e){
			name=$("#myname").val()
				webSocket.send("name :"+name)
				console.log(name)
	})
	$('#send').click(function(e){
		var msg = $("#message").val()
		var to=$("#clientNames").val()
		console.log(to);
		mymsg=name+":"+to+":"+msg
		webSocket.send(mymsg)
		$("#message").val('')
	})
})
