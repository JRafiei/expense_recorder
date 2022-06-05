const addExpenseMsg = document.querySelector('#add-expense-msg');
const addExpenseBtn = document.querySelector('#add-expense button');
const titleInput = document.querySelector('#add-expense #title');
const valueInput = document.querySelector('#add-expense #value');
const timestampInput = document.querySelector('#add-expense #timestamp');
const categoryInput = document.querySelector('#add-expense #category');
const monthPicker = document.querySelector('.month-picker');
const yearSelect = monthPicker.querySelector('#year');

const GetData = async(url, data) => {
    const response = await fetch(url);
    const responseData = await response.json();
    return responseData;
}
const PostData = async(url, data) => {
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const responseData = await response.json();
    return responseData;
}
const addExpense = async (title, value, category, timestamp) => {
    const responseData = await PostData('/add-expense', {
            'title': title,
            'value': value,
            'cat': category,
            'timestamp': timestamp
    });
    if (responseData.status == "success") {
        // addExpenseMsg.innerHTML = `
        // <div class="alert alert-success alert-dismissible fade show" role="alert">
        //   <strong>Expense Added Successfully!</strong> You can add another expense right now!
        //   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        // </div>`;
        // titleInput.value = "";
        // valueInput.value = "";
        // categoryInput.value = categoryInput.querySelector("option:first-child").value;
        window.location.href = "/";
    }
}

addExpenseBtn.addEventListener('click', e => {
    e.preventDefault();
    const title = titleInput.value;
    const value = valueInput.value;
    const category = categoryInput.value;
    const timestamp = timestampInput.value;
    addExpense(title, value, category, timestamp);
})

monthPicker.addEventListener('click', e => {
    if (e.target.tagName.toLowerCase() === 'button') {
        let = url = '/monthly-expenses?' 
        const params = new URLSearchParams({
            'year': yearSelect.value,
            'month': e.target.innerText
        });
        url += params;
        window.open(url, '_blank');
    }
})