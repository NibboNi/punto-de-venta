const tableProducts = document.querySelector("#table-body-products");
const clientsWarning = document.querySelector("#clienteWarning");
const clientSearch = document.querySelector("#client");
const clientsSuggestions = document.querySelector("#clients-autocomplete");
const productSearch = document.querySelector("#product");
const productsSuggestions = document.querySelector("#products-autocomplete");
const products = [];
const discountEl = document.querySelector("#discount");
const subtotalEl = document.querySelector("#subtotal");
const totalEl = document.querySelector("#total");
const formTableEl = document.querySelector("#formTable");
const totalsEl = document.querySelector("#totals");
const createSaleBtn = document.querySelector("#createSaleBtn");
const paymentModalContainer = document.querySelector("#paymenthMethod");
const paymentModal = document.querySelector("#paymentModal");
const modalTotal = document.querySelector("#totalPay");
const modalPaymentMethod = document.querySelector("#payment");
const modalImport = document.querySelector("#import");
const modalChange = document.querySelector("#change");
const confirmSaleBtn = document.querySelector("#confirmSale");
const sale = {
  change: -1,
  client: -1,
  import: -1,
  payment: "",
  products: [],
  total: -1,
};
let saleCreated = false;

function search(type, query, url, searchEl, suggetionsEl) {
  if (query.length > 1) {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        suggetionsEl.innerHTML = "";
        suggetionsEl.classList.add("show");

        data.data.forEach((item) => {
          let li = document.createElement("li");
          li.textContent = item.name;

          li.addEventListener("click", function () {
            if (type === "product") {
              searchEl.value = "";
              if (!products.some((product) => product.id === item.id)) {
                item.qty = 1;
                item.discount = 0;
                products.push(item);
              } else {
                const product = products.find(
                  (product) => product.id === item.id
                );
                product.qty += 1;
              }
              createProducts(products);
            } else {
              searchEl.value = this.textContent;
              createSaleBtn.disabled = false;
              sale.client = item.id;
            }

            suggetionsEl.innerHTML = "";
            suggetionsEl.classList.remove("show");
          });

          suggetionsEl.appendChild(li);
        });
      });
  } else {
    suggetionsEl.innerHTML = "";
    suggetionsEl.classList.remove("show");
  }
}

clientSearch.addEventListener("input", function () {
  if (this.value.trim()) {
    let query = this.value.trim();

    search(
      "client",
      query,
      `/panel/autocomplete-clientes/?c=${query}`,
      clientSearch,
      clientsSuggestions
    );
    clientsWarning.classList.remove("show");
  } else {
    clientsWarning.classList.add("show");
    createSaleBtn.disabled = true;
  }
});

productSearch.addEventListener("input", function () {
  let query = this.value.trim();

  search(
    "product",
    query,
    `/panel/autocomplete-productos/?p=${query}`,
    productSearch,
    productsSuggestions
  );
});

