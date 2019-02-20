let createTagForGuiQueue = element => {
    let queueDiv = document.getElementById('queue-elements')
    
    let newDiv = document.createElement('DIV')
    newDiv.setAttribute('name', element['name'])

    let newP = document.createElement('P');
    newP.setAttribute('name', element['name']
    )
    let newPText = document.createTextNode(element['name'])
    newP.appendChild(newPText)

    let newPInterval = document.createElement('P')
    newPInterval.setAttribute('id', element['interval'].toString())
    newPInterval.style.visibility = 'hidden'

    newDiv.appendChild(newP)
    newDiv.appendChild(newPInterval)
    queueDiv.appendChild(newDiv)
}

let removeFromGuiQueue = interval => {
    let queueDiv = document.getElementById('queue-elements')
    let div = document.querySelector(`div[name='${interval['name']}']`)
    queueDiv.removeChild(div)

}
