const form = document.getElementById("drinkForm"); //this line of code retrieves the HTML element with the ID "drinkForm" and assigns it to the variable 'form'.
const addtoorderbtn = document.getElementById("addToOrder"); // Get the "Add to Order" button
const placeorderbtn = document.getElementById("placeOrder"); // Get the "Place Order" button
const orderlist = document.getElementById('orderList'); // Get the list element for displaying orders
const totalcost = document.getElementById("totalCost"); // Get the element for displaying total cost
const sizeChoice = document.getElementById("sizeSlecet"); // Get the dropdown for selecting drink size

//const is used if you don't want the varible to change.
const drinkType = document.getElementById("sizeType"); // Get the dropdown for selecting drink type

//VAR is simpler to const but the behaviours in the variable can change based on the situation 
var juiceBaseFieldset = document.getElementById('juicebasefieldset'); // Get the fieldset for juice base options
var milkBaseFieldset = document.getElementById('milkbasefieldset'); // Get the fieldset for milk base options
var extratoppingsCheckboxes = document.getElementsByName('extratoppings'); // Get an array of checkboxes for extra toppings

// Define a container for ingredients
const ingredientsContainer = document.getElementById('ingredientsContainer');

// This line of code initializes an empty object named 'orderDetails' which will be used to store details of drink order.
let orderDetails = {};


// Function to calculate total order cost
function calculateTotalOrderCost() {
  // Initialize total cost
  let totalOrderCost = 0;

  // Loop through each drink in the order
  for (const drink in orderDetails) {
    const drinkDetails = orderDetails[drink];
    let drinkCost = parseFloat(drinkDetails.sizechoiceValue);

    // If the drink is a milkshake, add the cost of extra toppings
    if (drinkDetails.type === 'milkshake') {
      drinkCost += getCheckedToppings().length * 0.85;
    }

    // Add drink cost to total
    totalOrderCost += drinkCost;
  }

  // Store total order cost in session storage and return it
  sessionStorage.setItem("TotalCost", totalOrderCost);
  return totalOrderCost.toFixed(2);
}

// Function to calculate extra toppings cost
function calculateExtraToppingsCost(toppings) {
  return toppings.reduce((acc, curr) => acc + parseFloat(curr), 0);
}

// Function to calculate total cost of current drink
function calculateTotalCost() {
  const sizeCost = parseFloat(getSelectedValue(sizeChoice));
  const extraToppingsCost = getCheckedToppings().length * 0.85;
  totalcost.innerText = (sizeCost + extraToppingsCost).toFixed(2);
}

// Function to get value of selected radio button
function getSelectedValue(radio) {
  var productSelect = document.getElementById('sizeSlecet');
  return productSelect.value;
}

// Function to get type of selected drink
function getDrinkType(radio) {
  return drinkType.value;
}

// Function to get selected ingredients
function getIngredient(radio) {
  var ingredients = [];
  var ingredientCheckboxes = document.getElementsByName('ingredients');
  ingredientCheckboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      ingredients.push(checkbox.value);
    }
  });
  return ingredients;
}
// Function to fetch and process ingredients from JSON file
function fetchIngredientsFromJSON() {
  fetch('ingredients.json') // Fetch the JSON file named 'ingredients.json'
      .then(response => response.json()) // Convert the response to JSON format
      .then(data => {
          const ingredients = data.ingredients; // Extract the list of ingredients from the JSON data

          // Loop through each ingredient and create checkboxes for them
          const ingredientsContainer = document.getElementById('ingredientsContainer'); // Find the place on the webpage for checkboxes
          ingredients.forEach(ingredient => { // Loop through each ingredient
              ingredientsContainer.innerHTML += `
                  <input type="checkbox" name="ingredients" value="${ingredient.name}">
                  <label>${ingredient.name}</label><br>
              `;
          });
      })
      .catch(error => {
          console.error('Error fetching ingredients:', error); // Log an error message if something goes wrong
      });
}




