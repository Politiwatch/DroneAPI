function loadStrike() {
  var strike = $("#selectedstrike").val();
  $(".loading").fadeIn();
  $.ajax({
    url: "/strike?strike=" + strike,
    type: "GET",
    dataType: "json",
    timeout: 10000,
    success: function(data, status, jqXHR) {
      $(".loading").fadeOut();
      $(".strike-index").text(data.index)
      $(".strike-date").text(data.date)
      $(".strike-minkilled").text(data.minKilled)
      $(".strike-maxkilled").text(data.maxKilled)
      $(".strike-location").text(data.location)
      $(".strike-type").text(data.type)
      $(".strike-json").html(jqXHR.responseText)
      $(".strike-apiurl").attr("href", "/strike?strike=" + data.index)
      var body = data.body
      if(data.body == null){
        body = "<i>No description available.</i>"
      }
      $(".strike-description").html(body)
    },
    error: function(xmlhttprequest, textstatus, message) {
        $(".loading").fadeOut();
        alert("Unable to complete your request: " + message)
    }
  });
}

$('#export-form .input-daterange').datepicker({
  todayHighlight: true
});
