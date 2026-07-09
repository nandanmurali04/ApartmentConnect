import { useEffect, useState } from "react";
import api from "../services/api";
import "./Flats.css";

function Flats() {

    const [flats, setFlats] = useState([]);

    const [showForm, setShowForm] = useState(false);

    const [editingId, setEditingId] = useState(null);

    const [newFlat, setNewFlat] = useState({
        flat_number: "",
        block: "",
        floor: "",
        flat_type: "",
        maintenance_amount: "",
        is_occupied: false,
    });

    useEffect(() => {
        loadFlats();
    }, []);

    const loadFlats = async () => {

        try {

            const response = await api.get("/flats/");
            setFlats(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    const saveFlat = async () => {

        try {

            if (editingId === null) {

                await api.post("/flats/", newFlat);

                alert("Flat added successfully!");

            } else {

                await api.put(`/flats/${editingId}`, newFlat);

                alert("Flat updated successfully!");

            }

            setShowForm(false);

            setEditingId(null);

            setNewFlat({
                flat_number: "",
                block: "",
                floor: "",
                flat_type: "",
                maintenance_amount: "",
                is_occupied: false,
            });

            loadFlats();

        } catch (error) {

            console.log(error);

            alert("Operation failed.");

        }

    };

    const editFlat = (flat) => {

        setEditingId(flat.id);

        setNewFlat({
            flat_number: flat.flat_number,
            block: flat.block,
            floor: flat.floor,
            flat_type: flat.flat_type,
            maintenance_amount: flat.maintenance_amount,
            is_occupied: flat.is_occupied,
        });

        setShowForm(true);

    };

    const deleteFlat = async (flatId) => {

        const confirmDelete = window.confirm(
            "Are you sure you want to delete this flat?"
        );

        if (!confirmDelete) return;

        try {

            await api.delete(`/flats/${flatId}`);

            alert("Flat deleted successfully!");

            loadFlats();

        } catch (error) {

            console.log(error);

            alert("Unable to delete flat.");

        }

    };

    return (

        <div className="flats-page">

            <h1>Apartment Flats</h1>

            <button
                className="add-btn"
                onClick={() => {

                    setEditingId(null);

                    setNewFlat({
                        flat_number: "",
                        block: "",
                        floor: "",
                        flat_type: "",
                        maintenance_amount: "",
                        is_occupied: false,
                    });

                    setShowForm(true);

                }}
            >
                + Add Flat
            </button>

            {showForm && (

                <div className="flat-form">

                    <input
                        type="text"
                        placeholder="Flat Number"
                        value={newFlat.flat_number}
                        onChange={(e) =>
                            setNewFlat({
                                ...newFlat,
                                flat_number: e.target.value,
                            })
                        }
                    />

                    <input
                        type="text"
                        placeholder="Block"
                        value={newFlat.block}
                        onChange={(e) =>
                            setNewFlat({
                                ...newFlat,
                                block: e.target.value,
                            })
                        }
                    />

                    <input
                        type="number"
                        placeholder="Floor"
                        value={newFlat.floor}
                        onChange={(e) =>
                            setNewFlat({
                                ...newFlat,
                                floor: Number(e.target.value),
                            })
                        }
                    />

                    <input
                        type="text"
                        placeholder="Flat Type"
                        value={newFlat.flat_type}
                        onChange={(e) =>
                            setNewFlat({
                                ...newFlat,
                                flat_type: e.target.value,
                            })
                        }
                    />

                    <input
                        type="number"
                        placeholder="Maintenance Amount"
                        value={newFlat.maintenance_amount}
                        onChange={(e) =>
                            setNewFlat({
                                ...newFlat,
                                maintenance_amount: Number(e.target.value),
                            })
                        }
                    />

                    <label className="checkbox">

                        <input
                            type="checkbox"
                            checked={newFlat.is_occupied}
                            onChange={(e) =>
                                setNewFlat({
                                    ...newFlat,
                                    is_occupied: e.target.checked,
                                })
                            }
                        />

                        Occupied

                    </label>

                    <div className="form-buttons">

                        <button
                            className="save-btn"
                            onClick={saveFlat}
                        >
                            {editingId === null ? "Save Flat" : "Update Flat"}
                        </button>

                        <button
                            className="cancel-btn"
                            onClick={() => {

                                setShowForm(false);
                                setEditingId(null);

                            }}
                        >
                            Cancel
                        </button>

                    </div>

                </div>

            )}

            <table>

                <thead>

                    <tr>
                        <th>Flat</th>
                        <th>Block</th>
                        <th>Floor</th>
                        <th>Type</th>
                        <th>Maintenance</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>

                </thead>

                <tbody>

                    {flats.map((flat) => (

                        <tr key={flat.id}>

                            <td>{flat.flat_number}</td>
                            <td>{flat.block}</td>
                            <td>{flat.floor}</td>
                            <td>{flat.flat_type}</td>
                            <td>₹{flat.maintenance_amount}</td>

                            <td>
                                {flat.is_occupied ? "Occupied" : "Vacant"}
                            </td>

                            <td>

                                <button
                                    className="edit-btn"
                                    onClick={() => editFlat(flat)}
                                >
                                    ✏ Edit
                                </button>

                                <button
                                    className="delete-btn"
                                    onClick={() => deleteFlat(flat.id)}
                                >
                                    🗑 Delete
                                </button>

                            </td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default Flats;