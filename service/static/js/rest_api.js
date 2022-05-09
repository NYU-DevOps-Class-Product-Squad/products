$(function () {
    // *******************************************************
    //  U T I L I T Y   F U N C T I O N S
    // *******************************************************
    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    };
    // *******************************************************
    //  P R O D U C T   U T I L I T Y   F U N C T I O N S
    // *******************************************************
    // Updates the form with data from the response
    function update_product_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_category").val(res.category);
        $( "#product_available" ).val(res.available);

        if(res.available == true){
            $( "#product_available" ).val("true");
        }
        else{
            $( "#product_available" ).val("false");
        }

        $("#product_price").val(res.price);
    };
    /// Clears all form fields
    function clear_product_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_price").val("");
        $("#product_available").val("");
    };

    // *******************************************************
    //  P R O D U C T   F U N C T I O N S
    // *******************************************************
    // Create a Product
    // *******************************************************
    $("#create-btn").click(function () {
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let price = $("#product_price").val();
        let available = $("#product_available").val() == "true";

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "price": price
        };

        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        ajax.done(function(res){
            update_product_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Update a Product
    // *******************************************************
    $("#update-btn").click(function () {
        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let price = $("#product_price").val();
        let available = $("#product_available").val() == "true";

        
        let data = {
            "name": name,
            "category": category,
            "price": price,
            "available": available
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_product_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Retrieve a Product
    // *******************************************************
    $("#retrieve-btn").click(function () {
        let product_id = $("#product_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            update_product_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            clear_product_form_data();
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Delete a Product
    // *******************************************************
    $("#delete-btn").click(function () {
        let product_id = $("#product_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            clear_product_form_data();
            flash_message("Product has been Deleted!");
        });
        ajax.fail(function(res){
            flash_message("Server error!");
        });
    });
    // *******************************************************
    // Clear the product form
    // *******************************************************
    $("#clear-btn").click(function () {
        clear_product_form_data();
        $("#flash_message").empty();
    });
    // *******************************************************
    // Search for a Product
    // *******************************************************
    $("#search-btn").click(function () {
        let id = $("#product_id").val();
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let price = $("#product_price").val();
        let available = $("#product_available").val() == "true";   
        
        var previousQuery = false;

        let queryString = "";
        if (id) {
            queryString = '/' + id
        };

        if (name) {
            queryString += '?name=' + name;
            previousQuery = true;
        };

        if (category) {
            if(previousQuery){
                queryString += "&";
            }
            else{
                queryString += "?";
            }
            queryString += 'category=' + category;
            previousQuery = true;
        };

        if (price) {
            if(previousQuery){
                queryString += "&";
            }
            else{
                queryString += "?";
            }
            queryString += 'price=' + price;
            previousQuery = true;
        };

        if (available) {
            if(previousQuery){
                queryString += "&";
            }
            else{
                queryString += "?";
            }
            queryString += 'available=' + available;
        };

        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/products${queryString}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){

            console.log("query is " + ("/products" + queryString));
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th class="col-md-2">ID</th>';
            table += '<th class="col-md-2">Name</th>';
            table += '<th class="col-md-2">Category</th>';
            table += '<th class="col-md-2">Availability</th>';
            table += '<th class="col-md-2">Price</th>';
            table += '</tr></thead><tbody>';
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.category}</td><td>${product.available}</td><td>${product.price}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                };
            };
            table += '</tbody></table>';
            $("#search_results").append(table);
            // copy the first result to the form
            if (firstProduct != "") {
                update_product_form_data(firstProduct)
            };
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Disable a product
    // *******************************************************
    $("#disable-btn").click(function () {
        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let price = $("#product_price").val();
        let available = false;
        
        let data = {
            "name": name,
            "category": category,
            "price": price,
            "available": available
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}/disable`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_product_form_data("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

});