let sortby = "id";
let show_no_date = true;

async function getTasks() {
  const response = await fetch("/tasks");
  return await response.json();
}

function strip(x) {
  if (x === null)
    return null
  return x.trim()
}

async function addTask() {
  name = document.getElementById("nazwa").value;
  if (strip(name) === "") {
    alert("Nie można utworzyć zadania bez nazwy")
    return
  }

  let description = document.getElementById("desc").value;
  description = description === "" ? null : description;

  let due = document.getElementById("due").value;
  due = due === "" ? null : due;

  await fetch("/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: strip(name),
      description: strip(description),
      due: due
    }),
  });
  await buildTable()
}

async function rmTask(task) {
  await fetch("/tasks", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: task,
    }),
  });
  await buildTable()
}

function cmp(x,y) {
  let reverse = sortby.startsWith("-") ? -1 : 1;
  switch (sortby.replace(/-/,"")) {
    case "name":
      return reverse*x.name.localeCompare(y.name);

    case "due":
      if(x.due === null)
        return 1
      if(y.due === null)
        return -1;
      return reverse*x.due.localeCompare(y.due);

    case "description":
      if(x.description === null)
        return 1
      if(y.description === null)
        return -1;
      return reverse*x.description.localeCompare(y.description);

    case "id":
      return x.id-y.id;
  }
}


async function switch_sorting(field) {
  if (!sortby.endsWith(field)) {
    sortby = field;
    await buildTable();
    return
  }
  if (sortby.startsWith("-")) {
    sortby = "id"
    await buildTable();
    return
  }
  if (sortby === field) {
    sortby = "-" + field
    await buildTable();
    return;
  }

  sortby = field
  await buildTable();
}

function overdue(days) {
  if (days === null)
    return ""
  if (days<0)
    return "Po terminie"
  return days
}

const make_row = task => `<tr id="${task.id}"><td>${task.name}</td><td>${task.description === null ? "" : task.description}</td><td class="center">${task.due === null ? "" : task.due}</td><td class="center">${overdue(task.days)}</td><td><button onclick="rmTask(${task.id})" class="func">Usuń</button></td></tr>`
const filter_row = task => task.due !== null || show_no_date

async function buildTable() {
  let tasks = await getTasks()
  document.getElementById("main").innerHTML = `
    <table>
      <tr>
        <th onclick="switch_sorting('name')">Nazwa<img id="namearw"></th>
        <th onclick="switch_sorting('description')">Opis<img id="descriptionarw"></th>
        <th onclick="switch_sorting('due')">Data<img id="duearw"></th>
        <th onclick="switch_sorting('due')">Pozostało dni</th>
        <th onclick="show_no_date = !show_no_date; buildTable()">Dodaj/Usuń</th>
      </tr>
      
      ${tasks.toSorted(cmp).filter(filter_row).map(make_row).join("")}
      
      <tr>
        <td><input id="nazwa"></td>
        <td><textarea id="desc"></textarea></td>
        <td><input id="due" type="date"></td>
        <td></td>
        <td><button onclick="addTask()" class="func">Dodaj</button></td>
      </tr>
    </table>`
  if (sortby === "id")
    return
  let arw = sortby.startsWith("-") ? "/static/down.svg" : "/static/up.svg"
  let img = document.getElementById(sortby.replace(/-/,"")+"arw")
  img.src = arw
  img.classList.add("arrow")
}

async function main() {
  await buildTable()
}


main()