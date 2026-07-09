import { useEffect, useState } from "react";
import api from "../services/api";
import "./Dashboard.css";

function Dashboard() {

    const [dashboard, setDashboard] = useState({
        total_flats: 0,
        occupied_flats: 0,
        vacant_flats: 0,
        total_owners: 0,
        pending_maintenance: 0,
        paid_maintenance: 0,
        total_collection: 0,
    });

    useEffect(() => {

        loadDashboard();

    }, []);

    const loadDashboard = async () => {

        try {

            const response = await api.get("/dashboard/");

            setDashboard(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    return (

        <div className="dashboard">

            <h1>ApartmentConnect Dashboard</h1>

            <div className="cards">

                <div className="card">
                    <h2>Total Flats</h2>
                    <p>{dashboard.total_flats}</p>
                </div>

                <div className="card">
                    <h2>Occupied</h2>
                    <p>{dashboard.occupied_flats}</p>
                </div>

                <div className="card">
                    <h2>Vacant</h2>
                    <p>{dashboard.vacant_flats}</p>
                </div>

                <div className="card">
                    <h2>Total Owners</h2>
                    <p>{dashboard.total_owners}</p>
                </div>

                <div className="card">
                    <h2>Pending</h2>
                    <p>{dashboard.pending_maintenance}</p>
                </div>

                <div className="card">
                    <h2>Paid</h2>
                    <p>{dashboard.paid_maintenance}</p>
                </div>

                <div className="card">
                    <h2>Collection</h2>
                    <p>₹{dashboard.total_collection}</p>
                </div>

            </div>

        </div>

    );

}

export default Dashboard;