async function getTasks() {
  const response = await fetch("/tasks");
  const tasks = await response.json();
  document.getElementById("main").innerHTML = JSON.stringify(tasks);
}


async function main() {
  await getTasks()
}

main()