var ctx = document.getElementById('myChart').getContext('2d');
var arrProg = document.getElementById('input_from_python')
var arrComplete= document.getElementById('input_from_python2')
var arrTotal = document.getElementById('input_from_python3')


//alert(arrProg.textContent)
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      datasets: [{ 
          data: JSON.parse(arrTotal.textContent),
          label: "Total",
          borderColor: "rgb(62,149,205)",
          backgroundColor: "rgb(62,149,205,0.1)",
        }, { 
          data: JSON.parse(arrComplete.textContent),
          label: "Completed",
          borderColor: "rgb(60,186,159)",
          backgroundColor: "rgb(60,186,159,0.1)",
        }, { 
          data: JSON.parse(arrProg.textContent),
          label: "In-Progress",
          borderColor: "rgb(255,165,0)",
          backgroundColor:"rgb(255,165,0,0.1)",
        }
      ]
    },
  });