// Call the function when the page loads
document.addEventListener('DOMContentLoaded', fetchIngredientsFromJSON);

// Function to get checked extra toppings
function getCheckedToppings() {
  var extratoppings = [];
  extratoppingsCheckboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      extratoppings.push(checkbox.value);
    }
  });
  console.log('toppings:',extratoppings)
  return extratoppings;
}

// Function to update the order display
function updateOrderDisplay() {
  // Clear the order list
  orderlist.innerHTML = '';

  // Loop through each drink in the order
  for (const drink in orderDetails) {
    const drinkDetails = orderDetails[drink];
    const sizeCost = parseFloat(drinkDetails.sizechoiceValue);
    let drinkCost = sizeCost;

    // If the drink is a milkshake, add the cost of extra toppings
    if (drinkDetails.type === 'milkshake') {
      drinkCost += getCheckedToppings().length * 0.85;
    }

    // Create list item to display drink details
    const listItem = document.createElement('li');

    // Display ingredients based on drink type
    if (drinkDetails.type === 'smoothie') {
      listItem.textContent = `${drinkDetails.sizechoice} ${drinkDetails.type}: ${drinkDetails.ingredients.join(', ')} with ${drinkDetails.juicebase}`;
    } else if (drinkDetails.type === 'milkshake') {
      listItem.textContent = `${drinkDetails.sizechoice} ${drinkDetails.type}: ${drinkDetails.ingredients.join(', ')} with ${drinkDetails.milkbase} and extra ${drinkDetails.extratoppings.join(', ')}`;
    }

    // Add cost per drink to display
    const costSpan = document.createElement('span');
    costSpan.textContent = ` £${drinkCost.toFixed(2)}`; // Display cost per drink
    listItem.appendChild(costSpan);
    orderlist.appendChild(listItem);
  }

  // Display total order cost
  const totalOrderItem = document.createElement('li');
  totalOrderItem.textContent = `Order total:`;
  const totalCostSpan = document.createElement('span');
  totalCostSpan.textContent = ` £${calculateTotalOrderCost()}`;
  totalOrderItem.appendChild(totalCostSpan);
  orderlist.appendChild(totalOrderItem);
}

// Event listeners for changes in size selection and "Add to Order" button
for (const sizeRadioButton of sizeChoice) {
  sizeRadioButton.addEventListener('change', calculateTotalCost);
}

// Event listener for "Add to Order" button click
addtoorderbtn.addEventListener("click", function(evt) {
  evt.preventDefault();
  if (form.checkValidity()) {
    const formData = new FormData(form);
    const drinkDetails = {};
    
    for (const [name, value] of formData) {
      drinkDetails[name] = value;
    }
    drinkDetails.ingredients = getIngredient();
    drinkDetails.sizechoice =  getSelectedValue(sizeChoice).split(' - ')[0];
    drinkDetails.sizechoiceValue =  getSelectedValue(sizeChoice).split(' - ')[1].substring(1);
    drinkDetails.type = getDrinkType(drinkType);
    if (milkBaseFieldset.style.display !== 'none') {
      drinkDetails.milkbase = document.querySelector('input[name="milkbase"]:checked') ? document.querySelector('input[name="milkbase"]:checked').value : null;
    }
    else {
      drinkDetails.juicebase = document.querySelector('input[name="juicebase"]:checked') ? document.querySelector('input[name="juicebase"]:checked').value : null;
    }
    
    drinkDetails.extratoppings = getCheckedToppings();

    orderDetails[`Drink ${Object.keys(orderDetails).length + 1}`] = drinkDetails;

    updateOrderDisplay();
    try {
      form.reset(); // Attempt to reset the form for a new order

      sizeChoice.selectedIndex = 2; 
      drinkType.selectedIndex = 0; 
      const ingredientCheckboxes = document.getElementsByName('ingredients');
      ingredientCheckboxes.forEach(checkbox => checkbox.checked = false);
      // Hide milk and juice base fieldsets
      milkBaseFieldset.style.display = 'none';
      juiceBaseFieldset.style.display = 'none';
    } catch (error) {
      console.error("Error resetting form:", error.message);
    }
  }
});