function createProducts(products) {
  if (products.length > 0) {
    formTableEl.classList.add("show");
    totalsEl.classList.add("show");
  } else {
    formTableEl.classList.remove("show");
    totalsEl.classList.remove("show");
  }

  tableProducts.innerHTML = "";
  updateTotals();

  products.forEach((product) => {
    const productEl = document.createElement("li");
    productEl.id = product.id;

    const productQty = document.createElement("input");
    productQty.type = "number";
    productQty.min = 1;
    productQty.max = product.existence - product.existence_min;
    productQty.value = product.qty;
    productQty.addEventListener("change", function () {
      product.qty += 1;
      updateTotals();
    });

    const productName = document.createElement("p");
    productName.textContent = product.name;

    const productPrice = document.createElement("p");
    productPrice.textContent = product.sale_price;

    const productDiscount = document.createElement("input");

    productDiscount.addEventListener("change", function () {
      product.discount = this.value;
      updateTotals();
    });
    productDiscount.type = "number";
    productDiscount.min = 0;
    productDiscount.max = 100;
    productDiscount.value = product.discount;

    const productAction = document.createElement("button");
    productAction.type = "button";
    productAction.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <title>elimar de la venta</title>
        <path d="M21.41,11.58L12.41,2.58C12.04,2.21 11.53,2 11,2H4A2,2 0 0,0 2,4V11C2,11.53 2.21,12.04 2.59,12.41L3,12.81C3.9,12.27 4.94,12 6,12A6,6 0 0,1 12,18C12,19.06 11.72,20.09 11.18,21L11.58,21.4C11.95,21.78 12.47,22 13,22C13.53,22 14.04,21.79 14.41,21.41L21.41,14.41C21.79,14.04 22,13.53 22,13C22,12.47 21.79,11.96 21.41,11.58M5.5,7A1.5,1.5 0 0,1 4,5.5A1.5,1.5 0 0,1 5.5,4A1.5,1.5 0 0,1 7,5.5A1.5,1.5 0 0,1 5.5,7M8.12,21.54L6,19.41L3.88,21.54L2.46,20.12L4.59,18L2.46,15.88L3.87,14.47L6,16.59L8.12,14.47L9.53,15.88L7.41,18L9.53,20.12L8.12,21.54Z" />
      </svg>
    `;
    productAction.addEventListener("click", () => {
      const index = products.indexOf(product);
      products.splice(index, 1);
      createProducts(products);
    });

    productEl.appendChild(productQty);
    productEl.appendChild(productName);
    productEl.appendChild(productPrice);
    productEl.appendChild(productDiscount);
    productEl.appendChild(productAction);
    tableProducts.appendChild(productEl);
  });
}

function updateTotals() {
  let discount = products.reduce(
    (acc, product) =>
      acc +
      (Number(product.sale_price) *
        Number(product.qty) *
        Number(product.discount)) /
        100,
    0
  );

  let subtotal = products.reduce(
    (acc, product) => acc + Number(product.sale_price) * Number(product.qty),
    0
  );
  let total = subtotal - discount;

  discountEl.textContent = discount;
  subtotalEl.textContent = subtotal;
  totalEl.textContent = total;
}

createSaleBtn.addEventListener("click", () => {
  modalTotal.value = totalEl.textContent;
  sale.total = Number(totalEl.textContent);
  sale.products = products;
  paymentModalContainer.classList.add("show");
});

modalPaymentMethod.addEventListener("change", function () {
  if (this.value) {
    if (this.value !== "efectivo") {
      modalImport.value = totalEl.textContent;
      modalImport.disabled = true;
      modalChange.value = 0;
      sale.import = modalImport.value;
      sale.change = 0;
    } else {
      modalImport.disabled = false;
      modalImport.value = totalEl.textContent;
    }
    sale.payment = this.value;
  } else {
    modalImport.value = 0;
    modalChange.value = 0;
  }
});

modalImport.addEventListener("change", function () {
  if (this.value >= 0) {
    if (modalImport.value - modalTotal.value >= 0) {
      modalChange.value = modalImport.value - modalTotal.value;
    } else {
      this.value = modalTotal.value;
      modalChange.value = 0;
    }
    sale.change = modalChange.value;
    sale.import = this.value;
  }
});

confirmSaleBtn.addEventListener("click", (e) => {
  e.preventDefault();

  sale.change = Number(modalChange.value);
  sale.import = Number(modalImport.value);
  sale.payment = modalPaymentMethod.value;

  if (
    sale.change >= 0 &&
    sale.client >= 0 &&
    sale.import >= 0 &&
    sale.payment !== "" &&
    sale.products.length > 0 &&
    sale.total >= 0
  ) {
    fetch("/panel/ventas/crear/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(sale),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error en la respuesta del servidor");
        }

        return response.json();
      })
      .then((data) => {
        saleCreated = true;
        const successBox = document.createElement("div");
        successBox.classList.add("success-checkmark");
        const successIcon = document.createElement("div");
        successIcon.classList.add("check-icon");
        const iconTip = document.createElement("span");
        iconTip.classList.add("icon-line", "line-tip");
        const iconLong = document.createElement("span");
        iconLong.classList.add("icon-line", "line-long");
        const iconCircle = document.createElement("div");
        iconCircle.classList.add("icon-circle");
        const iconFix = document.createElement("div");
        iconFix.classList.add("icon-fix");

        successIcon.appendChild(iconTip);
        successIcon.appendChild(iconLong);
        successIcon.appendChild(iconCircle);
        successIcon.appendChild(iconFix);

        successBox.appendChild(successIcon);

        paymentModal.appendChild(successBox);

        const successMessage = document.createElement("p");
        successMessage.textContent = data.message;
        successMessage.classList.add("success-sale");

        paymentModal.appendChild(successMessage);

        const ticketButton = document.createElement("button");
        const ticketText = document.createElement("span");
        ticketText.textContent = "Imprimir ticket";

        confirmSaleBtn.disabled = true;

        ticketButton.id = "saleTicket";
        ticketButton.innerHTML =
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>descargar ticket</title><path d="M3 3V22L6 20L9 22L12 20V13H7V11H14.47L21 14.26V3H3M17 9H7V7H17V9M14 23V19L18 18L14 17V13L24 18L14 23Z" /></svg>';
        ticketButton.appendChild(ticketText);
        ticketButton.classList.add("btn", "btn--add", "btn--sale");

        paymentModal.appendChild(ticketButton);
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Ocurrió un error al crear la venta");
      });
  }
});

paymentModalContainer.addEventListener("click", function () {
  this.classList.remove("show");

  if (saleCreated) {
    window.location.href = "/panel/ventas/";
  }
});

paymentModal.addEventListener("click", (e) => {
  e.stopPropagation();
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
