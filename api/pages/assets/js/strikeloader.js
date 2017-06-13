function loadStrike() {
  var strike = $("#selectedstrike").val();
  $(".loading").fadeIn();
  $.get("https://tbij.dronescout.org/strike?strike=" + strike, function(data, status) {
    $(".loading").fadeOut();
    alert("Data: " + data + "\nStatus: " + status);
  });
}
