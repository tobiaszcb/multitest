let markAsFinished = () => {
    let div = document.getElementById('zero');
    for (child of div.children) {
        div.removeChild(child)
    }
    
    let newDiv = document.createElement('DIV')
    let newH = document.createElement('H2')
    newH.appendChild(document.createTextNode('TEST ARE ALREADY EXECUTING!'))
    let newP1 = document.createElement('P');
    newP1.appendChild(document.createTextNode(
        "IF SOMETHING WENT WRONG AND YOU TESTS SHOULD LAUNCH"
    ))
    let newP2 = document.createElement('P');
    newP2.appendChild(document.createTextNode(
        "CLICK BUTTON BELLOW TO MARK THEM AS FINISHED AND REFRESH PAGE TO RUN TESTS"
    ))
    let newButton = document.createElement('INPUT')
    newButton.setAttribute('type', 'button')
    newButton.setAttribute('name', 'button')
    newButton.setAttribute('id','mark-as-finished')
    newButton.setAttribute('class', 'btn btn-outline-dark test-button')
    newButton.setAttribute('value','MARK AS FINISHED')
        
    
    newDiv.appendChild(newH)
    newDiv.appendChild(document.createElement('br'))
    newDiv.appendChild(newP1)
    newDiv.appendChild(newP2)
    newDiv.appendChild(document.createElement('br'))
    div.appendChild(newDiv)

    $("h3:contains('RESULTS')").remove() // remove h3 tag with RESULTS
    document.getElementsByClassName('result')[0]
        .appendChild(newButton);

    document.getElementById('mark-as-finished')
        .addEventListener("click", () => {
            $.ajax({
                url: `http://${window.location.host}/tests/mark-as-finished/`,
                method: 'GET',
                success: () => {alert("DONE")}
            })
        })
        

}
