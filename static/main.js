async function getTasks() {
  const response = await fetch("/tasks");
  return await response.json();
}

const make_row = task => `<tr id="${task.id}"><td>${task.name}</td><td>${task.description === null ? "" : task.description}</td><td>${task.due === null ? "" : task.due}</td></tr>`

async function main() {
  let tasks = await getTasks()
  console.log(tasks)
  console.log(tasks.forEach(make_row))
  document.getElementById("main").innerHTML = `<table><tr><th>Nazwa</th><th>Opis</th><th>Data</th></tr>${tasks.map(make_row)}</table>`
}

main()