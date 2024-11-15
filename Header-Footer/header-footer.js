

class SpecialHeader extends HTMLElement{
    connectedCallback(){
        this.innerHTML=`
        <head>
        <link href="https://cdn.jsdelivr.net/npm/remixicon@2.5.0/fonts/remixicon.css" rel="stylesheet">

        <link rel="stylesheet" href="../Header-Footer/Stylesheets/style.css">
        
    
       
        </head>
         <nav>
        <img src="../nurse/images/KingaBoraLogo.jpg" alt="Logo">

        <!-- Navigation Links -->
        <ul class="nav__links" id="nav-links">
            <li><a href="../LandingPage/altIndex.html">Home</a></li>
            <li><a href="../HeaderLinks/About.html">About</a></li>
            <li><a href="../HeaderLinks/Contacts.html">Contact</a></li>
            <li><a href="#">Services</a></li>
        </ul>

        <!-- Sign Up and Log In Buttons -->
        <div class="header-buttons" id="header-buttons">
            <button><a href="../authentication/signup.html" class="headerlinks" >Sign Up</a></button>
            <button><a href="../authentication/login.html" class="headerlinks">Log In</a></button>
        </div>

        <!-- Menu Icon for Small Screens -->
        <div class="nav__menu__btn" id="menu-btn">
            <i class="ri-menu-line"></i>
        </div>
    </nav>

        `
    }
}
class SpecialFooter extends HTMLElement{
    connectedCallback(){
        this.innerHTML=`

        <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        
        </head>
       
         <footer>
        <div class="news-letter">
            <img src="../nurse/images/KingaBoraLogo.jpg">
            <br>
            <p>Join Our newsletter to stay up to date <br> by subscribing you agree to our <a href="">PrivacyPolicy</a> and <br> provide consent to receive updates from KingaBora</p>
            <input type="email" placeholder="Enter your email">
            <button class="Subscribe-btn">Subscribe</button>
        </div>

        <table>
            <tr>
                <th>Kinga Bora</th>
                <th>Useful links</th>
                <th>Follow us</th>
            </tr>
            <tr>
                <td><a href="#">Home</a></td>
                <td><a href="#">Privacy Policy</a></td>
                <td><a href="#"><i class="fab fa-facebook"></i> Facebook</a></td>
            </tr>
            <tr>
                <td><a href="#">About Us</a></td>
                <td><a href="#">Terms and Conditions</a></td>
                <td><a href="#"><i class="fab fa-instagram"></i> Instagram</a></td>
            </tr>
            <tr>
                <td><a href="#">Contact Us</a></td>
                <td><a href="#">FAQs</a></td>
                <td><a href="#"><i class="fab fa-twitter"></i> Twitter</a></td>
            </tr>
            <tr>
                <td><a href="#">Our Services</a></td>
                <td><a href="#">Blog Post</a></td>
                <td><a href="#"><i class="fab fa-youtube"></i> YouTube</a></td>
            </tr>
            <tr>
                <td><a href="#">Our Mantra</a></td>
                <td><a href="#">Payment Methods</a></td>
                <td><a href="#"><i class="fab fa-linkedin"></i> LinkedIn</a></td>
            </tr>
        </table>
    </footer>
        `
    }
}
customElements.define('special-header', SpecialHeader);
customElements.define('special-footer', SpecialFooter);

const menuBtn = document.getElementById('menu-btn');
const menuIcon = menuBtn.querySelector('i');
const navLinks = document.getElementById('nav-links');
const headerButtons = document.getElementById('header-buttons');


window.addEventListener('load', () => {
    headerButtons.classList.add('show');
});


// Toggle the 'open' class on click to show/hide the menu
menuBtn.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const isOpen = navLinks.classList.contains('open');
    menuIcon.setAttribute('class', isOpen ? 'ri-close-line' : 'ri-menu-line');
});

// Show the buttons after the page has loaded

// When a link is clicked, close the menu and change the icon back
navLinks.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuIcon.setAttribute('class', 'ri-menu-line');
});
