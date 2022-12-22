



// import DateRangePicker from 'flowbite-datepicker/DateRangePicker';

// // Datepicker
// const dateRangePickerEl = document.getElementById('dateRangePickerId');
// new DateRangePicker(dateRangePickerEl, {
//     // options
// }); 

// Chart.js
const data = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
};

const config = {
    type: 'pie',
    data: data,
    options: {
        plugins: {
            legend: {
                position: 'right'
            }
        }
    }
};

// Render the chart

const stockPie = new Chart(
    document.getElementById('stockPie'),
    config
  );

// End Chart.js


// Barcode Lookup from Open Food Facts API 
function BarcodeLookup() {
  console.log("Barcode Lookup Test");
  const barcode = document.getElementById('barcode_search').value;
  console.log(barcode);
  fetch(`https://world.openfoodfacts.org/api/v0/product/${barcode}.json`)
      .then((response) => response.json())
      .then((p) => {      
          if(p.status == 1){
              return p.product;
          }else{
              alert(p.status_verbose);
          }
      }
      ).then((result) => {
          console.log(result.forest_footprint_data);
          document.getElementById('id_brand').value = result.brands;
          document.getElementById('id_barcode').value = result.code;
          document.getElementById('id_name').value = result.product_name || result.product_name_en;
          document.getElementById('id_weight').value = result.product_quantity;
          document.getElementById('id_allergens').value = (result.allergens).replaceAll('en:','');
          document.getElementById('id_category').value = result.categories;
          document.getElementById('id_footprint').value = result.forest_footprint_data.footprint_per_kg;
      })
};


//Local Barcode Lookup from products database (stock in from collections)
function LocalBarcodeLookup() {
  console.log("Local Barcode Lookup Test");
  const barcode = document.getElementById('barcode_search').value;
  console.log(barcode);
  fetch(`http://localhost:8000/api/products/?barcode=${barcode}&format=json`)
  .then(response => response.json())
  .then((result) => {
    console.log(result[0]);
    document.getElementById('id_brand').value = result[0].brand;
    document.getElementById('id_barcode').value = result[0].barcode;
    document.getElementById('id_name').value = result[0].name;
    document.getElementById('id_weight').value = result[0].weight;
    document.getElementById('id_allergens').value = result[0].allergens;
    document.getElementById('id_category').value = result[0].category;
    document.getElementById('id_footprint').value = result[0].footprint;
  })
  .catch(error => console.log('error', error));
};




// Submit Product Form to Database

// function submitProduct() {
//   console.log("Submit Product Test");
//   const barcode = document.getElementById('id_barcodeInput').value;
//   const brand = document.getElementById('id_brand').value;
//   const name = document.getElementById('id_name').value;
//   const weight = document.getElementById('id_weight').value;
//   const allergens = document.getElementById('id_allergens').value;
//   const category = document.getElementById('id_category').value;
//   const product = {
//     barcode: barcode,
//     brand: brand,
//     name: name,
//     weight: weight,
//     allergens: allergens,
//     category: category
//   }
//   console.log(product);
// }

//AJAX SEARCH
// member search
const q = document.getElementById("search");
q.addEventListener("keyup", (event) => {
    if (q.value.length > 0) {
        fetch("/search/" + q.value)
        .then((response) => response.text())
        .then((results) => (document.getElementById("resTable").innerHTML = results));
    }
});

// product search
const p = document.getElementById("p_search");
p.addEventListener("keyup", (event) => {
  if (p.value.length > 0) {
    fetch("/p_search/" + p.value)
      .then((response) => response.text())
      .then((results) => (document.getElementById("p-resTable").innerHTML = results));
  }
});


// Qugga2 Live Barcode Scanner
console.log("Barcode Scanner Test");
navigator.mediaDevices.getUserMedia({ video: true })
  .then(function(stream) {
    var video = document.getElementById('live_scanner');
    video.srcObject = stream;
  })
  .catch(function(error) {
    console.error(error);
  });

// Barcode Scanner Start 
document.getElementById('start-button').addEventListener('click', function() {
  Quagga.init({
    inputStream: {
      type: 'LiveStream',
      target: document.querySelector('#live-video'),
    },
    decoder: {
      readers: ['code_128_reader']
    },
    locate: true,
  }, function(err) {
    if (err) {
      console.error(err);
      return;
    }
    console.log('Initialization finished. Ready to start');
    Quagga.start();
  });
});
  
// Barcode Callback

Quagga.onDetected(function(result) {
  var code = result.codeResult.code;
  console.log('Barcode detected:', code);
  Quagga.stop();
  var barcode_input = document.getElementById('barcode_search');
  barcode_input.value = code;

  BarcodeLookup();

});