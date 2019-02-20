var createDivForTestResult = (test, resultDivList) => {
    let testName = test.name.split('.')[0];
    let div = document.createElement('DIV');
    div.setAttribute('name', testName);
    div.setAttribute('class', 'row zoom')
    
    let name = document.createElement('H4');
    let duration = document.createElement('P');
    let err = document.createElement('P');
    let out = document.createElement('P')
    err.setAttribute('class', 'err')
    out.setAttribute('class', 'out')

    let nameText = document.createTextNode(testName);
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
    try{
        resultDivList.appendChild(div);
    } catch (err) {
        console.log(err);
    }
    
}