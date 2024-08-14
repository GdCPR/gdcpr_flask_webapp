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
      console.log(data.output)
    });
    e.preventDefault();
  });
});