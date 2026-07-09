import { useEffect, useState } from "react";
import api from "../services/api";
import "./Maintenance.css";

function Maintenance() {

    const [maintenance, setMaintenance] = useState([]);

    useEffect(() => {
        loadMaintenance();
    }, []);

    const loadMaintenance = async () => {
        try {
            const response = await api.get("/maintenance/");
            setMaintenance(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const generateBills = async () => {
        try {

            await api.post("/maintenance/generate", {
                month: "October",
                year: 2026,
                due_date: "2026-10-10",
            });

            alert("Maintenance Bills Generated Successfully!");

            loadMaintenance();

        } catch (error) {

            console.log(error);
            alert("Unable to generate bills.");

        }
    };

    const markAsPaid = async (maintenanceId) => {
        try {

            await api.put(`/maintenance/${maintenanceId}/paid`);

            alert("Maintenance marked as Paid!");

            loadMaintenance();

        } catch (error) {

            console.log(error);
            alert("Unable to update payment.");

        }
    };

    const sendReminder = async (maintenanceId) => {
        try {

            await api.post(`/maintenance/${maintenanceId}/reminder`);

            alert("Reminder email sent successfully!");

        } catch (error) {

            console.log(error);
            alert("Unable to send reminder.");

        }
    };

    const exportReport = () => {

        window.open(
            "http://127.0.0.1:8000/maintenance/export",
            "_blank"
        );

        alert("Excel report download started.");

    };

    return (

        <div className="maintenance-page">

            <h1>Maintenance Management</h1>

            <div className="top-buttons">

                <button
                    className="generate-btn"
                    onClick={generateBills}
                >
                    Generate Monthly Bills
                </button>

                <button
                    className="export-btn"
                    onClick={exportReport}
                >
                    📊 Export Excel
                </button>

            </div>

            <table>

                <thead>

                    <tr>
                        <th>Flat</th>
                        <th>Month</th>
                        <th>Year</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Due Date</th>
                        <th>Action</th>
                    </tr>

                </thead>

                <tbody>

                    {maintenance.map((bill) => (

                        <tr key={bill.id}>

                            <td>
                                {bill.flat_number} - Block {bill.block}
                            </td>

                            <td>{bill.month}</td>

                            <td>{bill.year}</td>

                            <td>₹{bill.amount}</td>

                            <td>{bill.status}</td>

                            <td>{bill.due_date}</td>

                            <td>

                                {bill.status !== "Paid" ? (

                                    <div className="action-buttons">

                                        <button
                                            className="paid-btn"
                                            onClick={() => markAsPaid(bill.id)}
                                        >
                                            ✔ Mark Paid
                                        </button>

                                        <button
                                            className="reminder-btn"
                                            onClick={() => sendReminder(bill.id)}
                                        >
                                            📧 Reminder
                                        </button>

                                    </div>

                                ) : (

                                    <span
                                        style={{
                                            color: "green",
                                            fontWeight: "bold",
                                        }}
                                    >
                                        ✔ Paid
                                    </span>

                                )}

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default Maintenance;