// Function to retrieve total order cost from session storage
function calculateTotalOrderCostSeessionstorage(){
  return sessionStorage.getItem("TotalCost");
}

// Event listener for "Place Order" button click
placeorderbtn.addEventListener("click", function() {
  alert(`Your order has been placed! Total cost: £${calculateTotalOrderCostSeessionstorage()}`);
  sessionStorage.removeItem("TotalCost");
  form.reset();
  orderDetails = {};
  updateOrderDisplay();
});

// Function to initialize the page
function initialize() {
  // Load any initial data or configurations
}

// Initialize the page when DOM content is loaded
document.addEventListener("DOMContentLoaded", initialize);

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
  // Get references to various elements
  var productSelect = document.getElementById('sizeSlecet');
  var priceDisplay = document.getElementById('cost');

  // Function to update price based on selection
  function updatePrice() {
    console.log(productSelect.value.split(' - ')[1].substring(1));
    var selectedPrice = parseFloat(productSelect.value.split(' - ')[1].substring(1)) + getCheckedToppings().length * 0.85;;
    priceDisplay.textContent =  + selectedPrice;
  }

  // Call the updatePrice function on page load
  updatePrice();

  // Attach change event listener to sizeType
  productSelect.addEventListener('change', updatePrice);

  // Attach change event listener to checkboxes for extra toppings
  var checkboxesExtra = document.querySelectorAll('input[name="extratoppings"]');
  checkboxesExtra.forEach(function(checkboxesExtra) {
    checkboxesExtra.addEventListener('change', updatePrice);
  });

  // Get reference to sizeType and extra toppings fieldset
  var sizeType = document.getElementById('sizeType');
  const extraToppingsFieldset = document.getElementById('extratoppingsfieldset');

  // Function to display juicebase or milkbase fieldsets based on selection
  function displayJuicebase() {
    var sizeTypeOption = sizeType.value;
    if(sizeTypeOption == 'smoothie'){
        console.log('smoothie selected');
        milkBaseFieldset.style.display  = 'none';
        extraToppingsFieldset.style.display = 'none'
        juiceBaseFieldset.style.display  = 'block';
    }
    else if (sizeTypeOption == 'milkshake'){
      juiceBaseFieldset.style.display  = 'none';
      milkBaseFieldset.style.display  = 'block';
      extraToppingsFieldset.style.display = 'block'
    }
    else{
      juiceBaseFieldset.style.display  = 'hide';
    }
  }

  // Attach change event listener to sizeType
  sizeType.addEventListener('change', displayJuicebase);

  // Get references to checkboxes and submit button
  var checkboxes = document.querySelectorAll('input[name="ingredients"]');
  var submitButton = document.getElementById('saveFavorite');

  // Function to update button state based on checkbox selection
  function updateButtonState() {
    var atLeastOneChecked = false;
    checkboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        atLeastOneChecked = true;
      }
    });

    submitButton.disabled = !atLeastOneChecked;
  }

  // Attach change event listener to checkboxes
  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', updateButtonState);
  });

// Get reference to the "Order My Favorite" button
var orderFavoriteButton = document.getElementById('orderFavorite');

// Check if the "favoriteDrink" item exists in local storage
var favoriteDrink = localStorage.getItem('favoriteDrink');

if (!favoriteDrink) {
    // If favoriteDrink is not available, disable the "Order My Favorite" button
    orderFavoriteButton.disabled = true;
}

