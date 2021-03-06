/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// geting the values from template checkout.html
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);  //slice the double quotations
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements(); // creating an instance of stripe elements
// style
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style: style}); // create card element
card.mount('#card-element'); // mount the card to the div. mount()=Activates a component, enabling it to autoredraw on user events

// Handle realtime validation errors on the card element
//for example if he card number is invalid a message in red will show below the box

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
// process:
// when hit the checkout page stripe create a payment IntersectionObserver
// Stripe returns client_secret, which is return to the template
// Use client_secret in the template to call confirmCardpayment() and verify the card number

// handle form submit
var form = document.getElementById('payment-form');
console.log("OUT console log---------***********-----------------**************------------")

form.addEventListener('submit', function(ev) {
    console.log("inside console log---------***********-----------------**************------------")
    // below, prevent form from submitting in order to run the code below
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    // below three lines has to do with fading form and displaying loading overlay 
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Getting the value of saveInfo box
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    // object to pass info to the payment intent
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    // creating url
    var url = '/checkout/cache_checkout_data/';
    console.log("before post function---------***********-----------------**************------------")
    // post data above to the view with the url and postData object in it
    $.post(url, postData).done(function () {
        console.log("inside post function---------***********-----------------**************------------")

    // below line is to send the card info to stripe securely. It is built in function from stripe
        stripe.confirmCardPayment(clientSecret, {
            // below is to store payment information to be used with stripe
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function (result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                // below 2 ByteLengthQueuingStrategy. to fade form and show loading spinning 
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                // if the there is an error allow the user to fix it. 4 lines below
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                // submit the form if the status comes back as SecurityPolicyViolationEventDisposition. status is found on the dictionary result from print(intent) found on the views.py
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    })
});

