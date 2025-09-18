
var _0x5a46 = ["f49bf}", "_again_e", "this", "Password Verified", "Incorrect password", "getElementById", "value", "substring", "picoCTF{", "not_this"];

(function (paths, opt_attributes) {
    var setter = function (val) {
        for (; --val;) {
            paths["push"](paths["shift"]());
        }
    };
    setter(++opt_attributes);
})(_0x5a46, 435);

var _0x4b5b = function (key, dataAndEvents) {
    key = key - 0;
    var label = _0x5a46[key];
    return label;
};

console.log(_0x5a46);

// [
//     'getElementById',
//     'value',
//     'substring',
//     'picoCTF{',
//     'not_this',
//     'f49bf}',
//     '_again_e',
//     'this',
//     'Password Verified',
//     'Incorrect password'
//   ]

function verify() {
    checkpass = document[_0x4b5b("0x0")]("pass")[_0x4b5b("0x1")];  //document.getElementById("pass").value
    split = 4;
    if (checkpass[_0x4b5b("0x2")](0, split * 2) == _0x4b5b("0x3")) {
        if (checkpass[_0x4b5b("0x2")](7, 9) == "{n") {
            if (checkpass[_0x4b5b("0x2")](split * 2, split * 2 * 2) == _0x4b5b("0x4")) {
                if (checkpass[_0x4b5b("0x2")](3, 6) == "oCT") {
                    if (checkpass[_0x4b5b("0x2")](split * 3 * 2, split * 4 * 2) == _0x4b5b("0x5")) {
                        if (checkpass["substring"](6, 11) == "F{not") {
                            if (checkpass[_0x4b5b("0x2")](split * 2 * 2, split * 3 * 2) == _0x4b5b("0x6")) {
                                if (checkpass[_0x4b5b("0x2")](12, 16) == _0x4b5b("0x7")) {
                                    alert(_0x4b5b("0x8"));
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        alert(_0x4b5b("0x9"));
    }
}
;