//get references to interactive elements
const txtName = document.getElementById("name");
const txtSubject = document.getElementById("subject");
const txtResult = document.getElementById("result");
const txtOutput = document.getElementById("output");
const btnAddResult = document.getElementById("addResult");
const btnCalculateAverage = document.getElementById("calculateAverage");

//listen for user interactions
btnAddResult.addEventListener("click", addResult);
btnCalculateAverage.addEventListener("click", calculateAverage);

//declare variables used by event handlers
let sum;
let count;
let subjects;

//initialise default values
initialise();

//initialise default values
function initialise() {
    sum = 0;
    count = 0;
    subjects = "";
    
}

//when user clicks add result button
function addResult() {
    //input subject
    let subject = txtSubject.value;
    //input result
    let result = parseInt(txtResult.value);
    //increase sum by result
    sum += result; //or sum = sum + result;
    //increase count by 1
    count++;
    //append subject to subjects
    subjects += `${subject} `;
    //display subject and result, and reset input
    txtOutput.innerText = subjects;
    txtResult.value = 0;
    txtSubject.value = "";

}

//when user clicks calculate average button
function calculateAverage() {
    //input name
    let name = txtName.value;
    
    //average = sum / count
    let average = sum / count;
    
    //determine grade based on average
    let grade;if (average < 40) {
        grade = "Fail";
    } else if (average < 65) {
        grade = "Pass";
    } else if (average < 80) {
        grade = "Merit";
    } else {
        grade = "Distinction";
    }
    
    //display name in pop-up
    
    alert(`${name}'s results`);
    //output name, subjects and average
    txtOutput.innerText = `${name} has an average of ${average.toFixed(2)}`;}