// Event listener for "Order My Favorite" button click
orderFavoriteButton.addEventListener('click', function() {
  // Retrieve favorite drink data from local storage
  var favoriteData = JSON.parse(localStorage.getItem('favoriteDrink'));

  console.log('Placing order for favorite drink:', `${favoriteData.size}  ${favoriteData.type} ${favoriteData.ingredients.join(', ')}`);
  showFavourate(favoriteData);
  
});


function showFavourate(drinkDetails) {
  orderlist.innerHTML = '';

    const listItem = document.createElement('li');
    if (drinkDetails.hasOwnProperty("milkBase")) {
      listItem.textContent = `${drinkDetails.size} ${drinkDetails.type}: ${drinkDetails.ingredients.join(', ')} with ${drinkDetails.milkBase} and extra ${drinkDetails.extraToppings.join(', ')}`;
    } else {
      listItem.textContent = `${drinkDetails.sizechoice} ${drinkDetails.type}: ${drinkDetails.ingredients.join(', ')} with ${drinkDetails.juiceBase}`;
    }
    
    const costSpan = document.createElement('span');
    costSpan.textContent = ` £${drinkDetails.cost}`;
    listItem.appendChild(costSpan);
    orderlist.appendChild(listItem);


  const totalOrderItem = document.createElement('li');
  totalOrderItem.textContent = `Order total:`;
  const totalCostSpan = document.createElement('span');
  totalCostSpan.textContent = ` £${drinkDetails.cost}`;
  totalOrderItem.appendChild(totalCostSpan);
  orderlist.appendChild(totalOrderItem);
}
  // Get reference to "Save My Favorite" button
  var saveFavoriteButton = document.getElementById('saveFavorite');

  // Add event listener to "Save My Favorite" button
  saveFavoriteButton.addEventListener('click', function() {
    // Get references to form elements
    var sizeSelect = document.getElementById('sizeSlecet');
    var typeSelect = document.getElementById('sizeType');
    var ingredientCheckboxes = document.querySelectorAll('#Ingredients input[type="checkbox"]');
    var extraToppingsCheckboxes = document.querySelectorAll('#extratoppingsfieldset input[type="checkbox"]');
    var costvalue = document.getElementById('cost').innerHTML;

    // Collect form data
    var favoriteData = {
      size: sizeSelect.value.split(' - ')[0],
      type: typeSelect.value,
      ingredients: [],
      juiceBase: '',
      milkBase: '',
      extraToppings: [],
      cost: costvalue
    };

    // Collect selected ingredients
    ingredientCheckboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        favoriteData.ingredients.push(checkbox.value);
      }
    });

    // Collect selected juice base
    if (juiceBaseFieldset.style.display !== 'none') {
      var juiceBaseRadioButtons = document.querySelectorAll('input[name="juicebase"]');
      juiceBaseRadioButtons.forEach(function(radioButton) {
        if (radioButton.checked) {
          favoriteData.juiceBase = radioButton.value;
        }
      });
    } else {
      // Remove juiceBase property if fieldset is hidden
      delete favoriteData.juiceBase;
    }

    // Collect selected milk base
    if (milkBaseFieldset.style.display !== 'none') {
      var milkBaseRadioButtons = document.querySelectorAll('input[name="milkbase"]');
      milkBaseRadioButtons.forEach(function(radioButton) {
        if (radioButton.checked) {
          favoriteData.milkBase = radioButton.value;
        }
      });
    } else {
      // Remove milkBase property if fieldset is hidden
      delete favoriteData.milkBase;
    }

    // Collect selected extra toppings
    extraToppingsCheckboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        favoriteData.extraToppings.push(checkbox.value);
      }
    });

    // Save favorite data to local storage
    localStorage.setItem('favoriteDrink', JSON.stringify(favoriteData));

    // Enable "Order My Favorite" button
    document.getElementById('orderFavorite').disabled = false;

    // Notify user that favorite has been saved
    alert('Your favorite drink has been saved!');

    
  });

  // Update button state initially
  updateButtonState();
});