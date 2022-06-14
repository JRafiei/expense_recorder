const addExpenseMsg = document.querySelector('#add-expense-msg');
const addExpenseBtn = document.querySelector('#add-expense button');
const titleInput = document.querySelector('#add-expense #title');
const valueInput = document.querySelector('#add-expense #value');
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
const addExpense = async (title, value, category) => {
    const responseData = await PostData('/add-expense', {
            'title': title,
            'value': value,
            'cat': category,
    });
    if (responseData.status == "success") {
        window.location.href = "/";
    }
}

addExpenseBtn.addEventListener('click', e => {
    e.preventDefault();
    const title = titleInput.value;
    const value = valueInput.value;
    const category = categoryInput.value;
    addExpense(title, value, category);
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