

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =", data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            if (data.quantity == 0) {
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            }
        }
        
    });
})


$(".remove-cart").click(function () {
  let id = $(this).attr("pid");
  $.ajax({
    url: "/remove_cart/",  
    method: "GET",        
    data: {
      prod_id: id
    },
    success: function (response) {
      location.reload();
    }
  });
});