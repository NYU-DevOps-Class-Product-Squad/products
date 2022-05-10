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
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "name" to "Pants"
    And I set the "category" to "Clothing" 
    And I select "True" in the "available" dropdown
    And I set the "price" to "75"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "category" field should be empty
    And the "price" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "Pants" in the "name" field
    And I should see "Clothing" in the "category" field
    And I should see "True" in the "available" dropdown
    And I should see "75" in the "price" field

Scenario: Query by Name
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "name" to "Jacket"
    And I press the "Search" button
    Then I should see "Jacket" in the results
    And I should not see "Shirt" in the results
    And I should not see "Pen" in the results
    And I should not see "Couch" in the results

Scenario: Query by Category
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "category" to "Clothing"
    And I press the "Search" button
    Then I should see "Jacket" in the results
    And I should see "Shirt" in the results
    And I should not see "Pen" in the results
    And I should not see "Couch" in the results

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Jacket" in the results
    And I should see "Shirt" in the results
    And I should see "Pen" in the results
    And I should see "Couch" in the results

Scenario: Disable a Product
    When I visit the "Home Page"
    And I press the "Search" button
    #And I copy the "id" field
    And I press the "Disable" button
    #And I paste the "id" field
    #And I press the "Retrieve" button
    Then I should see "False" in the "available" dropdown

Scenario: Delete a Product
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Jacket" in the results
    When I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    
Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "name" to "Shirt"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Shirt" in the "name" field
    And I should see "Clothing" in the "category" field
    And I should see "False" in the "available" dropdown
    And I should see "150" in the "price" field
    
Scenario: Update Product
    When I visit the "Home Page"
    And I set the "name" to "Pen"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Pen" in the "name" field
    And I should see "Stationary" in the "category" field
    And I should see "True" in the "available" dropdown
    And I should see "200" in the "price" field
    When I change "price" to "15"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Pen" in the "name" field
    And I should see "Stationary" in the "category" field
    And I should see "True" in the "available" dropdown
    And I should see "15" in the "price" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "15" in the results
    And I should not see "200" in the results
 
