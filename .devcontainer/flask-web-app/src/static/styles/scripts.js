var li_elements = document.querySelectorAll(".wrapper-left ul li");
var item_elements = document.querySelectorAll(".item");
for (var i = 0; i < li_elements.length; i++) {
  li_elements[i].addEventListener("click", function() {
    li_elements.forEach(function(li) {
      li.classList.remove("active");
    });
    this.classList.add("active");
    var li_value = this.getAttribute("data-li");
    item_elements.forEach(function(item) {
      item.style.display = "none";
    });
  })
}

$(document).ready(function() {
  $('.wrapper-left ul li').on('click', function(e){
    $.ajax({
      type : 'POST',
      url : '/',
      data : {"location": this.id}
    })
    .done(function(data){
      console.log("Client query location")
      console.log(data.articlesObj.length)
      if (data.articlesObj.length == 0) {
        // $('.table-container').empty();
        $('#output').text("Showing all articles because database do not contain articles tagged with selected location").show() // Make txt appear in element with id #output
      } else if (data.articlesObj.length > 0) {
        $('#output').hide()
        $('#articles-table').html("");
        for (var i = 0; i < data.articlesObj.length; i++) {
          var row = data.articlesObj[i];
          $('#articles-table').append('<tr><td data-cell="datetime">' + row.DateTime
            + '</td><td data-cell="headline-author-subheadline"><a href="{{row.URL}}" target="_blank">' + row.Headline + '</a>'
            + '<p>' + row.Subheadline + '</p>'
            + '<p> Por: ' + row.Author + '</p></td>');
        }
      }
    });
    e.preventDefault();
  });
});