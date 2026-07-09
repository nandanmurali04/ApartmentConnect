import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {

    const navigate = useNavigate();

    const handleLogin = () => {
        navigate("/dashboard");
    };

    return (
        <div className="login-container">

            <div className="login-card">

                <h1>ApartmentConnect</h1>

                <p>Smart Apartment Management System</p>

                <input
                    type="text"
                    placeholder="Username"
                />

                <input
                    type="password"
                    placeholder="Password"
                />

                <button onClick={handleLogin}>
                    Login
                </button>

            </div>

        </div>
    );
}

export default Login;