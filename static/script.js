const tables = {
//    rooms: document.getElementById('rooms'),
//    reservations: document.getElementById('reservations'),
    cases: document.getElementById('cases'),
    detective: document.getElementById('detective')
};

function showTable(name) {
    for (var table of Object.values(tables))
        table.classList.add('hidden');
    tables[name].classList.remove('hidden');
}

async function tranDetails(id) {
    url = "/t?id=" + id;
    let details = await (await fetch(url)).json();
    if (details.status == 1)
        var status = "Success";
    else if (details.status == 0)
        var status = "Pending";
    else var status = "Declined";
    const message = `Transaction ID: ${id}
    Date: ${details.date}
    Amount: ${details.amount}
    Payment Mode: ${details.payment}
    Payment Status: ${status}`;
    alert(message);
}

const buttons = {
//    rooms: tables.rooms.querySelectorAll("button"),
//    reservations: tables.reservations.querySelectorAll("button"),
    cases: tables.cases.querySelectorAll("button"),
    detective: tables.detective.querySelectorAll("button")
};

//for (var btn of buttons.rooms) {
//    if (btn.getAttribute("data-type") == "delete") {
//        const id = btn.getAttribute("data-id");
//        btn.addEventListener("click", () => {
//            window.location.href = "/del/room?id=" + id;
//        })
//    }
//}

//for (var btn of buttons.reservations) {
//    if (btn.getAttribute("data-type") == "delete") {
//        const id = btn.getAttribute("data-id");
//        btn.addEventListener("click", () => {
//            window.location.href = "/del/res?id=" + id;
//        })
//    }
//}

for (var btn of buttons.cases) {
    if (btn.getAttribute("data-type") == "delete") {
        const id = btn.getAttribute("data-id");
        btn.addEventListener("click", () => {
            window.location.href = "/del/" + id;
        })
    }
}

for (var btn of buttons.cases) {
    if (btn.getAttribute("data-type") == "edit") {
        const id = btn.getAttribute("data-id");
        btn.addEventListener("click", () => {
            window.location.href = "/edit/" + id;
        })
    }
}


for (var btn of buttons.cases) {
    if (btn.getAttribute("data-type") == "view") {
        const id = btn.getAttribute("data-id");
        btn.addEventListener("click", () => {
            window.location.href = "/view/" + id;
        })
    }
}

for (var btn of buttons.detective) {
    if (btn.getAttribute("data-type") == "delete") {
        const id = btn.getAttribute("data-id");
        btn.addEventListener("click", () => {
            window.location.href = "/del/emp?id=" + id;
        })
    }
}

const clearBtn = document.getElementById("clear");
clearBtn.addEventListener('click', () => {
    if (confirm("Clear The Entire Database?")) {
        window.location.href = '/clear';
    }
})