const deleteNotesButton = document.getElementById("delete");
const notes = document.getElementsByClassName("note");
const notesToDelete = document.getElementById("notesToDelete");

function getNotesToDelete() {
  let notesToDeleteArray = [];
  for (let index = 0; index < notes.length; index++) {
    const noteTitle = notes[index].children[0].innerHTML;
    const noteContent = notes[index].children[1].innerHTML;
    const note = `${noteTitle}|${noteContent}`;
    notesToDeleteArray.push(note);
  }
  const notesToDeleteString = notesToDeleteArray.join("\n");
  return notesToDeleteString;
}

deleteNotesButton.addEventListener("click", function() {
  notesToDelete.value = getNotesToDelete();
  window.location.replace("/delete");
  return false;
});