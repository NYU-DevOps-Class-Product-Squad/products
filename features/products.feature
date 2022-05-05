Feature: The product service back-end
    As a Retail Product Website
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name   | category  | available | price |
        | Jacket | Clothing  | True      | 100   |
        | Shirt  | Clothing  | False     | 150   |
        | Pen    | Stationary| True      | 200   |
        | Couch  | Furniture | False     | 250   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "name" to "Jacket"
    And I set the "category" to "Clothing" 
    #And I select "avaliable" 
    And I set the "price" to "100"
    And I press the "Create" button
    Then I should see the message "Success"
    # When I copy the "id" field
    # And I press the "Clear" button
    # Then the "id" field should be empty
    # And the "name" field should be empty
    # And the "category" field should be empty
    # And the "price" field should be empty
    # When I paste the "id" field
    # And I press the "Retrieve" button
    # Then I should see "Jacket" in the "name" field
    # And I should see "Clothing" in the "category" field
    # #And I should see "TRUE" in the "Available" dropdown
    # And I should see "100" in the "price" field


# Scenario: Search for categories
#     When I visit the "Home Page"
#     And I set the "Category" to "Top"
#     And I press the "Search" button
#     Then I should see "jacket" in the results
#     And I should  see "shirt" in the results
#     And I should not see "pants" in the results
#     And I should not see "socks" in the results

# Scenario: Search for available
#     When I visit the "Home Page"
#     And I select "TRUE" in the "Available" dropdown
#     And I press the "Search" button
#     Then I should see "jacket" in the results
#     And I should see "socks" in the results
#     And I should not see "shirt" in the results
#     And I should not see "pants" in the results

# Scenario: Update a product
#     When I visit the "Home Page"
#     And I set the "Name" to "jacket"
#     And I press the "Search" button
#     Then I should see "jacket" in the "Name" field
#     And I should see "top" in the "Category" field
#     When I change "Name" to "Blue jacket"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see "Blue jacket" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see "Blue jacket" in the results
#     Then I should not see "jacket" in the results
