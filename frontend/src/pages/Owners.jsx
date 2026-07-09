import { useEffect, useState } from "react";
import api from "../services/api";
import "./Owners.css";

function Owners() {

    const [owners, setOwners] = useState([]);
    const [flats, setFlats] = useState([]);

    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState(null);

    const [newOwner, setNewOwner] = useState({
        full_name: "",
        email: "",
        phone: "",
        flat_id: "",
    });

    useEffect(() => {
        loadOwners();
        loadFlats();
    }, []);

    const loadOwners = async () => {

        try {

            const response = await api.get("/owners/");
            setOwners(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    const loadFlats = async () => {

        try {

            // CHANGED HERE
            const response = await api.get("/flats/");
            setFlats(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    const saveOwner = async () => {

        try {

            if (editingId === null) {

                await api.post("/owners/", newOwner);
                alert("Owner added successfully!");

            } else {

                await api.put(`/owners/${editingId}`, newOwner);
                alert("Owner updated successfully!");

            }

            setShowForm(false);
            setEditingId(null);

            setNewOwner({
                full_name: "",
                email: "",
                phone: "",
                flat_id: "",
            });

            loadOwners();
            loadFlats();

        } catch (error) {

            console.log(error);
            alert("Operation failed.");

        }

    };

    const editOwner = (owner) => {

        setEditingId(owner.id);

        setNewOwner({
            full_name: owner.full_name,
            email: owner.email,
            phone: owner.phone,
            flat_id: owner.flat_id,
        });

        loadFlats();
        setShowForm(true);

    };

    const deleteOwner = async (ownerId) => {

        const confirmDelete = window.confirm(
            "Are you sure you want to delete this owner?"
        );

        if (!confirmDelete) return;

        try {

            await api.delete(`/owners/${ownerId}`);

            alert("Owner deleted successfully!");

            loadOwners();
            loadFlats();

        } catch (error) {

            console.log(error);
            alert("Unable to delete owner.");

        }

    };

    return (

        <div className="owners-page">

            <h1>Apartment Owners</h1>

            <button
                className="add-btn"
                onClick={() => {

                    setEditingId(null);

                    setNewOwner({
                        full_name: "",
                        email: "",
                        phone: "",
                        flat_id: "",
                    });

                    loadFlats();
                    setShowForm(true);

                }}
            >
                + Add Owner
            </button>

            {showForm && (

                <div className="owner-form">

                    <input
                        type="text"
                        placeholder="Full Name"
                        value={newOwner.full_name}
                        onChange={(e) =>
                            setNewOwner({
                                ...newOwner,
                                full_name: e.target.value,
                            })
                        }
                    />

                    <input
                        type="email"
                        placeholder="Email"
                        value={newOwner.email}
                        onChange={(e) =>
                            setNewOwner({
                                ...newOwner,
                                email: e.target.value,
                            })
                        }
                    />

                    <input
                        type="text"
                        placeholder="Phone"
                        value={newOwner.phone}
                        onChange={(e) =>
                            setNewOwner({
                                ...newOwner,
                                phone: e.target.value,
                            })
                        }
                    />

                    <select
                        value={newOwner.flat_id}
                        onChange={(e) =>
                            setNewOwner({
                                ...newOwner,
                                flat_id: Number(e.target.value),
                            })
                        }
                    >
                        <option value="">
                            Select Flat
                        </option>

                        {flats.map((flat) => (

                            <option
                                key={flat.id}
                                value={flat.id}
                            >
                                {flat.flat_number} - Block {flat.block}
                            </option>

                        ))}

                    </select>

                    <div className="form-buttons">

                        <button
                            className="save-btn"
                            onClick={saveOwner}
                        >
                            {editingId === null ? "Save Owner" : "Update Owner"}
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
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Flat </th>
                        <th>Action</th>
                    </tr>

                </thead>

                <tbody>

                    {owners.map((owner) => (

                        <tr key={owner.id}>

                            <td>{owner.full_name}</td>
                            <td>{owner.email}</td>
                            <td>{owner.phone}</td>
                            <td>{owner.flat_number} - Block {owner.block}</td>

                            <td>

                                <button
                                    className="edit-btn"
                                    onClick={() => editOwner(owner)}
                                >
                                    ✏ Edit
                                </button>

                                <button
                                    className="delete-btn"
                                    onClick={() => deleteOwner(owner.id)}
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

export default Owners;