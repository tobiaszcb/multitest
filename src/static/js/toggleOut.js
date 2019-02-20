var startTime = new Date(Date.now());
var toggleOut = testName => {
    let div = document.getElementsByName(testName)[0];
    let out = div.getElementsByClassName('out')[0];
    if (out.style.display === "none") {
        out.style.display = "block";
    } else {
        out.style.display = "none";
    }

}