let width = screen.availWidth;
console.log(width);
if (width < 561) {
    let navbar = document.getElementById("navigation");
    navbar.remove();

    // let nav = document.createElement("span");
    // nav.setAttribute = "id", "nav_btn";

    // let hamburger = document.createElement("img");
    // nav.setAttribute = "id", "humburger_icon";
    // nav.setAttribute = "src", "./Hamburger_icon.png";

    // nav.appendChild(hamburger);

    // let check = document.getElementById("box");
    // console.log(check);

    function dropdown_menu() {
        let check = document.getElementById("box");
        console.log(check);


        // if (check != null) {
        let icon = document.getElementById("hamburger_icon");
        icon.remove();
        let dropdown = document.createElement("span");
        dropdown.setAttribute = "id", "box";
        dropdown.className = "box";

        let download = document.createElement("a");
        download.href = "./index.html";
        let download_display = document.createTextNode("Home");
        download.appendChild(download_display);

        let about = document.createElement("a");
        about.href = "./about2.o.html"
        let about_display = document.createTextNode("About");
        about.appendChild(about_display);

        let help = document.createElement("a");
        help.href = "./help2.0.html"
        let help_display = document.createTextNode("Help");
        help.appendChild(help_display);

        dropdown.appendChild(download);
        dropdown.appendChild(about);
        dropdown.appendChild(help);

        //dropdown.s

        let top = document.getElementById("top");
        top.appendChild(dropdown);
        // }
    }
}
