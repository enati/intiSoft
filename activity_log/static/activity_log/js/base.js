function viewActivityList() {
    var divBox = document.getElementById("recentActivityBox");
    var span = document.getElementById("viewActivityText");
    divBox.style.display = divBox.style.display === 'none' ? '' : 'none';
    span.innerHTML = span.innerHTML === 'Ver actividad reciente' ? 'Ocultar actividad reciente' : 'Ver actividad reciente';
}