import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {

    return (

        <nav className="navbar">

            <h2>ApartmentConnect</h2>

            <div className="nav-links">

                <Link to="/dashboard">Dashboard</Link>

                <Link to="/flats">Flats</Link>

                <Link to="/owners">Owners</Link>

                <Link to="/maintenance">Maintenance</Link>

                <Link to="/">Logout</Link>

            </div>

        </nav>

    );

}

export default Navbar;