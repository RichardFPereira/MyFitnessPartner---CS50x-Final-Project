function hideShowExercises(buttonId) {
    switch (buttonId) {
        case "BicepsButton":
            if (document.getElementById("Biceps").style.visibility == 'hidden') {
                document.getElementById("Biceps").style.visibility = 'visible';
            }
            else {
                document.getElementById("Biceps").style.visibility = 'hidden';
            }
            break;
        case "BackButton":
            if (document.getElementById("Back").style.visibility == 'hidden') {
                document.getElementById("Back").style.visibility = 'visible';
            }
            else {
                document.getElementById("Back").style.visibility = 'hidden';
            }
            break;
        case "CalvesButton":
            if (document.getElementById("Calves").style.visibility == 'hidden') {
                document.getElementById("Calves").style.visibility = 'visible';
            }
            else {
                document.getElementById("Calves").style.visibility = 'hidden';
            }
            break;
        case "CardioButton":
            if (document.getElementById("Cardio").style.visibility == 'hidden') {
                document.getElementById("Cardio").style.visibility = 'visible';
            }
            else {
                document.getElementById("Cardio").style.visibility = 'hidden';
            }
            break;
        case "ChestButton":
            if (document.getElementById("Chest").style.visibility == 'hidden') {
                document.getElementById("Chest").style.visibility = 'visible';
            }
            else {
                document.getElementById("Chest").style.visibility = 'hidden';
            }
            break;
        case "CoreButton":
            if (document.getElementById("Core").style.visibility == 'hidden') {
                document.getElementById("Core").style.visibility = 'visible';
            }
            else {
                document.getElementById("Core").style.visibility = 'hidden';
            }
            break;
        case "LegsButton":
            if (document.getElementById("Legs").style.visibility == 'hidden') {
                document.getElementById("Legs").style.visibility = 'visible';
            }
            else {
                document.getElementById("Legs").style.visibility = 'hidden';
            }
            break;
        case "TrapeziusButton":
            if (document.getElementById("Trapezius").style.visibility == 'hidden') {
                document.getElementById("Trapezius").style.visibility = 'visible';
            }
            else {
                document.getElementById("Trapezius").style.visibility = 'hidden';
            }
            break;
        case "TricepsButton":
            if (document.getElementById("Triceps").style.visibility == 'hidden') {
                document.getElementById("Triceps").style.visibility = 'visible';
            }
            else {
                document.getElementById("Triceps").style.visibility = 'hidden';
            }
            break;
        default:
            break;
    }
}

function checkTrainning(elementId) {
    if (document.getElementById(elementId).style.textDecoration == "line-through") {
      document.getElementById(elementId).style.textDecoration = "none";
    }
    else {
      document.getElementById(elementId).style.textDecoration = "line-through";
    }

  }