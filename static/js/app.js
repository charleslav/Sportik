function onButtonClick() {
    var inputElement = document.getElementById("todo-input")
    var newTodoText = inputElement.value

    var newTodoElement = document.createElement("div")
    newTodoElement.innerHTML = newTodoText

    var todosContainer = document.getElementById("todos-container")
    todosContainer.appendChild(newTodoElement)

    inputElement.value = ""
}