






$(document).ready(function() {

    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();


        // Check if an address is selected
        var selectedAddress = $("input[name='address']:checked").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        if (!selectedAddress) {
            swal("Alert!", "Please select an address before proceeding with the payment.",'error');
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/order/proceed-to-pay",
                success: function (response) {
                   console.log(response);
                   var options = {
                    "key": "rzp_test_9mI3x0STwZvFoe", // Enter the Key ID generated from the Dashboard
                    "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Sa Footwear",
                    "description": "Thank you for buying from us",
                    "image": "https://example.com/your_logo",
                    // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (responseb){
                        alert(responseb.razorpay_payment_id);
                        data = {
                            "selectedAddress" : selectedAddress,
                            'payment_mode' : "Paid by Razorypay",
                            "payment_id" : responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: token,

                        }


                        $.ajax({
                            method: "POST",
                            url: "/order/place-order",
                            data: data,
                            success: function (responsec) {
        
                                swal("Order Placed!", responsec.status, 'success').then((value) => {
                                    window.location.href = '/order/order_complete';
                                });
                            },
                            error: function(xhr, status, error) {
                                console.error(xhr.responseText);
                            }
                        });
                        
                    },
                    "prefill": {
                        "name": '{{ user_info.name }}',
                        "email": '{{ user_info.email }}',
                        "contact": '{{ user_info.contact }}',
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                    
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
          
    
        }
       

    });



});