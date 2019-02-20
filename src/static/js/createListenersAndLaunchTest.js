var intervals = [] // works like a simple queque

let isShouldSpine = () => {
    let divForSpin = document.getElementById('spin');
    let spinDiv = document.createElement('DIV');
    spinDiv.setAttribute('class', 'loader');

    if (intervals.length !== 0) { // if there are any tasks running
        if (divForSpin.childElementCount === 1) { // and if spinner is not present yet
            divForSpin.appendChild(spinDiv); // add spinner
        }
    } else { // if there are no tasks running
        try { // remove spinner
            divForSpin.removeChild(document.getElementsByClassName('loader')[0]);
        } catch (err) {}
    }
}

setInterval(isShouldSpine, 500);

let createTagForResult = (test) => {
    let div = document.createElement('DIV');
    div.setAttribute('name', test.name);
    div.setAttribute('class', 'row zoom');

    let name = document.createElement('H4');
    let duration = document.createElement('P');
    let err = document.createElement('P');
    let out = document.createElement('P');
    err.setAttribute('class', 'err');
    out.setAttribute('class', 'out');

    let nameText = document.createTextNode(test.name);
    let text = `Test duration: ${test.duration}s`
    let durationText = document.createTextNode(text);
    let errText = document.createTextNode(test.err);

    name.appendChild(nameText);
    duration.appendChild(durationText);
    err.appendChild(errText);

    div.appendChild(name);
    div.appendChild(duration);
    let outArray = test.out.split("[INFO]").slice(1);
    for (let i = 0; i < outArray.length; i++) {
        let p = document.createElement('P');
        let txtNode = document.createTextNode(`[INFO] ${outArray[i]}`)
        p.appendChild(txtNode);
        div.appendChild(p);
    }
    div.appendChild(err);
    let resultDiv = document.getElementsByName('results')[0]
    try{
        resultDiv.appendChild(div);
    } catch (err) {
        console.log(err);
    }
}


let checkIfTestFinished = (results, startTime) => {
    if (results.created.length === 0 || results.created === undefined) {
        return;
    }
    let testCreatedTime = new Date(results.created);
    testCreatedTime.setHours(testCreatedTime.getHours() + 1); //mongoengine bug with time
    if (testCreatedTime < startTime) {
        return;
    } else {
        let intervalToRemove = intervals.shift()
        clearInterval(intervalToRemove['interval']) // stop asking API for results
        createTagForResult(results);
        removeFromGuiQueue(intervalToRemove); // remove from "QUEUE" from gui
        
    }
}


let succesFunc = (name, startTime) => {
    let newInterval = {
        'name': name,
        'interval': setInterval(() => {
            $.ajax({
                url: `http://${window.location.host}/api/get-latest-test/` + name,
                method: 'GET',
                success: response => {checkIfTestFinished(response, startTime);}
            });
        }, 4000)
    }
    intervals.push(newInterval)
    createTagForGuiQueue(newInterval)
}


let createListenersAndLaunchTest = () => {
    var nodes = document.querySelectorAll('input[name=button]');
    $(window).ready( () => {
        for (let element of nodes) {
        element.addEventListener("click", () => {
            let name = element.value
            var startTime = new Date(Date.now());
            $.ajax({
                url: `http://${window.location.host}/tests/run/` + name, // tell django to start celery task
                method: 'GET',
                error: (xhr, status, err) => {console.log('ERROR: ' + err);},
                success: () => {succesFunc(name, startTime)}
            });
        });
    }});

}

createListenersAndLaunchTest();