const dateStartInput = document.querySelector("#date_start");
const dateEndInput = document.querySelector("#date_end");
let dateRange = "";

dateStartInput.addEventListener("change", function () {
  dateEndInput.min = this.value;
  if (dateEndInput) {
    dateRange = `${this.value} ${dateEndInput.value}`;
  } else {
    dateRange = `${this.value} ${""}`;
  }
  console.log(dateRange);
});
dateEndInput.addEventListener("change", function () {
  dateStartInput.max = this.value;
  if (dateStartInput) {
    dateRange = `${dateStartInput.value} ${this.value}`;
  } else {
    dateRange = `${""} ${this.value}`;
  }
  console.log(dateRange);
});
