var choosed_login='login';
var islogin = false;
function status(){
  $.ajax({
    type: "GET",
    url: "/api/islogin",
    success: function(data)
    {
      if (data == "OK"){
        console.log("Workform");
        $("#workform").show()
        $("#mainform").hide()
        islogin=true;
      }
      else{
        $("#mainform").show()
        $("#workform").hide()
        islogin=false;
      }
      console.log(data);
    }
  });
}
function init(){
  status()
  $( 'input[type="submit"]').click(function() {
    a =$("#usr").val();
    b =$("#pwd").val();
    console.log("submit clicked " + a + " "+b);

    if (a.length != 0 && b.length !=0){
      $.ajax({
        type: "GET",
        url: "/api/"+choosed_login,
        data: {"username":a, "password":b},
        success: function(data)
        {
          if (data == "OK"){
            $('#status').html("success");
            status()
          }
          else{
            $("#status").html("Invalid login or password");
          }
          console.log("data:",data);
        }
      });
    }
  });
  $( '#Register_ref' ).click(function(){
    $("#Login_ref").removeClass("choosed");
    $("#Register_ref").addClass("choosed");
    choosed_login ="register";
    $("#submit_login").val("Register")
  });
  $( '#Login_ref' ).click(function(){
    $("#Login_ref").addClass("choosed");
    $("#Register_ref").removeClass("choosed");
    choosed_login ="login";
    $("#submit_login").val("Login")
  });
  $("#sendfile").click(function (event) {
      event.preventDefault();
      var form = $('#sendform')[0];
      var data = new FormData(form);
      $.ajax({
          type: "POST",
          enctype: 'multipart/form-data',
          url: "/api/convert",
          data: data,
          processData: false,
          contentType: false,
          cache: false,
          timeout: 600000,
          success: function (data) {
              console.log();
              $("#status_mes").html(data);
          },
      });
  });
  setInterval(function(){
    if (islogin){
      $.ajax({
        type: "GET",
        url: "/api/list",
        cache: false,
        success: function (jsn){
          console.log(jsn);
          data="";
          for (var i=0; i<jsn.data.length;i++){
            d=jsn.data[i]
            data += "<tr>";
            data += "<th> Gifs</th>";
            data += "<td>";
            data += jsn.data[i]['infile'];
            data += "</td>";
            data += "<td>";
            data += jsn.data[i]['status'];
            data += "</td>";
            data += "<td>";
            data += "<a href='/out/"+jsn.data[i]['outfile']+"''>"+jsn.data[i]['outfile']+"</a>";
            data += "</td>";
            data += "</tr>";
          }
          $("#results").html(data);
        },
      });
    }
  }, 5000);
}
