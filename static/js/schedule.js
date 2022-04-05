let groups = [];
let schedule = null;

$(document).ready(function () {
    let groupSelect = $("#group-select");
    $.get('/database/groups', function (res) {
        for (let i = 0; i < res.length; i++) {
            groups.push(res[i].id);
            groupSelect.append(`<option value="${res[i].id}">${res[i].id}</option>`)
        }
        $.get('/schedule', function (res) {
            schedule = res['schedule'];
            show_shedule($("#group-select").val());
        })
    });
});

function groupChanged() {
    let group = $("#group-select").val();
    show_shedule(group);
}

function show_shedule(group) {
    let slots = $(".course");
    for (let i = 0; i < slots.length; i++) {
        slots[i].classList.add('invisible');
    }

    for (let i = 0; i < schedule.length; i++) {
        if (schedule[i].group.includes(group)) {
            slots[schedule[i].time_slot].classList.remove("invisible");
            for (let j = 0; j < slots[schedule[i].time_slot].children.length; j++) {
                let item = slots[schedule[i].time_slot].children[j];
                switch (item.className) {
                    case "title":
                        item.textContent = schedule[i].course;
                        break;
                    case "teacher":
                        item.textContent = schedule[i].teacher;
                        break;
                    case "room":
                        item.textContent = schedule[i].room;
                        break;
                    case "type":
                        item.textContent = schedule[i].type;
                        break;
                }
            }
        }
    }
}