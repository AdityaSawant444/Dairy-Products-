
$(document).on('click', '.plus-cart', function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$(document).on('click', '.minus-cart', function() {
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
                eml.parentNode.parentNode.parentNode.parentNode.remove();
            }
        }
    });
});

$(document).on('click', '.remove-cart', function() {
    let id = $(this).attr("pid");
    $.ajax({
        url: "/remove_cart/",
        method: "GET",
        data: {
            prod_id: id
        },
        success: function(response) {
            location.reload();
        }
    });
});