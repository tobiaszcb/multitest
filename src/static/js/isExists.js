
var checkIfExists = test => {
    let resultDivList = document.getElementsByClassName('result')[0];
    let divList = resultDivList.getElementsByTagName('DIV');

    if (divList.length === 0) {
        return {
            result: undefined,
            resultDivList: resultDivList
        };
    }
    
    let nameArray = [];
    try { // create array which contains names of divs in results
        for (let div of divList) {
            nameArray.push(div.getAttribute('name'));
        }
    } catch (err) {
        console.error(err);
    }
    
    if (nameArray.includes(test.name)) {
        return {
            result: true,
            resultDivList: resultDivList
        }
    } else {
        return {
            result: false,
            resultDivList: resultDivList
        }
    }
}

var checkIfTestResultTagExists = tests => {
    for (let test of tests) {
        let resultObj = checkIfExists(test);
        if (resultObj === undefined) { // if there are no div in results
            continue;
        }
        if (resultObj.result === true) {
            let div = document.getElementsByName(test.name)[0];
            div.addEventListener("click", function() {
                let div = document.getElementsByName(test.name)[0];
                let out = div.getElementsByClassName('out')[0]
                if (out.style.display === "none") {
                    out.style.display = "block";
                } else {
                    out.style.display = "none";
                }
            });
            continue;
        } else {
            createDivForTestResult(test, resultObj.resultDivList);
        }
    }
}

var cleanUp = () => {
    clearInterval(checkTestsInterval); // stop checking for results update
    $('.loader').hide(); // hide spinning wheel
    $('button[id=cancel]').hide(); // hide cancel button
}

var checkIfNewTestSuiteAlreadyCreated = response => {
    let TestSuiteCreatedTime = new Date(response.created);
    TestSuiteCreatedTime.setHours(TestSuiteCreatedTime.getHours() + 1); // weird bug with time
    if (response.created === 0 || response.created === undefined) {
        return;
    }
    if (TestSuiteCreatedTime < startTime) {
        return;
    } else {
        if (response.is_finished) {
            cleanUp();
            $('.status').replaceWith("<h2>DONE</h2>");
            $.ajax({
                url: `http://${window.location.host}/tests/mark-as-finished/`,
                type: 'GET'
            }); // set 'is_running' to False in django session
        }
        checkIfTestResultTagExists(response.tests);
    }

}

var getLatestResults = () => {
    $(window).ready( () => {
        $.ajax({
            url: `http://${window.location.host}/api/get-latest-test-suite/`,
            type: 'GET',
            error: (xhr, status, err) => {console.log('ERROR: ' + err);},
            success: resp => {checkIfNewTestSuiteAlreadyCreated(resp)}
        });
    });
 };

 var checkTestsInterval = setInterval(getLatestResults, 8000);

