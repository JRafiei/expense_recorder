const addExpenseMsg = document.querySelector('#add-expense-msg');
const addExpenseBtn = document.querySelector('#add-expense button');
const titleInput = document.querySelector('#add-expense #title');
const valueInput = document.querySelector('#add-expense #value');
const categoryInput = document.querySelector('#add-expense #category');
const addExpense = async (title, value, category) => {
    const response = await fetch('/add-expense', {
        method: 'POST',
        body: JSON.stringify({
            'title': title,
            'value': value,
            'cat': category
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const responseData = await response.json();
    if (responseData.status == "success") {
        addExpenseMsg.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong>Expense Added Successfully!</strong> You can add another expense right now!
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        titleInput.value = "";
        valueInput.value = "";
        categoryInput.value = categoryInput.querySelector("option:first-child").value;
    }

}
addExpenseBtn.addEventListener('click', e => {
    e.preventDefault();
    const title = titleInput.value;
    const value = valueInput.value;
    const category = categoryInput.value;
    addExpense(title, value, category);
})