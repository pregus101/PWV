function checkPasswords() {
    const signindiv = document.getElementById("signinbox");
    const mainpage = document.getElementById("mainpage");
    var ename = document.getElementById("username").value;
    var epass = document.getElementById("password").value;
    var access = false;

    ename = ename.toLowerCase();
    console.log(ename);
    let clearance;
    
    fetch('users.json')
        .then(response => response.json())
        .then(data => {
            for (var i = 0; i < data.length; i++) {
                if (data[i]["username"] === ename && data[i]["password"] === epass) {
                    access = true;
                    clearance = data[i]["clearance"];
                    break;
                }
            }

            if (access) {
                signindiv.style = "display: none";
                mainpage.style = "display: block";

                displayhidesecure(clearance);
            } else {
                document.getElementById("incorrect").innerText = "Incorrect Username or Password!";
            }
        })
        .catch(error => console.error('Error fetching users:', error));
}

function displayhidesecure(clearance) {
    const secureitems = document.querySelector(".needsclearance");
    const displayitems = document.querySelector(".display");
    if (clearance >= 3) {
        displayitems.style = "display: none";
        secureitems.style = "display: block";
    } else if (clearance < 3) {
        displayitems.style = "display: block";
        secureitems.style = "display: none";
    }
}

var visible = false;

function togglepwdvis() {
    const pwdin = document.getElementById("password");
    const togglebtn = document.getElementById("showhidepwd");

    if (visible == false) {
        visible = true;
        pwdin.type = "text";
        togglebtn.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
    } else if (visible == true) {
        visible = false;
        pwdin.type = "password";
        togglebtn.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
    
}

function signOut() {
    location.reload();
}
