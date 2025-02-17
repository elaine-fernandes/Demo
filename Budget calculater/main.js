//get references to interactive elements
const txtWeeklyBudget = document.getElementById("WeeklyBudget");
const txtRent = document.getElementById("Rent");
const txtFood = document.getElementById("Food");
const txtTransport = document.getElementById("Transport");
const btnCalculate = document.getElementById("Calculate");
const txtResult = document.getElementById("Result")

//listen for user interactions
btnCalculate.addEventListener("click", calculate);

//declare variables used by event handlers
RemaingBudget = 0;

//when user clicks add result button
function Calculate() {

    //input subject
    let weeklybudget = parseFloat(txtWeeklyBudget.value) ;
    //input result
    let rent = parseFloat(txtRent.value);
    let transport = parseFloat(txtTransport.value);
    let food = parseFloat(txtFood.value);

    let RemaingBudget = weeklybudget - rent - food - transport;

    

}

alert(`${weeklybudget}'s results`);
    
    txtResult.innerText = `${weeklybudget} has an budget of ${RemaingBudget.toFixed(2)}`;
   
;