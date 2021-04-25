var slider = window.document.getElementById("myRange");
var output = window.document.getElementById("demo");
var fileUpload = document.getElementById("fileUpload");
var upload = document.getElementById("upload");
var back = document.getElementById("back");
var dvCSV = document.getElementById("dvCSV");
var sentencesAndValues = [];
var orderToHide = []
var rangeSize = 100;

output.innerHTML = slider.value; // Display the default slider value

slider.oninput = function() {
    output.innerHTML = this.value;
    
    numToHide = (100 - this.value) / rangeSize;
    for(var i = 0; i < numToHide; i++) {
        var sentence = document.getElementById(orderToHide[i]);
        sentence.style.display = 'none';
    }
    for(var i = numToHide; i < orderToHide.length; i++) {
        var sentence = document.getElementById(orderToHide[i]);
        sentence.innerHTML = sentencesAndValues[i][1] + " ";
        sentence.style.display = 'inline';
    }
}

function Upload() {
    slider.style.display = "block";
    output.style.display = "block";
    fileUpload.style.display = "none";
    upload.style.display = "none";
    back.style.display = "block";
    dvCSV.style.display = 'block';
    dvCSV.innerHTML = "";
    var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
    if (regex.test(fileUpload.value.toLowerCase())) {
        if (typeof (FileReader) != "undefined") {
            var reader = new FileReader();
            reader.onload = function (e) {
                var sentenceName = "sentence";
                var rows = e.target.result.split("\n");
                for (var i = 1; i < rows.length; i++) {
                    var cells = rows[i].split(",");
                    if (cells.length > 1) {
                        var sen = document.createElement("span");
                        sen.setAttribute("id", sentenceName + i);
                        sen.innerHTML = cells[0] + " ";
                        dvCSV.appendChild(sen);
                        var newList = [sentenceName + i, cells[0] + " ", cells[1], cells[2]];
                        sentencesAndValues.push(newList);
                    }
                }
                rangeSize = 100 / sentencesAndValues.length;
                orderToHide = sortInLeastAmountOfKeepVotes(sentencesAndValues);
                var n = document.createElement("div");
                n.innterHTML = "" + rangeSize;
                dvCSV.appendChild(n);
            }
            reader.readAsText(fileUpload.files[0]);
        } else {
            alert("This browser does not support HTML5.");
        }
    } else {
        alert("Please upload a valid CSV file.");
    }
}

//This function sorts the sentences in order of least to most amount of keep votes 
//returns the list of ids to hide
function sortInLeastAmountOfKeepVotes(sents) {
    sents.sort(function (a, b) {
        return a[3] - b[3];
    });
    
    var toReturn = [];
    
    for(var i = 0; i < sents.length; i++) {
        toReturn.push(sents[i][0]);
    }
    
    return toReturn;
}

function Return() {
    slider.style.display = "none";
    output.style.display = "none";
    fileUpload.style.display = 'block';
    upload.style.display = "block";
    back.style.display = "none";
    dvCSV.style.display = "none";
    sentencesAndValues = [];
    orderToHide = []
    rangeSize = 100;
}