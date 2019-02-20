
var cancelTests = () => {
    $.ajax({
        url: `http://${window.location.host}/tests/run/all/cancel`,
        type: 'GET',
        error: (xhr, status, err) => {console.log('Error: ' + err)},
        success: (xhr, status, success) => {console.log('Success: ' + success)}
    });
    }

var launchTests = () => {
    $.ajax({
        url:`http://${window.location.host}/tests/run/all`,
        type: 'GET',
        error: (xhr, status,  err) => {
        console.log('Error:');
        console.log(err);
        clearInterval(checkTestsInterval);
        },
        success: (xhr, status, success) => {}
    })
}

var markAsStarted = () => {
    $.ajax({
        url: `http://${window.location.host}/tests/mark-as-started`,
        type: 'GET'
    })
}