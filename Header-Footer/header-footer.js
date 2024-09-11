class SpecialHeader extends HTMLElement{
    connectedCallback(){
        this.innerHTML=`
          <nav>
        <img src="images/KingaBoraLogo.jpg">

        <ul>
            <li><a href="">Home</a></li>
            <li><a href="">About</a></li>
            <li><a href="">Contact</a></li>
            <li><a href="">Services</a></li>
        </ul>

        <div class="header-buttons">
            <button>Sign Up</button>
            <button>Log In</button>
        </div>

            
    </nav>
        `
    }
}
class SpecialFooter extends HTMLElement{
    connectedCallback(){
        this.innerHTML=`
         <footer>
        <div class="news-letter">
            <img src="images/KingaBoraLogo.jpg">
            <p>Join Our newsletter to stay up to date</p>
            <input type="email" placeholder="Enter your email">
            <button class="Subscribe-btn">Subscribe</button>
            <p>by subscribing you agree to our <a href="">PrivacyPolicy</a> and provide consent to receive updates from KingaBora</p>
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